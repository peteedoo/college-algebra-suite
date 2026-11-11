#!/usr/bin/env python3
"""Engine v4.7: last three corpus gaps — multi-variable log expansion,
coefficient condensation, and applied decibel-formula substitution."""
from pathlib import Path
import py_compile

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")
assert "__ENGINE_V4_7__" not in src
done = []

def patch(tag, anchor, repl):
    global src
    n = src.count(anchor)
    assert n == 1, f"{tag}: {n} hits"
    src = src.replace(anchor, repl, 1)
    done.append(tag)

# --- H1: balanced-brace \\frac{A}{B} -> (A)/(B) in normalizeLatexToAscii ---
patch("H1-frac",
      """    function normalizeLatexToAscii(raw) {
      if (!raw) return '';
      let s = raw.trim();
      s = s.replace(/\\$/g, '');""",
      """    function normalizeLatexToAscii(raw) {
      if (!raw) return '';
      let s = raw.trim();
      // __ENGINE_V4_7__: balanced-brace \\frac{A}{B} (nested braces allowed)
      // -> (A)/(B). Simple [^{}] regexes miss \\frac{\\sqrt{x}...}{...}.
      s = (function (t) {
        let out = '', i = 0;
        while (i < t.length) {
          const at = t.indexOf('\\\\frac', i) >= 0 ? t.indexOf('\\\\frac', i) : t.indexOf('\\\\dfrac', i);
          const at2 = t.indexOf('\\\\dfrac', i);
          const use = at >= 0 && (at2 < 0 || at <= at2) ? at : at2;
          if (use < 0) { out += t.slice(i); break; }
          out += t.slice(i, use);
          const grab = (from) => {
            let p = from;
            while (p < t.length && t[p] !== '{') p++;
            if (p >= t.length) return null;
            let d = 0, j = p;
            for (; j < t.length; j++) {
              if (t[j] === '{') d++;
              else if (t[j] === '}') { d--; if (d === 0) break; }
            }
            if (j >= t.length) return null;
            return [t.slice(p + 1, j), j + 1];
          };
          let pfx = use;
          while (pfx < t.length && t[pfx] !== '{') pfx++;
          const numG = grab(pfx);
          if (!numG) { out += t.slice(use); break; }
          const denG = grab(numG[1]);
          if (!denG) { out += t.slice(use); break; }
          out += '(' + numG[0] + ')/(' + denG[0] + ')';
          i = denG[1];
        }
        return out;
      })(s);
      s = s.replace(/\\$/g, '');""")

# --- H2: parser detectors, inserted before the logMatch line ----------------
ANCHOR2 = "      const logMatch = logSrc.match(/^([+-]?\\d*\\.?\\d*)?\\s*\\*?\\s*(ln|log(?:_(\\d+(?:\\.\\d+)?))?)\\s*\\(\\s*([^()]+?)\\s*\\)\\s*([+-]\\s*\\d+(?:\\.\\d+)?)?(?:\\s*=\\s*(.+))?$/i);"
BLOCK2 = """      // 10a-1. __ENGINE_V4_7__: applied log formula with substitution —
      //      d = 10log((I)/(I_0)); 100,000,000,000I_0  ->  d = 10*log10(10^11) = 110
      if (/;/.test(logSrc)) {
        const dSegs = logSrc.split(';').map(t2 => t2.trim()).filter(Boolean);
        const formM = dSegs[0] && dSegs[0].match(/^([a-z])\\s*=\\s*(\\d+(?:\\.\\d+)?)\\s*log\\s*\\(\\s*\\(?([a-z][a-z0-9_]*)\\)?\\s*\\/\\s*\\(?([a-z][a-z0-9_]*)\\)?\\s*\\)$/i);
        const unitM = dSegs[1] && dSegs[1].match(/^([\\d,]+(?:\\.\\d+)?)\\s*\\*?\\s*([a-z][a-z0-9_]*)$/i);
        if (formM && unitM && formM[4].toLowerCase() === unitM[2].toLowerCase()) {
          const ratio = parseFloat(unitM[1].replace(/,/g, ''));
          const mult = parseFloat(formM[2]);
          const val = mult * Math.log(ratio) / Math.LN10;
          if (isFinite(ratio) && ratio > 0 && isFinite(val)) {
            const valX = Math.abs(Math.round(val) - val) < 1e-6 ? Math.round(val) : Number(val.toFixed(4));
            return { type: 'log_expr', mode: 'applied', value: valX, ratio: ratio,
                     mult: mult, varName: formM[1], baseVar: formM[4],
                     formula: dSegs[0], raw: logSrc };
          }
        }
      }

      // 10a-2. __ENGINE_V4_7__: condense — c1*log_b(A) + c2*log_b(B) [...]
      //      (same base, no rhs)  ->  log_b(A^c1 · B^c2 ...)
      if (!/[=;]/.test(logSrc)) {
        const cParts = splitTopLevelOps(logSrc);
        if (cParts.length >= 2) {
          const cTerms = []; let cBase = null, cOK = true;
          for (let ci = 0; ci < cParts.length; ci++) {
            const mT = cParts[ci].match(/^([+-]?)\\s*(?:(\\d+(?:\\.\\d+)?)\\s*\\*?\\s*)?log[_]([a-z0-9]+)\\s*\\(([^()]+)\\)$/i);
            if (!mT) { cOK = false; break; }
            const tb = mT[3].toLowerCase();
            if (cBase === null) cBase = mT[3];
            else if (tb !== cBase.toLowerCase()) { cOK = false; break; }
            cTerms.push({ sign: mT[1] === '-' ? -1 : 1,
                          coef: mT[2] !== undefined ? parseFloat(mT[2]) : 1,
                          arg: mT[4].trim() });
          }
          if (cOK && cBase) {
            let cStr = 'log_' + cBase + '(';
            cTerms.forEach(function (t3, ix) {
              const powS = t3.coef === 1 ? '' : '^' + (t3.coef < 0 ? '(' + t3.coef + ')' : t3.coef);
              cStr += (ix > 0 ? (t3.sign < 0 ? '/' : '') : (t3.sign < 0 ? '1/' : '')) +
                      '(' + t3.arg + ')' + powS;
            });
            cStr += ')';
            return { type: 'log_expr', mode: 'condense', baseTok: cBase,
                     terms: cTerms, condenseStr: cStr, raw: logSrc };
          }
        }
      }

      // 10a-3. __ENGINE_V4_7__: multi-variable log expansion —
      //      log_b( sqrt(x)·y^(1/7) / (w^5·sqrt(z)) )
      //      -> 1/2·log_b(x) + 1/7·log_b(y) - 5·log_b(w) - 1/2·log_b(z)
      if (!/[=;]/.test(logSrc)) {
        const mME = logSrc.match(/^log[_]([a-z0-9]+)\\s*(.+)$/i);
        if (mME) {
          let body = mME[2].trim();
          while (body.startsWith('(') && body.endsWith(')')) {
            let dME = 0, balME = true;
            for (let bi = 0; bi < body.length; bi++) {
              if (body[bi] === '(') dME++;
              else if (body[bi] === ')') { dME--; if (dME === 0 && bi < body.length - 1) { balME = false; break; } }
            }
            if (!balME) break;
            body = body.slice(1, -1).trim();
          }
          const slashParts = [];
          let dSP = 0, sSP = 0;
          for (let si = 0; si < body.length; si++) {
            const ch = body[si];
            if (ch === '(') dSP++;
            else if (ch === ')') dSP--;
            else if (ch === '/' && dSP === 0) { slashParts.push(body.slice(sSP, si).trim()); sSP = si + 1; }
          }
          slashParts.push(body.slice(sSP).trim());
          const factors = []; let meOK = slashParts.length >= 1;
          for (let pi = 0; pi < slashParts.length && meOK; pi++) {
            let part = slashParts[pi];
            while (part.startsWith('(') && part.endsWith(')')) {
              let dP = 0, balP = true;
              for (let pj = 0; pj < part.length; pj++) {
                if (part[pj] === '(') dP++;
                else if (part[pj] === ')') { dP--; if (dP === 0 && pj < part.length - 1) { balP = false; break; } }
              }
              if (!balP) break;
              part = part.slice(1, -1).trim();
            }
            const atomRe = /(?:(\\d+(?:\\.\\d+)?)\\s*\\*\\s*)?(sqrt\\(\\s*([a-z])\\s*\\)|([a-z])(?:\\^\\(?\\s*(\\d+(?:\\.\\d+)?(?:\\/\\d+(?:\\.\\d+)?)?)\\s*\\)?)?)/gi;
            for (const mF of part.matchAll(atomRe)) {
              if (mF[3] !== undefined) factors.push({ v: mF[3], k: '1/2', sign: pi === 0 ? 1 : -1 });
              else if (mF[4] !== undefined) factors.push({ v: mF[4], k: mF[5] !== undefined ? mF[5] : '1', sign: pi === 0 ? 1 : -1 });
            }
            const left = part.replace(atomRe, '').replace(/[\\s*·]/g, '');
            if (left.length > 0) meOK = false;
          }
          if (meOK && factors.length >= 2 && slashParts.length >= 2) {
            const expStr = factors.map(function (t4, ix) {
              return (t4.sign < 0 ? ' - ' : (ix === 0 ? '' : ' + ')) +
                     (t4.k === '1' ? '' : t4.k + '·') + 'log_' + mME[1] + '(' + t4.v + ')';
            }).join('');
            return { type: 'log_expr', mode: 'expand-multi', baseTok: mME[1],
                     factors: factors, expandStr: expStr, raw: logSrc };
          }
        }
      }

"""
patch("H2-detectors", ANCHOR2, BLOCK2 + ANCHOR2)

# --- H3: tool rendering for the three new modes ------------------------------
ANCHOR3 = "      if (parsed.type === 'log_expr') {\n        const dec = (v) => Number(v.toFixed(4));\n        const steps = [];\n        if (parsed.mode === 'eval') {"
BLOCK3 = """      if (parsed.type === 'log_expr') {
        const dec = (v) => Number(v.toFixed(4));
        const steps = [];
        // __ENGINE_V4_7__: expansion / condensation / applied-formula modes
        if (parsed.mode === 'expand-multi') {
          return {
            title: `🧩 Logarithm Expansion — Product, Quotient & Power Rules (Ch 4.3): ${raw}`,
            outputVal: `Expanded Form: <strong>${parsed.expandStr}</strong>`,
            steps: [
              `1. Radicals become fractional exponents: √v = v^(1/2), ⁿ√v = v^(1/n).`,
              `2. Quotient Rule: log_b(A/B) = log_b(A) − log_b(B).`,
              `3. Product Rule: log_b(A·C) = log_b(A) + log_b(C).`,
              `4. Power Rule: log_b(v^k) = k·log_b(v).`,
              `5. Result: <strong>${parsed.expandStr}</strong>`
            ]
          };
        }
        if (parsed.mode === 'condense') {
          return {
            title: `🧩 Single Logarithm — Power & Product Rules (Ch 4.3): ${raw}`,
            outputVal: `Condensed (coefficient 1): <strong>${parsed.condenseStr}</strong>`,
            steps: [
              `1. Power Rule: c·log_b(A) = log_b(A^c).`,
              `2. Product Rule: log_b(A) + log_b(C) = log_b(A·C); Quotient Rule for differences.`,
              `3. Result: <strong>${parsed.condenseStr}</strong>`
            ]
          };
        }
        if (parsed.mode === 'applied') {
          const lg = Math.log(parsed.ratio) / Math.LN10;
          return {
            title: `🧮 Applied Logarithm Formula — Substitution (Ch 4.4): ${raw}`,
            outputVal: `${parsed.varName} = <strong>${parsed.value}</strong>`,
            steps: [
              `1. Formula: ${parsed.formula} (common log, base 10).`,
              `2. Substitute the given value (${parsed.baseVar} cancels): ratio = ${parsed.ratio}.`,
              `3. Evaluate: ${parsed.mult}·log₁₀(${parsed.ratio}) = ${parsed.mult}·${dec(lg)} = <strong>${parsed.value}</strong>`
            ]
          };
        }
        if (parsed.mode === 'eval') {"""
patch("H3-tools", ANCHOR3, BLOCK3)

P.write_text(src, encoding="utf-8")
print("PATCHED v4.7:", ", ".join(done))
py_compile.compile(str(P), doraise=True)
print("compiles OK")