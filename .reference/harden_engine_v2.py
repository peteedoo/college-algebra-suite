#!/usr/bin/env python3
"""Engine hardening v2 (2nd loop iteration). Marker __ENGINE_V4_2__."""
import py_compile
from pathlib import Path

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")
assert "__ENGINE_V4_2__" not in src and "__ENGINE_V4__" in src
patches = []

def patch(name, anchor, repl):
    global src
    n = src.count(anchor)
    assert n == 1, f"{name}: anchor {n}x"
    src = src.replace(anchor, repl, 1)
    patches.append(name)

# --- E1: exp_func falls through when RHS is not a constant -------------------
patch("E1-expfunc-guard", """        return { type: 'exp_func', a: a, base: base, h: h, k: k, m: m, bShift: bShift, hasRhs: hasRhs, rhs: rhs, solX: solX };
      }""",
"""        // __ENGINE_V4_2__: RHS present but not a constant (e.g. 256^(3x) = 64^(x+2))
        // means exponential EQUATION -> fall through to 9b, don't misreport.
        if (!hasRhs || rhsV !== null) {
          return { type: 'exp_func', a: a, base: base, h: h, k: k, m: m, bShift: bShift, hasRhs: hasRhs, rhs: rhs, solX: solX };
        }
      }""")

# --- E2: sign-aware classifyPowTerm ------------------------------------------
patch("E2-classify-sign", """    function classifyPowTerm(t) {
      t = String(t || '').replace(/^\\+/, '').trim();
      var coef = 1, rest = t;
      var cm = t.match(/^([+-]?\\d+(?:\\.\\d+)?)\\s*\\*\\s*(.+)$/);
      if (cm) { coef = parseFloat(cm[1]); rest = cm[2].trim(); }""",
"""    function classifyPowTerm(t) {
      // __ENGINE_V4_2__: leading '-' signs the WHOLE term (coef included)
      t = String(t || '').trim();
      var sign = 1;
      if (t.startsWith('-')) { sign = -1; t = t.slice(1).trim(); }
      else if (t.startsWith('+')) { t = t.slice(1).trim(); }
      var coef = sign, rest = t;
      var cm = t.match(/^(\\d+(?:\\.\\d+)?)\\s*\\*\\s*(.+)$/);
      if (cm) { coef = sign * parseFloat(cm[1]); rest = cm[2].trim(); }""")

# --- E2b: const case keeps sign ------------------------------------------------
patch("E2b-classify-const", """      var v = parseConstValue(t);
      if (v !== null) return { kind: 'const', v: v };
      return null;
    }""",
"""      var v = parseConstValue(t);
      if (v !== null) return { kind: 'const', v: sign * v };
      return null;
    }""")

# --- E3: 9b/9c use intrinsic signs (drop sgn2/neg2 hacks) ----------------------
patch("E3-eq-signs", """              const P1 = pows[0], P2 = pows[1];
              const sgn2 = (rTerms.indexOf(P2) >= 0 && eqParts[1].trim().startsWith('-')) ? -1 : 1;
              const sgn1 = 1;
              const lin = linSub(linMul(P1.lnBase * P1.coef * sgn1, P1.lin),
                                 linMul(P2.lnBase * P2.coef * sgn2, P2.lin));""",
"""              const P1 = pows[0], P2 = pows[1];
              // __ENGINE_V4_2__: signs are intrinsic to each term now
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef, P2.lin));""")
# both 9b and 9c share the b2 line — replace both at once
src = src.replace("b2: sgn2 * P2.lnBase", "b2: P2.lnBase")
patches.append("E3b+E3e-eq-signs")

patch("E3c-eq2-signs", """            } else if (pows.length === 1 && consts.length >= 1) {
              // b^E = K1 - K2 ... -> b^E = C
              const P = pows[0];
              const idxP = lTerms.indexOf(P);
              const cL = lTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const cR = rTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const C = idxP >= 0 ? (cR - cL) : (cL - cR);   // move consts across =
              const A = P.coef * (idxP >= 0 ? 1 : -1);""",
"""            } else if (pows.length === 1 && consts.length >= 1) {
              // b^E = K1 - K2 ... -> b^E = C  (signs intrinsic)
              const P = pows[0];
              const idxP = lTerms.indexOf(P);
              const cL = lTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const cR = rTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const C = idxP >= 0 ? (cR - cL) : (cL - cR);   // move consts across =
              const A = P.coef;""")

patch("E3d-eq3-signs", """            if (powT.length === 2 && constT.length === 0) {
              const P1 = powT[0], P2 = powT[1];
              const neg2 = terms.indexOf(P2) > 0 && expClean.indexOf(P2.lnBase) > 0 &&
                           splitTopLevelOps(expClean)[terms.indexOf(P2)].startsWith('-');
              const sgn2 = neg2 ? -1 : 1;
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef * sgn2, P2.lin));""",
"""            if (powT.length === 2 && constT.length === 0) {
              const P1 = powT[0], P2 = powT[1];
              // __ENGINE_V4_2__: signs intrinsic; no positional neg2 hack
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef, P2.lin));""")
# E3d fixed the 9b lin computation; b2 handled by the global replace above.

# --- E4: logSrc normalization — 'log 3' -> 'log(3)' ---------------------------
patch("E4-logsrc-spacing", """      const logSrc = expClean
        .replace(/\\blog\\s*10\\s*\\(/gi, 'log_10(')""",
"""      const logSrc = expClean
        .replace(/\\blog\\s*10\\s*\\(/gi, 'log_10(')
        .replace(/\\b(ln|log(?:_\\d+(?:\\.\\d+)?)?)\\s+(\\([^()]*\\)|[A-Za-z0-9][A-Za-z0-9.]*)/gi, '$1($2)')""")

# --- E5: log_expr evaluator + tool branch ------------------------------------
patch("E5-logexpr-helper", """    function Cnum2str(craw, rhsIsLog) {""",
r"""    // ===== __ENGINE_V4_2__: log expression arithmetic (Ch 4.3-4.4) =====
    // Parse "c1 log_b(A1) +/- c2 log_b2(A2) [= RHS]" into evaluated or
    // structurally-expanded form. Returns null when not all-log shaped.
    function parseLogExprShape(str) {
      var t = String(str || '').replace(/\s+/g, ' ').trim();
      if (!t) return null;
      var sides = t.split('=');
      if (sides.length > 2) return null;
      var lhs = sides[0].trim(), rhs = sides.length === 2 ? sides[1].trim() : null;
      function parseSide(side) {
        var parts = splitTopLevelOps(side);
        var terms = [], ok = true, anyLog = false;
        for (var i2 = 0; i2 < parts.length; i2++) {
          var raw = parts[i2];
          var sign = 1, s2 = raw.trim();
          if (s2.startsWith('-')) { sign = -1; s2 = s2.slice(1).trim(); }
          else if (s2.startsWith('+')) s2 = s2.slice(1).trim();
          var cm = s2.match(/^(\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
          var coef = sign, body = s2;
          if (cm) { coef = sign * parseFloat(cm[1]); body = cm[2].trim(); }
          var lm = body.match(/^(?:ln|log)_?\(?\s*(?:([0-9]+(?:\.[0-9]+)?))?\s*\)?\s*(?:\(\s*(.+?)\s*\)|([A-Za-z0-9][^()]*))$/i)
                 || body.match(/^(?:ln|log)\s*(?:\(\s*(.+?)\s*\)|([A-Za-z0-9][^()]*))$/i);
          var vm = null;
          if (!lm) vm = body.match(/^(\d+(?:\.\d+)?)$/);
          if (lm) {
            anyLog = true;
            var baseS = lm[1] !== undefined ? lm[1] : null;
            var argS = (lm[2] !== undefined ? lm[2] : lm[3]).trim();
            var baseV = baseS !== null ? parseFloat(baseS) : 10;
            var argConst = parseConstValue(argS);
            var argLin = argConst === null ? polyToLin(parsePolyCoeffs(argS.replace(/[()]/g, ''))) : null;
            terms.push({ kind: 'log', coef: coef, base: baseV, argRaw: argS,
                         argConst: argConst, argLin: argLin });
          } else if (vm) {
            terms.push({ kind: 'const', v: coef * parseFloat(vm[1]) });
          } else { ok = false; break; }
        }
        if (!ok || !terms.length) return null;
        return { terms: terms, anyLog: anyLog };
      }
      var L = parseSide(lhs);
      var Rr = rhs !== null ? parseSide(rhs) : null;
      if (!L || !L.anyLog || (rhs !== null && !Rr)) return null;
      return { lhs: L, rhs: Rr, hasRhs: rhs !== null };
    }

    function Cnum2str(craw, rhsIsLog) {""")

patch("E6-logexpr-parse", """      // 10b. Bare-argument log equations:""",
r"""      // 10a. Log EXPRESSION arithmetic (Ch 4.3-4.4): eval / expand / equation.
      //      Must run before 10b/10c/10d (it is the general shape).
      {
        const lshape = parseLogExprShape(logSrc);
        if (lshape) {
          const allConst = lshape.lhs.terms.every(t => t.kind === 'const' || t.argConst !== null)
                        && (!lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'const' || t.argConst !== null));
          if (allConst) {
            // numeric evaluation via change of base
            function evalSide(sd) {
              return sd.terms.reduce(function (acc2, t2) {
                if (t2.kind === 'const') return acc2 + t2.v;
                return acc2 + t2.coef * Math.log(t2.argConst) / Math.log(t2.base);
              }, 0);
            }
            const val = evalSide(lshape.lhs) - (lshape.rhs ? evalSide(lshape.rhs) : 0);
            const exactish = Math.abs(Math.round(val) - val) < 1e-9 ? Math.round(val) : Number(val.toFixed(4));
            return { type: 'log_expr', mode: lshape.hasRhs ? 'equation' : 'eval',
                     value: exactish, hasRhs: lshape.hasRhs, raw: logSrc };
          }
          // symbolic: structural expansion (product/quotient/power aware)
          return { type: 'log_expr', mode: 'expand', raw: logSrc, shape: lshape };
        }
      }

      // 10b. Bare-argument log equations:""")

patch("E7-logexpr-tool", """      if (parsed.type === 'sign_rule') {""",
r"""      if (parsed.type === 'log_expr') {
        const dec = (v) => Number(v.toFixed(4));
        const steps = [];
        if (parsed.mode === 'eval') {
          steps.push(`1. Identify the base and argument of each logarithm.`);
          steps.push(`2. Change of base: log_b(A) = ln(A) / ln(b).`);
          steps.push(`3. Evaluate each term and combine.`);
          return {
            title: `🚀 Logarithm Expression Evaluator (Ch 4.3-4.4): ${raw}`,
            solverKey: 'explog',
            params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
            outputVal: `Exact / 4-Decimal Value: <strong>${parsed.value}</strong>`,
            steps
          };
        }
        if (parsed.mode === 'equation') {
          steps.push(`1. Evaluate the log side(s) numerically (change of base).`);
          steps.push(`2. Set the evaluated sides equal and solve the resulting linear equation.`);
          return {
            title: `🚀 Logarithmic Equation (numeric) Solver (Ch 4.5): ${raw}`,
            solverKey: 'explog',
            params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
            outputVal: `Solution: <strong>${parsed.value}</strong>`,
            steps
          };
        }
        // expand mode
        const sh = parsed.shape;
        const lines = [];
        sh.lhs.terms.forEach(function (t) {
          if (t.kind === 'const') { lines.push(`${t.v}`); return; }
          const bb = t.base === Math.E ? 'e' : t.base;
          const flat = t.argRaw.replace(/[()]/g, ' ').replace(/\s+/g, ' ').trim();
          const slash = t.argRaw.indexOf('/');
          let argNote = '';
          if (slash >= 0) {
            argNote = ` (quotient: log of a quotient = difference of logs)`;
          }
          lines.push(`${t.coef === 1 ? '' : t.coef + '·'}log_${bb}(${flat})${argNote}`);
        });
        (sh.rhs ? sh.rhs.terms : []).forEach(function (t) {
          if (t.kind !== 'log') return;
          const bb = t.base === Math.E ? 'e' : t.base;
          lines.push(`= ${t.coef === 1 ? '' : t.coef + '·'}log_${bb}(${t.argRaw.replace(/[()]/g, ' ').replace(/\s+/g, ' ').trim()})`);
        });
        steps.push(`1. Product Rule: log_b(M·N) = log_b M + log_b N.`);
        steps.push(`2. Quotient Rule: log_b(M/N) = log_b M − log_b N.`);
        steps.push(`3. Power Rule: log_b(N^k) = k·log_b N.`);
        steps.push(`4. Structural expansion of each term:`);
        steps.push(`   ${lines.join('<br>&nbsp;&nbsp;&nbsp;')}`);
        return {
          title: `🚀 Logarithm Property Expansion (Ch 4.3): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
          outputVal: `Expression uses Product / Quotient / Power Rules — see expanded form in steps.`,
          steps
        };
      }

      if (parsed.type === 'sign_rule') {""")

# GRAPHABLE set: log_expr needs no drawable curve (tool-only).

P.write_text(src, encoding="utf-8")
print("PATCHED v2:", ", ".join(patches))
py_compile.compile(str(P), doraise=True)
print("compiles OK")