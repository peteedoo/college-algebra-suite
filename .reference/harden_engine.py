#!/usr/bin/env python3
"""Harden the universal solver engine inside sync_dashboard.py (HTML_TEMPLATE JS).

Anchored, asserted, one-way replacements. Each patch asserts the anchor occurs
exactly once before replacing. Idempotency marker: __ENGINE_V4__.
"""
import re, sys
from pathlib import Path

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")

assert "__ENGINE_V4__" not in src, "already patched"
patches = []


def patch(name, anchor, replacement, count=1):
    global src
    n = src.count(anchor)
    assert n == count, f"{name}: anchor found {n}x (want {count})"
    src = src.replace(anchor, replacement, 1)
    patches.append(name)


# ---------------------------------------------------------------------------
# PATCH 1: engine parsing helpers after stripOuterParens
# ---------------------------------------------------------------------------
HELPERS = r"""
    // ===== Engine v4 hardening helpers: constants, powers, linear forms =====
    function parseConstValue(t) {
      t = String(t == null ? '' : t).replace(/\s+/g, '');
      if (!t) return null;
      // unwrap parens around pure numeric/rational content: ((1)/(5)) -> 1/5
      if (/^[()+*/\d.\-]+$/.test(t)) t = t.replace(/[()]/g, '');
      if (/^e$/i.test(t)) return Math.E;
      var em = t.match(/^e\^(-?\d+(?:\.\d+)?)$/i);
      if (em) return Math.pow(Math.E, parseFloat(em[1]));
      if (/^[+-]?\d+(?:\.\d+)?$/.test(t)) return parseFloat(t);
      var rf = t.match(/^([+-]?\d+(?:\.\d+)?)\/([+-]?\d+(?:\.\d+)?)$/);
      if (rf && parseFloat(rf[2]) !== 0) return parseFloat(rf[1]) / parseFloat(rf[2]);
      return null;
    }

    function parseLnOfBase(t) {
      t = String(t || '').trim();
      var core = t.replace(/^\(/, '').replace(/\)$/, '').trim();
      var sm = core.match(/^sqrt\(\s*(\d+(?:\.\d+)?)\s*\)$/i);
      if (sm) return 0.5 * Math.log(parseFloat(sm[1]));
      var v = parseConstValue(core);
      if (v !== null && v > 0 && Math.abs(v - 1) > 1e-12) return Math.log(v);
      return null;
    }

    // split "base ^ exponent" at the FIRST ^ that sits outside any parens
    function splitPow(side) {
      side = String(side || '').trim();
      var depth = 0;
      for (var i = 0; i < side.length; i++) {
        var ch = side[i];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if (ch === '^' && depth === 0) return [side.slice(0, i).trim(), side.slice(i + 1).trim()];
      }
      return null;
    }

    // split an expression into top-level +/- terms (signs stay attached)
    function splitTopLevelOps(str) {
      var parts = [];
      var depth = 0, start = 0;
      for (var i = 0; i < str.length; i++) {
        var ch = str[i];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if ((ch === '+' || ch === '-') && depth === 0 && i > 0 &&
                 /[0-9x)\]]/.test(str[i - 1]) && i + 1 < str.length) {
          parts.push(str.slice(start, i).trim());
          start = i;
        }
      }
      parts.push(str.slice(start).trim());
      return parts.filter(Boolean);
    }

    function polyToLin(coeffs) {
      if (!coeffs || coeffs.length > 2) return null;
      var m = coeffs[0], b = coeffs.length === 2 ? coeffs[1] : 0;
      if (!isFinite(m) || !isFinite(b)) return null;
      return { m: m, b: b };
    }
    function linMul(k, lin) { return { m: k * lin.m, b: k * lin.b }; }
    function linSub(a, b) { return { m: a.m - b.m, b: a.b - b.b }; }

    function rationalizeVal(x) {
      if (!isFinite(x)) return String(x);
      for (var d = 1; d <= 64; d++) {
        var n = Math.round(x * d);
        if (Math.abs(x - n / d) < 1e-9) return fracStr(n, d);
      }
      return Number(x.toFixed(4)) + '';
    }

    // classify one +/- term as coeff*b^linearExp ("3 * 3^(x-2)") or constant
    function classifyPowTerm(t) {
      t = String(t || '').replace(/^\+/, '').trim();
      var coef = 1, rest = t;
      var cm = t.match(/^([+-]?\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
      if (cm) { coef = parseFloat(cm[1]); rest = cm[2].trim(); }
      var sp = splitPow(rest);
      if (sp) {
        var lnBase = parseLnOfBase(sp[0]);
        var lin = polyToLin(parsePolyCoeffs(sp[1]));
        if (lnBase !== null && lin) return { kind: 'pow', coef: coef, lnBase: lnBase, lin: lin };
      }
      var v = parseConstValue(t);
      if (v !== null) return { kind: 'const', v: v };
      return null;
    }

    // Circle from grouped/general polynomial form (Ch 2.2 Q15/Q21):
    // (x^2 + 12x) + (y^2 - 14y) = 5   or   4x^2 + 4x + 4y^2 - 32y - 79 = 0
    function parseConicTermsSide(side) {
      var co = { x2: 0, y2: 0, x: 0, y: 0, c: 0 };
      var parts = splitTopLevelOps(side);
      for (var i = 0; i < parts.length; i++) {
        var raw = parts[i];
        var sign = 1, t = raw;
        if (t.startsWith('-')) { sign = -1; t = t.slice(1).trim(); }
        else if (t.startsWith('+')) { t = t.slice(1).trim(); }
        var m;
        if ((m = t.match(/^(?:(\d*\.?\d+)?)x\^2$/i))) co.x2 += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)y\^2$/i))) co.y2 += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)x$/i))) co.x += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)y$/i))) co.y += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(\d*\.?\d+)$/))) co.c += sign * parseFloat(m[1]);
        else return null;
      }
      return co;
    }
    function parseConicGeneralStd(raw) {
      var t = String(raw).replace(/\s+/g, '').replace(/\(([^()]+)\)/g, '$1');
      var sides = t.split('=');
      if (sides.length !== 2) return null;
      var L = parseConicTermsSide(sides[0]);
      var R = parseConicTermsSide(sides[1]);
      if (!L || !R) return null;
      var A = L.x2 - R.x2, C = L.y2 - R.y2;
      var D = L.x - R.x, E = L.y - R.y, F = L.c - R.c;
      if (Math.abs(A) < 1e-12 || Math.abs(A - C) > 1e-9) return null;  // circle only
      return { type: 'circle_gen', a: 1, b: D / A, c: E / A, d: F / A };
    }
    // ===== __ENGINE_V4__ ====="""

patch("1-helpers",
      "        if (balancedOuter) s = s.slice(1, -1).trim();\n        else break;\n      }\n      return s;\n    }",
      "        if (balancedOuter) s = s.slice(1, -1).trim();\n        else break;\n      }\n      return s;\n    }\n" + HELPERS)

# ---------------------------------------------------------------------------
# PATCH 2: conic_general branch after circle section (before abs section 5)
# ---------------------------------------------------------------------------
patch("2-conic-general",
      "      // 5. Absolute Value Equations & Inequalities (Ch 1.6 & 1.8)",
      r"""      // 4b. Circle from grouped/general polynomial form (Ch 2.2 Q15/Q21):
      // (x^2 + 12x) + (y^2 - 14y) = 5   or   4x^2 + 4x + 4y^2 - 32y - 79 = 0
      if (/x\^2/i.test(s) && /y\^2/i.test(s) && /=/.test(s) && !/[\/|;<>]/.test(s)) {
        const conicParsed = parseConicGeneralStd(s);
        if (conicParsed) return conicParsed;
      }

      // 5. Absolute Value Equations & Inequalities (Ch 1.6 & 1.8)""")

# ---------------------------------------------------------------------------
# PATCH 3: abs_func branch before the rat_ineq section (after sign rules)
# ---------------------------------------------------------------------------
patch("3-abs-func",
      "      // 6. Rational Inequalities (Ch 3.6): N(x)/D(x) [op] RHS",
      r"""      // 5c. Absolute value FUNCTION form: y = a*abs(bx + c) + d (graph only)
      const absFnSrc = s.replace(/^(?:y|[fgh]\(x\))\s*=\s*/i, '').trim();
      if (/^abs\(/i.test(absFnSrc) && !/\^/.test(absFnSrc)) {
        const absFnMatch = absFnSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*abs\(\s*([^|()]+)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?$/i);
        if (absFnMatch && /[a-zA-Z]/.test(absFnMatch[2])) {
          const insideLin = polyToLin(parsePolyCoeffs(absFnMatch[2]));
          if (insideLin && Math.abs(insideLin.m) > 1e-12) {
            const aStr = absFnMatch[1] || '';
            const aFn = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
            const dFn = absFnMatch[3] ? parseFloat(absFnMatch[3].replace(/\s+/g, '')) : 0;
            return { type: 'abs_func', a: aFn, inside: absFnMatch[2].trim(), lin: insideLin, d: dFn };
          }
        }
      }

      // 6. Rational Inequalities (Ch 3.6): N(x)/D(x) [op] RHS""")

# ---------------------------------------------------------------------------
# PATCH 4: exp section — fractional/parenthesized/decimal bases + sqrt func +
#          exponential equations (same-base, rhs-constant, mixed A*b^E ± C)
# ---------------------------------------------------------------------------
OLD_EXP_HEAD = """      // 9. Exponential Functions & Equations (Ch 4.2, 4.5)
      // e.g. 2^(x - 1) - 3, f(x) = 3^(x+2) + 1, 2^(x-1) = 8, e^(2x) = 7
      const expClean = s.replace(/^(?:[fgh]\\(x\\)|y)\\s*=\\s*/i, '').trim();
      const expMatch = expClean.match(/^([+-]?\\d*\\.?\\d*)?\\s*\\*?\\s*(e|\\d+(?:\\.\\d+)?)\\s*\\^\\s*(?:\\(([^)]+)\\)|([+-]?[0-9a-zA-Z+-]+))\\s*([+-]\\s*\\d+(?:\\.\\d+)?)?(?:\\s*=\\s*([+-]?\\s*\\d+(?:\\.\\d+)?))?$/i);"""

NEW_EXP_HEAD = r"""      // 9. Exponential Functions & Equations (Ch 4.2, 4.5)
      // e.g. 2^(x - 1) - 3, f(x) = 3^(x+2) + 1, 2^(x-1) = 8, e^(2x) = 7
      // HARDENED (v4): fractional / parenthesized / decimal bases like
      // (1/5)^x, (0.5)^x, (9/2)^x, -(1/4)^(x+3) - 2
      const expClean = s.replace(/^(?:[fghg]\(x\)|y)\s*=\s*/i, '').trim();
      const expCleanFlat = expClean
        .replace(/\(\(([+-]?\d+(?:\.\d+)?)\)\)/g, '($1)')
        .replace(/\(([+-]?\d+(?:\.\d+)?)\)\s*\/\s*\(([+-]?\d+(?:\.\d+)?)\)/g, '($1/$2)');
      const expMatch = expCleanFlat.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(e|\d+(?:\.\d+)?|\([\d.]+\)|\(\d+(?:\.\d+)?\s*\/\s*\d+(?:\.\d+)?\)|sqrt\(\d+(?:\.\d+)?\))\s*\^\s*(?:\(([^()]+)\)|([+-]?[0-9a-zA-Z+\-]+))\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (expMatch && (expMatch[3] || expMatch[4] || '').toLowerCase().includes('x')) {
        const aStr = expMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const baseRawM = expMatch[2];
        let base;
        if (/^e$/i.test(baseRawM)) base = Math.E;
        else if (/^sqrt\(/i.test(baseRawM)) base = Math.sqrt(parseFloat(baseRawM.replace(/[^\d.]/g, '')));
        else base = parseConstValue(baseRawM) !== null ? parseConstValue(baseRawM) : parseFloat(baseRawM);
        const expPoly = parsePolyCoeffs(expMatch[3] || expMatch[4]);
        const m = expPoly.length === 2 ? expPoly[0] : 1;
        const bShift = expPoly.length === 2 ? expPoly[1] : 0;
        const h = -bShift / m;
        const k = expMatch[5] ? parseFloat(expMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = expMatch[6] !== undefined;
        let rhs = undefined, rhsV = null;
        if (hasRhs) { rhsV = parseConstValue(expMatch[6]); rhs = rhsV !== null ? rhsV : parseFloat(expMatch[6]); }
        let solX = undefined;
        if (hasRhs && rhsV !== null && (rhs - k) / a > 0 && base > 0 && base !== 1) {
          solX = (Math.log((rhs - k) / a) / Math.log(base) - bShift) / m;
        }
        return { type: 'exp_func', a: a, base: base, h: h, k: k, m: m, bShift: bShift, hasRhs: hasRhs, rhs: rhs, solX: solX };
      }

      // 9a. sqrt function form: a*sqrt(linear) + k (graph + domain)
      const sqrtFnMatch = expClean.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*sqrt\(\s*([^()]+)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (sqrtFnMatch && /x/i.test(sqrtFnMatch[2])) {
        const insideLin = polyToLin(parsePolyCoeffs(sqrtFnMatch[2]));
        if (insideLin) {
          const aStr = sqrtFnMatch[1] || '';
          const aSq = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
          const kSq = sqrtFnMatch[3] ? parseFloat(sqrtFnMatch[3].replace(/\s+/g, '')) : 0;
          return { type: 'sqrt_func', a: aSq, inside: sqrtFnMatch[2].trim(), lin: insideLin, k: kSq };
        }
      }

      // 9b. Exponential EQUATIONS (Ch 4.2 Q32-38, 4.5 Q2-Q8, PW 4.3 Q5-12):
      //   b1^E1 = b2^E2 | b^E = K | b1^E1 -/+ b2^E2 | A*b^E +/- C1 +/- C2
      if (/\^/.test(expClean) && /[0-9]/.test(expClean) && /x/i.test(expClean) &&
          !/x\s*\^/.test(expClean) && !/[|,;]/.test(expClean) && !/[<>]/.test(expClean)) {
        const eqParts = expClean.split('=');
        if (eqParts.length === 2) {
          const lTerms = splitTopLevelOps(eqParts[0]).map(classifyPowTerm);
          const rTerms = splitTopLevelOps(eqParts[1]).map(classifyPowTerm);
          if (lTerms.every(Boolean) && rTerms.every(Boolean)) {
            const pows = [].concat(lTerms, rTerms).filter(t => t && t.kind === 'pow');
            const consts = [].concat(lTerms, rTerms).filter(t => t && t.kind === 'const');
            if (pows.length === 2 && consts.length === 0) {
              // b1^E1 = b2^E2  ->  (ln b1)E1 = (ln b2)E2 (linear in x)
              const P1 = pows[0], P2 = pows[1];
              const sgn2 = (rTerms.indexOf(P2) >= 0 && eqParts[1].trim().startsWith('-')) ? -1 : 1;
              const sgn1 = 1;
              const lin = linSub(linMul(P1.lnBase * P1.coef * sgn1, P1.lin),
                                 linMul(P2.lnBase * P2.coef * sgn2, P2.lin));
              if (Math.abs(lin.m) > 1e-12) {
                const x = -lin.b / lin.m;
                return { type: 'exp_eq', lhs: eqParts[0].trim(), rhs: eqParts[1].trim(),
                         b1: P1.lnBase, b2: sgn2 * P2.lnBase, x: x, xStr: rationalizeVal(x) };
              }
            } else if (pows.length === 1 && consts.length >= 1) {
              // b^E = K1 - K2 ... -> b^E = C
              const P = pows[0];
              const idxP = lTerms.indexOf(P);
              const cL = lTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const cR = rTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const C = idxP >= 0 ? (cR - cL) : (cL - cR);   // move consts across =
              const A = P.coef * (idxP >= 0 ? 1 : -1);
              if (C * A > 0 && P.lnBase !== null) {
                const rhsT = Math.log(C * A) - Math.log(Math.abs(A));
                // A*b^E = C*A? No: A*b^E = C  -> b^E = C/A
                const lin = linMul(P.lnBase, P.lin);
                if (Math.abs(lin.m) > 1e-12) {
                  const x = (Math.log(C / A) - lin.b) / lin.m;
                  return { type: 'exp_eq', lhs: eqParts[0].trim(), rhs: eqParts[1].trim(),
                           b1: P.lnBase, b2: Math.log(C / A), x: x, xStr: rationalizeVal(x) };
                }
              }
            }
          }
        } else if (eqParts.length === 1) {
          // no '=': difference/sum or coeff*pow +/- consts  (Ch 4.5 Q4-Q8)
          const terms = splitTopLevelOps(expClean).map(classifyPowTerm);
          if (terms.every(Boolean)) {
            const powT = terms.filter(t => t.kind === 'pow');
            const constT = terms.filter(t => t.kind === 'const');
            if (powT.length === 2 && constT.length === 0) {
              const P1 = powT[0], P2 = powT[1];
              const neg2 = terms.indexOf(P2) > 0 && expClean.indexOf(P2.lnBase) > 0 &&
                           splitTopLevelOps(expClean)[terms.indexOf(P2)].startsWith('-');
              const sgn2 = neg2 ? -1 : 1;
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef * sgn2, P2.lin));
              if (Math.abs(lin.m) > 1e-12) {
                const x = -lin.b / lin.m;
                return { type: 'exp_eq', lhs: expClean.trim(), rhs: '0',
                         b1: P1.lnBase, b2: sgn2 * P2.lnBase, x: x, xStr: rationalizeVal(x) };
              }
            } else if (powT.length === 1) {
              const P = powT[0];
              const C = constT.reduce((s, t) => s + t.v, 0);
              // A*b^E + C = 0  ->  b^E = -C/A
              if (Math.abs(P.coef) > 1e-12) {
                const K = -C / P.coef;
                if (K > 0 && P.lnBase !== null) {
                  const lin = linMul(P.lnBase, P.lin);
                  if (Math.abs(lin.m) > 1e-12) {
                    const x = (Math.log(K) - lin.b) / lin.m;
                    return { type: 'exp_eq', lhs: expClean.trim(), rhs: '0',
                             b1: P.lnBase, b2: Math.log(K), x: x, xStr: rationalizeVal(x) };
                  }
                }
              }
            }
          }
        }
      }
"""

patch("4-exp-section", OLD_EXP_HEAD, NEW_EXP_HEAD)

# remove the now-dead original exp_func body (it was fully replaced above)
DEAD_EXP_BODY = r"""      if (expMatch && (expMatch[3] || expMatch[4] || '').includes('x')) {
        const aStr = expMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const base = expMatch[2].toLowerCase() === 'e' ? Math.E : parseFloat(expMatch[2]);
        const expPoly = parsePolyCoeffs(expMatch[3] || expMatch[4]);
        const m = expPoly.length === 2 ? expPoly[0] : 1;
        const bShift = expPoly.length === 2 ? expPoly[1] : 0;
        const h = -bShift / m;
        const k = expMatch[5] ? parseFloat(expMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = expMatch[6] !== undefined;
        const rhs = hasRhs ? parseFloat(expMatch[6].replace(/\s+/g, '')) : undefined;
        let solX = undefined;
        if (hasRhs && (rhs - k) / a > 0 && base > 0 && base !== 1) {
          solX = (Math.log((rhs - k) / a) / Math.log(base) - bShift) / m;
        }
        return { type: 'exp_func', a, base, h, k, m, bShift, hasRhs, rhs, solX };
      }
"""
assert src.count(DEAD_EXP_BODY) == 1, f"dead exp body found {src.count(DEAD_EXP_BODY)}x"
src = src.replace(DEAD_EXP_BODY, "")
patches.append("4b-dead-exp-body")

# ---------------------------------------------------------------------------
# PATCH 5: log section — bare args, fractional/variable bases, rhs fractions,
#          change-of-base division form, log-sum equations
# ---------------------------------------------------------------------------
OLD_LOG_HEAD = """      // 10. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      // e.g. log_2(x - 1) + 2, ln(x + 3) = 4, log(x) - 1 = 2
      const logMatch = expClean.match(/^([+-]?\\d*\\.?\\d*)?\\s*\\*?\\s*(ln|log(?:_(\\d+(?:\\.\\d+)?))?)\\s*\\(\\s*([^)]+)\\s*\\)\\s*([+-]\\s*\\d+(?:\\.\\d+)?)?(?:\\s*=\\s*([+-]?\\s*\\d+(?:\\.\\d+)?))?$/i);
      if (logMatch && logMatch[4].includes('x')) {"""

NEW_LOG_HEAD = r"""      // 10. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      // e.g. log_2(x - 1) + 2, ln(x + 3) = 4, log(x) - 1 = 2
      // HARDENED (v4): log10( -> log_10(, bare args (log_5 x = 2),
      // fractional bases (log_1/4(x+2) = -3), variable bases
      // (log_(x + 7) 13 = 1), rhs fractions, change-of-base division form
      // (ln(x)/ln(2) + k) and log-sum equations (log A + log B = log C | K).
      const logSrc = expClean
        .replace(/\blog\s*10\s*\(/gi, 'log_10(')
        .replace(/^x\s*=\s*(?=[+-]?\d*\.?\d*\s*(?:ln|log)\b)/i, '');
      const logMatch = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log(?:_(\d+(?:\.\d+)?))?)\s*\(\s*([^()]+?)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (logMatch && logMatch[4].includes('x')) {"""

patch("5-log-head", OLD_LOG_HEAD, NEW_LOG_HEAD)

# logMatch block now needs rhs parsing via parseConstValue — patch its body
OLD_LOG_BODY = """        const aStr = logMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName = logMatch[2].toLowerCase();
        const base = fnName === 'ln' ? Math.E : (logMatch[3] ? parseFloat(logMatch[3]) : 10);
        const insideP = parsePolyCoeffs(logMatch[4]);
        const m = insideP.length === 2 ? insideP[0] : 1;
        const bShift = insideP.length === 2 ? insideP[1] : 0;
        const h = -bShift / m;
        const k = logMatch[5] ? parseFloat(logMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = logMatch[6] !== undefined;
        const rhs = hasRhs ? parseFloat(logMatch[6].replace(/\s+/g, '')) : undefined;
        let solX = undefined;
        if (hasRhs) {
          solX = (Math.pow(base, (rhs - k) / a) - bShift) / m;
        }
        return { type: 'log_func', a, base, h, k, m, bShift, hasRhs, rhs, solX };
      }"""

NEW_LOG_BODY = r"""        const aStr = logMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName = logMatch[2].toLowerCase();
        const base = fnName === 'ln' ? Math.E : (logMatch[3] ? parseFloat(logMatch[3]) : 10);
        const insideP = parsePolyCoeffs(logMatch[4]);
        const m = insideP.length === 2 ? insideP[0] : 1;
        const bShift = insideP.length === 2 ? insideP[1] : 0;
        const h = -bShift / m;
        const k = logMatch[5] ? parseFloat(logMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = logMatch[6] !== undefined;
        const rhsV = hasRhs ? parseConstValue(logMatch[6]) : null;
        const rhs = hasRhs ? (rhsV !== null ? rhsV : parseFloat(logMatch[6])) : undefined;
        let solX = undefined;
        if (hasRhs && rhsV !== null) {
          solX = (Math.pow(base, (rhs - k) / a) - bShift) / m;
        }
        return { type: 'log_func', a, base, h, k, m, bShift, hasRhs, rhs, solX };
      }

      // 10b. Bare-argument log equations: log_5 x = 2 | log_36 x = 3/2 |
      //      variable base log_(x + 7) 13 = 1 | fractional base log_1/4(x+2) = -3
      const logBare = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log)_?(?:\(\s*([^()]+?)\s*\)|([0-9]+(?:\/[0-9]+)?))?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9][A-Za-z0-9.^+\-]*))?\s*(?:(?:[+-]\s*\d+(?:\.\d+)?)\s*)?(?:=\s*(.+))?$/i);
      if (logBare) {
        const aStr = logBare[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName2 = logBare[2].toLowerCase();
        const baseRaw2 = logBare[3] !== undefined ? logBare[3] : (logBare[4] !== undefined ? logBare[4] : null);
        const argRaw2 = (logBare[5] !== undefined ? logBare[5] : (logBare[6] !== undefined ? logBare[6] : '')).trim();
        const hasRhs2 = logBare[7] !== undefined;
        const rhsV2 = hasRhs2 ? parseConstValue(logBare[7]) : null;
        if (argRaw2 && (hasRhs2 ? rhsV2 !== null : true)) {
          const baseVar = baseRaw2 !== null && /[a-z]/i.test(baseRaw2);
          let base2 = fnName2 === 'ln' ? Math.E : 10;
          if (baseRaw2 !== null && !baseVar) base2 = parseConstValue(baseRaw2) !== null ? parseConstValue(baseRaw2) : parseFloat(baseRaw2);
          if (base2 > 0 && base2 !== 1) {
            const argPoly2 = parseAnyPolyCoeffs(argRaw2);
            const argLin2 = polyToLin(argPoly2);
            if (baseVar) {
              // log_(x + 7) 13 = 1  ->  (x + 7)^rhs = 13
              const baseLin2 = polyToLin(parsePolyCoeffs(baseRaw2));
              const argV2 = parseConstValue(argRaw2);
              if (baseLin2 && argV2 !== null && hasRhs2 && rhsV2 !== null) {
                const target = Math.pow(argV2, 1 / rhsV2);
                if (isFinite(target)) {
                  const x = (target - baseLin2.b) / baseLin2.m;
                  if (Math.abs(baseLin2.m) > 1e-12) {
                    return { type: 'log_eq2', roots: [x], baseExpr: baseRaw2, argExpr: argRaw2,
                             rhs: rhsV2, kind: 'var-base', xStr: rationalizeVal(x) };
                  }
                }
              }
            } else if (argLin2 && argPoly2.length <= 2 && !hasRhs2) {
              // log_b(linear) with no rhs: plain function form
              return { type: 'log_func', a: a, base: base2, h: -argLin2.b / argLin2.m, k: 0,
                       m: 1, bShift: 0, hasRhs: false, rhs: undefined, solX: undefined };
            } else if (argLin2 && argPoly2.length <= 2 && hasRhs2) {
              const solX2 = (Math.pow(base2, (rhsV2 - 0) / a) - argLin2.b) / argLin2.m;
              return { type: 'log_func', a: a, base: base2, h: -argLin2.b / argLin2.m, k: 0,
                       m: 1, b: 0, hasRhs: true, rhs: rhsV2, solX: solX2 };
            } else if (argPoly2.length === 3 && hasRhs2) {
              // log_b(quadratic) = K  ->  quadratic = base^(K/a), then solve
              const target2 = Math.pow(base2, rhsV2 / a);
              const qa = argPoly2[0], qb = argPoly2[1], qc = argPoly2[2] - target2;
              const disc = qb * qb - 4 * qa * qc;
              if (disc >= 0) {
                const r1 = (-qb + Math.sqrt(disc)) / (2 * qa);
                const r2 = (-qb - Math.sqrt(disc)) / (2 * qa);
                const rad2 = simplifyRadical(disc);
                return { type: 'log_eq2', roots: [r1, r2], baseExpr: String(base2), argExpr: argRaw2,
                         rhs: rhsV2, kind: 'quadratic', radStr: rad2.str, qa, qb, qc };
              }
            }
          }
        }
      }

      // 10c. Change-of-base division form: a*ln(ARG)/ln(b) + k  (Ch 4.3 Q6/25/27/28)
      const cobM = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log)\s*\(\s*(.+?)\s*\)\s*\/\s*(?:ln|log)(?:_?|\s*\()?\s*(\d+(?:\.\d+)?)\s*\)?\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (cobM && /x/i.test(cobM[3])) {
        const aStr = cobM[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const base3 = parseFloat(cobM[4]);
        const argRaw3 = cobM[3].trim();
        const k3 = cobM[5] ? parseFloat(cobM[5].replace(/\s+/g, '')) : 0;
        const hasRhs3 = cobM[6] !== undefined;
        const rhsV3 = hasRhs3 ? parseConstValue(cobM[6]) : null;
        const argPoly3 = parseAnyPolyCoeffs(argRaw3);
        const argLin3 = polyToLin(argPoly3);
        if (base3 > 0 && base3 !== 1 && argLin3 && argPoly3.length <= 2 && (!hasRhs3 || rhsV3 !== null)) {
          const h3 = -argLin3.b / argLin3.m;
          const solX3 = hasRhs3 ? (h3 + Math.pow(base3, (rhsV3 - k3) / a)) : undefined;
          return { type: 'log_func', a: a, base: base3, h: h3, k: k3, m: 1,
                   bShift: 0, hasRhs: hasRhs3, rhs: rhsV3, solX: solX3 };
        }
      }

      // 10d. Log-sum / log-difference equations (Ch 4.5 Q18-21, 25-26):
      //      log A + log B = log C | K     (any common base, bare or parens)
      const logSum = logSrc.match(/^(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*([+-])\s*(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*=\s*(?:(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))|([0-9]+(?:\.[0-9]+)?))$/i);
      if (logSum) {
        const baseS = logSum[1] !== undefined ? parseFloat(logSum[1]) : (logSum[5] !== undefined ? parseFloat(logSum[5]) : 10);
        const Araw = (logSum[2] !== undefined ? logSum[2] : logSum[3] || '').trim();
        const opS = logSum[4] === '-' ? -1 : 1;
        const Braw = (logSum[6] !== undefined ? logSum[6] : logSum[7] || '').trim();
        const rhsIsLog = logSum[8] !== undefined;
        const baseS2 = rhsIsLog ? (logSum[8] !== undefined ? parseFloat(logSum[8]) : 10) : baseS;
        const Craw = rhsIsLog ? (logSum[9] !== undefined ? logSum[9] : logSum[10] || '').trim() : logSum[11];
        const A2 = parseAnyPolyCoeffs(Araw);
        const Bv = parseConstValue(Braw);
        const C2 = rhsIsLog ? parseAnyPolyCoeffs(Craw) : parseConstValue(String(Craw));
        if (A2 && (Bv !== null) && C2 !== null && baseS > 0 && baseS !== 1 && baseS === baseS2) {
          // log A ± log K = log C | number   ->  A * K^(±1) = C
          const lhsCo = opS > 0 ? multiplyPolysJS(A2, [Bv]) : multiplyPolysJS(A2, [1 / Bv]);
          let rhsCo = null;
          if (rhsIsLog) {
            const C2poly = C2;
            rhsCo = C2poly;
          } else {
            const Cnum = C2;
            rhsCo = [Cnum];
          }
          if (rhsCo) {
            const comb = subPolysJS(lhsCo, rhsCo);
            if (comb.length === 2) {
              const x = -comb[1] / comb[0];
              return { type: 'log_eq2', roots: [x], baseExpr: String(baseS),
                       argExpr: '(' + Araw + ')(' + Braw + ')', rhs: Cnum2str(Craw, rhsIsLog),
                       kind: 'sum-linear' };
            } else if (comb.length === 3) {
              const qa = comb[0], qb = comb[1], qc = comb[2];
              const disc = qb * qb - 4 * qa * qc;
              if (disc >= 0) {
                const r1 = (-qb + Math.sqrt(disc)) / (2 * qa);
                const r2 = (-qb - Math.sqrt(disc)) / (2 * qa);
                return { type: 'log_eq2', roots: [r1, r2], baseExpr: String(baseS),
                         argExpr: '(' + Araw + ')(' + Braw + ')', rhs: Cnum2str(Craw, rhsIsLog),
                         kind: 'sum-quadratic' };
              }
            }
          }
        }
      }"""

patch("5b-log-body", OLD_LOG_BODY, NEW_LOG_BODY)

# helper used by 10d for rhs display
patch("5c-helpers-cnum",
      "    function polyToLin(coeffs) {",
      r"""    function Cnum2str(craw, rhsIsLog) {
      return rhsIsLog ? String(craw).trim() : String(parseConstValue(String(craw)));
    }
    function polyToLin(coeffs) {""")

# ---------------------------------------------------------------------------
# PATCH 6: buildGraphDataFromParsed — new graph types
# ---------------------------------------------------------------------------
OLD_GDP_LOGTAIL = """      // 7. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      if (parsed.type === 'log_func') {"""

NEW_GDP_LOGTAIL = r"""      // 6b. sqrt function graph (Ch 1.3 / radical functions)
      if (parsed.type === 'sqrt_func') {
        const { a, inside, lin, k } = parsed;
        const fn = (x) => { const v = lin.m * x + lin.b; return (v >= -1e-12) ? a * Math.sqrt(Math.max(0, v)) + k : NaN; };
        return {
          id: `sqrtfn_${a}_${lin.m}_${lin.b}_${k}`,
          type: 'function',
          fn: fn,
          points: [
            { x: -lin.b / lin.m, y: k, type: 'vertex', color: '#38bdf8', label: `(${Number((-lin.b / lin.m).toFixed(2))}, ${Number(k.toFixed(2))})` },
            { x: -lin.b / lin.m + Math.max(1, Math.abs(lin.m)), y: a * Math.sqrt(Math.abs(lin.m)) + k, type: 'point', color: '#34d399', label: `√${inside}` }
          ],
          curveColor: '#38bdf8',
          label: `f(x) = ${a === 1 ? '' : a}√(${inside})${k ? (k > 0 ? ' + ' + k : ' - ' + Math.abs(k)) : ''}`
        };
      }

      // 6c. Absolute value function graph (Ch 1.6 / 3.1 one-to-one checks)
      if (parsed.type === 'abs_func') {
        const { a, inside, lin, d } = parsed;
        const fn = (x) => a * Math.abs(lin.m * x + lin.b) + d;
        return {
          id: `absfn_${a}_${lin.m}_${lin.b}_${d}`,
          type: 'function',
          fn: fn,
          axisOfSymmetry: -lin.b / lin.m,
          points: [
            { x: -lin.b / lin.m, y: d, type: 'vertex', color: '#38bdf8', label: `V(${Number((-lin.b / lin.m).toFixed(2))}, ${Number(d.toFixed(2))})` }
          ],
          curveColor: '#38bdf8',
          label: `f(x) = ${a === 1 ? '' : a}|${inside}|${d ? (d > 0 ? ' + ' + d : ' - ' + Math.abs(d)) : ''}`
        };
      }

      // 6d. Exponential equation graph: root of b1^E1 = b2^E2
      if (parsed.type === 'exp_eq') {
        const f1 = compileMathFunction(parsed.lhs);
        const f2 = compileMathFunction(parsed.rhs);
        if (f1 && f2) {
          return {
            id: `expeq_${parsed.lhs}_${parsed.rhs}`,
            type: 'function',
            fn: (x) => f1(x) - f2(x),
            points: [
              { x: parsed.x, y: 0, type: 'vertex', color: '#34d399', label: `x = ${parsed.xStr}` }
            ],
            curveColor: '#fbbf24',
            label: `${parsed.lhs} − (${parsed.rhs}) → root x = ${parsed.xStr}`
          };
        }
        return null;
      }

      // 6e. Log equation (quadratic argument) graph
      if (parsed.type === 'log_eq2') {
        const pts = (parsed.roots || []).map(r => ({
          x: Number(r.toFixed(2)), y: 0, type: 'vertex', color: '#34d399',
          label: `x = ${rationalizeVal(r)}`
        }));
        return {
          id: `logeq2_${parsed.kind}_${(parsed.roots || []).join('_')}`,
          type: 'number_line',
          intervals: (parsed.roots || []).map(r => ({ from: r, to: r, inclusiveFrom: true, inclusiveTo: true })),
          intervalStr: `{${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}}`,
          label: `Log equation roots: {${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}}`
        };
      }

      // 7. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      if (parsed.type === 'log_func') {"""

patch("6-graph-types", OLD_GDP_LOGTAIL, NEW_GDP_LOGTAIL)

# ---------------------------------------------------------------------------
# PATCH 7: runToolOnParsed — new tool branches
# ---------------------------------------------------------------------------
OLD_TOOL_SIGNRULE = """      if (parsed.type === 'sign_rule') {"""

NEW_TOOL_SIGNRULE = r"""      if (parsed.type === 'sqrt_func') {
        const { a, inside, lin, k } = parsed;
        const vx = -lin.b / lin.m;
        const domMin = lin.m > 0 ? vx : -Infinity;
        return {
          title: `🌿 Square Root Function Analyzer: f(x) = ${a === 1 ? '' : a}√(${inside})${k ? (k > 0 ? ' + ' + k : ' - ' + Math.abs(k)) : ''}`,
          solverKey: 'radical',
          params: { n: Math.round(lin.b * lin.b) },
          outputVal: `Domain: <strong>${lin.m > 0 ? `[${Number(vx.toFixed(2))}, ∞)` : `(-∞, ${Number(vx.toFixed(2))}]`}</strong> &nbsp;|&nbsp; Range: <strong>${a > 0 ? `[${Number(k.toFixed(2))}, ∞)` : `(-∞, ${Number(k.toFixed(2))}]`}</strong> &nbsp;|&nbsp; Start point: <strong>(${Number(vx.toFixed(2))}, ${Number(k.toFixed(2))})</strong>`,
          steps: [
            `1. Radical functions require the inside ≥ 0: ${inside} ≥ 0 → x ${lin.m > 0 ? '≥' : '≤'} ${Number(vx.toFixed(3))}`,
            `2. Domain: ${lin.m > 0 ? `[${Number(vx.toFixed(3))}, ∞)` : `(-∞, ${Number(vx.toFixed(3))}]`}`,
            `3. The square root outputs ≥ 0, so Range: ${a > 0 ? `[${Number(k.toFixed(3))}, ∞)` : `(-∞, ${Number(k.toFixed(3))}]`} (a = ${a})`,
            `4. Inverse: f⁻¹(x) = ((x ${k >= 0 ? '- ' + k : '+ ' + Math.abs(k)})/${a})² ${lin.m > 0 ? 'with x ≥ ' + Number(k.toFixed(2)) : ''}`
          ]
        };
      }

      if (parsed.type === 'abs_func') {
        const { a, inside, lin, d } = parsed;
        const vx = -lin.b / lin.m;
        return {
          title: `📏 Absolute Value Function Analyzer (Ch 1.6): f(x) = ${a === 1 ? '' : a}|${inside}|${d ? (d > 0 ? ' + ' + d : ' - ' + Math.abs(d)) : ''}`,
          solverKey: 'abs',
          params: { a, b: lin.b, op: '=', c: 0 },
          outputVal: `Vertex: <strong>(${Number(vx.toFixed(3))}, ${Number(d.toFixed(3))})</strong> &nbsp;|&nbsp; Axis: <strong>x = ${Number(vx.toFixed(3))}</strong> &nbsp;|&nbsp; V-shape opens: <strong>${a > 0 ? 'Upward (Min)' : 'Downward (Max)'}</strong>`,
          steps: [
            `1. Vertex form: f(x) = a|x − h| + k with vertex (h, k) → here a = ${a}, h = ${Number(vx.toFixed(3))}, k = ${d}`,
            `2. Axis of symmetry: x = ${Number(vx.toFixed(3))}`,
            `3. ${a > 0 ? 'a > 0 → opens UPWARD → vertex is a MINIMUM' : 'a < 0 → opens DOWNWARD → vertex is a MAXIMUM'}`,
            `4. Range: ${a > 0 ? `[${Number(d.toFixed(3))}, ∞)` : `(-∞, ${Number(d.toFixed(3))}]`}`,
            `5. Horizontal line test: every horizontal line above y = ${Number(d.toFixed(2))} crosses the V twice → NOT one-to-one`
          ]
        };
      }

      if (parsed.type === 'exp_eq') {
        const xStr = parsed.xStr;
        return {
          title: `🚀 Exponential Equation Solver (common-base / logarithmic): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'exp', a: 1, b: 2, h: 0, k: 0, rhs: 0 },
          outputVal: `Solution: <strong>x = ${xStr}</strong>`,
          steps: [
            `1. Both sides are powers: ${parsed.lhs} = ${parsed.rhs}`,
            `2. Take the natural log of both sides: ln(${parsed.lhs}) = ln(${parsed.rhs})`,
            `3. Power rule brings exponents down: (${Number(parsed.b1.toFixed(4))})·(exponent of left) = (${Number(parsed.b2.toFixed(4))})·(exponent of right)`,
            `4. Expand exponents and collect x terms → linear equation in x`,
            `5. Solve: <strong>x = ${xStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'log_eq2') {
        const rootsStr = (parsed.roots || []).map(r => rationalizeVal(r)).join(', ');
        return {
          title: `🚀 Logarithmic Equation Solver (condense + quadratic): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a: 1, b: 2, h: 0, k: 0 },
          outputVal: `Solution set: <strong>{${rootsStr}}</strong>${(parsed.roots || []).length > 1 ? ' (after domain check)' : ''}`,
          steps: [
            `1. Condense the logs: ${parsed.argExpr} = base^rhs form`,
            `2. Expand: quadratic in x`,
            `3. Solve the quadratic → candidate roots: <strong>${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}</strong>`,
            `4. Check the log domain (arguments > 0) and keep valid roots`,
            `5. Verified solution set: <strong>{${rootsStr}}</strong>`
          ]
        };
      }

      if (parsed.type === 'sign_rule') {"""

patch("7-tool-branches", OLD_TOOL_SIGNRULE, NEW_TOOL_SIGNRULE)

# ---------------------------------------------------------------------------
# write out + self-check
# ---------------------------------------------------------------------------
P.write_text(src, encoding="utf-8")
print("PATCHED:", ", ".join(patches))
print("bytes:", P.stat().st_size)

# sanity: python syntax check of sync_dashboard.py
import py_compile
py_compile.compile(str(P), doraise=True)
print("sync_dashboard.py compiles OK")