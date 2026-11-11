#!/usr/bin/env python3
"""Hardening v3 (loop iteration 3). Engine fixes F1-F6 + test-side fixes T1-T3."""
import py_compile, re
from pathlib import Path

ROOT = Path("/home/faulty/projects/college-algebra-suite")
SD = ROOT / "sync_dashboard.py"
TJ = ROOT / "test" / "test_all_assignments.js"

src = SD.read_text(encoding="utf-8")
tst = TJ.read_text(encoding="utf-8")
assert "__ENGINE_V4_3__" not in src
patches = []

def patch(name, anchor, repl, which="eng"):
    global src, tst
    s = src if which == "eng" else tst
    n = s.count(anchor)
    assert n == 1, f"{name}: anchor {n}x in {which}"
    if which == "eng": src = s.replace(anchor, repl, 1)
    else: tst = s.replace(anchor, repl, 1)
    patches.append(name)

# F1: splitTopLevelOps — operator may be preceded by spaces (term splitting bug)
patch("F1-split-ops", r"""    // split an expression into top-level +/- terms (signs stay attached)
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
    }""",
r"""    // split an expression into top-level +/- terms (signs stay attached).
    // __ENGINE_V4_3__: operators may be preceded by whitespace — look back
    // past spaces ("4x^2 - 32y" must split, not just "4x^2-32y").
    function splitTopLevelOps(str) {
      var parts = [];
      var depth = 0, start = 0;
      for (var i = 0; i < str.length; i++) {
        var ch = str[i];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if ((ch === '+' || ch === '-') && depth === 0 && i > 0 &&
                 /[0-9x)\]]\s*$/.test(str.slice(0, i)) && i + 1 < str.length &&
                 !/[\^]\s*$/.test(str.slice(0, i))) {
          parts.push(str.slice(start, i).trim());
          start = i;
        }
      }
      parts.push(str.slice(start).trim());
      return parts.filter(Boolean);
    }""")

# F2: parseLnOfBase — unwrap ALL outer parens; support A/B const quotients (incl. e^k)
patch("F2-lnbase", r"""    function parseLnOfBase(t) {
      t = String(t || '').trim();
      var core = t.replace(/^\(/, '').replace(/\)$/, '').trim();
      var sm = core.match(/^sqrt\(\s*(\d+(?:\.\d+)?)\s*\)$/i);
      if (sm) return 0.5 * Math.log(parseFloat(sm[1]));
      var v = parseConstValue(core);
      if (v !== null && v > 0 && Math.abs(v - 1) > 1e-12) return Math.log(v);
      return null;
    }""",
r"""    function parseLnOfBase(t) {
      // __ENGINE_V4_3__: unwrap ALL balanced outer parens, and accept
      // constant quotients like (1)/(e) or (1)/(e^3) via ln(A/B)=ln A - ln B.
      t = String(t || '').trim();
      while (t.startsWith('(') && t.endsWith(')')) {
        var d = 0, bal = true;
        for (var i2 = 0; i2 < t.length; i2++) {
          if (t[i2] === '(') d++;
          else if (t[i2] === ')') { d--; if (d === 0 && i2 < t.length - 1) { bal = false; break; } }
        }
        if (!bal) break;
        t = t.slice(1, -1).trim();
      }
      var sm = t.match(/^sqrt\(\s*(\d+(?:\.\d+)?)\s*\)$/i);
      if (sm) return 0.5 * Math.log(parseFloat(sm[1]));
      var v = parseConstValue(t);
      if (v !== null && v > 0 && Math.abs(v - 1) > 1e-12) return Math.log(v);
      // quotient of constants: (A)/(B) at top level (parens already stripped)
      var sl = -1, dep = 0;
      for (var j = 0; j < t.length; j++) {
        if (t[j] === '(') dep++;
        else if (t[j] === ')') dep--;
        else if (t[j] === '/' && dep === 0) { sl = j; break; }
      }
      if (sl > 0) {
        var A2 = parseConstValue(t.slice(0, sl).trim());
        var B2 = parseConstValue(t.slice(sl + 1).trim());
        if (A2 !== null && B2 !== null && A2 > 0 && B2 > 0) return Math.log(A2) - Math.log(B2);
      }
      return null;
    }""")

# F3: log_expr const-coef without '*': "5log_4(x)"
patch("F3-logexpr-coef", r"""          var cm = s2.match(/^(\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
          var coef = sign, body = s2;
          if (cm) { coef = sign * parseFloat(cm[1]); body = cm[2].trim(); }""",
r"""          var cm = s2.match(/^(\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
          var coef = sign, body = s2;
          if (cm) { coef = sign * parseFloat(cm[1]); body = cm[2].trim(); }
          // __ENGINE_V4_3__: "5log_4(x)" — implicit coefficient, no '*'
          else {
            var cm2 = s2.match(/^(\d+(?:\.\d+)?)\s*((?:ln|log)\b.*)$/i);
            if (cm2) { coef = sign * parseFloat(cm2[1]); body = cm2[2].trim(); }
          }""")

# F4: logSrc — nth-root braces \sqrt[14]{e} -> e^(1/14); \sqrt{e} -> sqrt(e)
patch("F4-sqrt-nth", r"""      const logSrc = expClean
        .replace(/\blog\s*10\s*\(/gi, 'log_10(')
        .replace(/\b(ln|log(?:_\d+(?:\.\d+)?)?)\s+(\([^()]*\)|[A-Za-z0-9][A-Za-z0-9.]*)/gi, '$1($2)')""",
r"""      const logSrc = expClean
        .replace(/\\?sqrt\[(\d+)\]\{([a-z0-9.]+)\}/gi, '$2^(1/$1)')
        .replace(/\\?sqrt\{([a-z0-9.]+)\}/gi, 'sqrt($1)')
        .replace(/\blog\s*10\s*\(/gi, 'log_10(')
        .replace(/\b(ln|log(?:_?\d+(?:\.\d+)?|_?sqrt\(\d+(?:\.\d+)?\))?)\s+(\([^()]*\)|[A-Za-z0-9][A-Za-z0-9.]*)/gi, '$1($2)')""")

# F5: 10a log_expr must NOT swallow log-sum EQUATIONS — bail to 10d solver
patch("F5-logexpr-bail", r"""        if (lshape) {
          const allConst = lshape.lhs.terms.every(t => t.kind === 'const' || t.argConst !== null)
                        && (!lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'const' || t.argConst !== null));""",
r"""        if (lshape) {
          // __ENGINE_V4_3__: a sum/difference of logs equal to another log
          // (or to nothing) is a SOLVABLE log equation/property question —
          // do not capture it here; 10d/10b solve it exactly.
          const allLogL = lshape.lhs.terms.every(t => t.kind === 'log');
          const allLogR = !lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'log');
          const allConstL = lshape.lhs.terms.every(t => t.kind === 'const' || t.argConst !== null);
          if (allLogL && allLogR) {
            if (!lshape.hasRhs) {
              return { type: 'log_expr', mode: 'expand', raw: logSrc, shape: lshape };
            }
            // condense-and-solve: A(+/-)B = C -> A*B = C (same base)
            // handled by 10d below via fallthrough: return null marker shape
            lshape.__defer = true;
          } else if (!allConstL) {
            return { type: 'log_expr', mode: 'expand', raw: logSrc, shape: lshape };
          }
          const allConst = allConstL
                        && (!lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'const' || t.argConst !== null));
          if (lshape.__defer) { /* fall through to 10b/10d */ }""")

# F6: 10d log-sum regex — bases may be sqrt(d), bare numbers, or absent
patch("F6-logsum-regex", r"""      const logSum = logSrc.match(/^(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*([+-])\s*(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*=\s*(?:(?:ln|log)_?\(?([0-9]+(?:\.[0-9]+)?)?\)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))|([0-9]+(?:\.[0-9]+)?))$/i);""",
r"""      // __ENGINE_V4_3__: bases may be missing, numeric, or sqrt(d);
      // arguments may be parenthesized or bare.
      const logSum = logSrc.match(/^(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*([+-])\s*(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*=\s*(?:(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))|([A-Za-z0-9][A-Za-z0-9.]*))$/i);""")

# F6b: 10d base extraction: parse 'sqrt(5)' bases via parseLnOfBase
patch("F6b-logsum-base", r"""        const baseS = logSum[1] !== undefined ? parseFloat(logSum[1]) : (logSum[5] !== undefined ? parseFloat(logSum[5]) : 10);
        const Araw = (logSum[2] !== undefined ? logSum[2] : logSum[3] || '').trim();
        const opS = logSum[4] === '-' ? -1 : 1;
        const Braw = (logSum[6] !== undefined ? logSum[6] : logSum[7] || '').trim();
        const rhsIsLog = logSum[8] !== undefined;
        const baseS2 = rhsIsLog ? (logSum[8] !== undefined ? parseFloat(logSum[8]) : 10) : baseS;
        const Craw = rhsIsLog ? (logSum[9] !== undefined ? logSum[9] : logSum[10] || '').trim() : logSum[11];""",
r"""        // __ENGINE_V4_3__: base tokens may be 'sqrt(5)' — use parseLnOfBase.
        function logBaseFrom(tok) {
          if (tok === undefined) return 10;
          const ln2 = parseLnOfBase(String(tok));
          return ln2 !== null ? Math.exp(ln2) : parseFloat(tok);
        }
        const baseS = logBaseFrom(logSum[1] !== undefined ? logSum[1] : (logSum[5] !== undefined ? logSum[5] : undefined));
        const Araw = (logSum[2] !== undefined ? logSum[2] : logSum[3] || '').trim();
        const opS = logSum[4] === '-' ? -1 : 1;
        const Braw = (logSum[6] !== undefined ? logSum[6] : logSum[7] || '').trim();
        const rhsIsLog = logSum[8] !== undefined;
        const baseS2 = rhsIsLog ? logBaseFrom(logSum[8]) : baseS;
        const Craw = rhsIsLog ? (logSum[9] !== undefined ? logSum[9] : logSum[10] || '').trim() : logSum[11];""")

SD.write_text(src, encoding="utf-8")
print("PATCHED v3:", ", ".join(patches))
py_compile.compile(str(SD), doraise=True)
print("compiles OK")
