#!/usr/bin/env python3
"""Engine hardening v4 (final loop iteration). Marker __ENGINE_V4_4__.

Fixes from probe2:
  G1 parseConstValue: strip balanced outer parens of ANY single token (so
     '(e)' -> e -> Math.E), and support numeric powers b^k (10^(-7)).
  G2 10a log_expr routing: eval when all-constant; DEFER to the 10d log-sum
     solver when both sides are pure logs with an rhs; expand otherwise.
     (v3's early expand-on-no-rhs wrongly captured log_2 16.)
  G3 parseLogExprShape coefficient regex: 'log\\b' fails before '_' —
     accept ln|log followed by [_ (].
"""
import py_compile
from pathlib import Path

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")
assert "__ENGINE_V4_4__" not in src and "__ENGINE_V4_2__" in src
patches = []

def patch(name, anchor, repl):
    global src
    n = src.count(anchor)
    assert n == 1, f"{name}: anchor {n}x"
    src = src.replace(anchor, repl, 1)
    patches.append(name)

# --- G1: parseConstValue — general unwrap + numeric powers -------------------
OLD = """    function parseConstValue(t) {
      t = String(t == null ? '' : t).replace(/\\s+/g, '');
      if (!t) return null;
      // unwrap parens around pure numeric/rational content: ((1)/(5)) -> 1/5
      if (/^[()+*/\\d.\\-]+$/.test(t)) t = t.replace(/[()]/g, '');
      if (/^e$/i.test(t)) return Math.E;
      var em = t.match(/^e\\^(-?\\d+(?:\\.\\d+)?)$/i);
      if (em) return Math.pow(Math.E, parseFloat(em[1]));
      if (/^[+-]?\\d+(?:\\.\\d+)?$/.test(t)) return parseFloat(t);
      var rf = t.match(/^([+-]?\\d+(?:\\.\\d+)?)\\/([+-]?\\d+(?:\\.\\d+)?)$/);
      if (rf && parseFloat(rf[2]) !== 0) return parseFloat(rf[1]) / parseFloat(rf[2]);
      return null;
    }"""
NEW = """    function parseConstValue(t) {
      // __ENGINE_V4_4__: strip ALL balanced outer paren pairs first (any
      // content), then accept e, e^k, b^k numeric powers, ints and A/B.
      t = String(t == null ? '' : t).replace(/\\s+/g, '');
      if (!t) return null;
      while (t.startsWith('(') && t.endsWith(')')) {
        var d = 0, bal = true;
        for (var i = 0; i < t.length; i++) {
          if (t[i] === '(') d++;
          else if (t[i] === ')') { d--; if (d === 0 && i < t.length - 1) { bal = false; break; } }
        }
        if (!bal) break;
        t = t.slice(1, -1).replace(/^\\s+|\\s+$/g, '');
        if (!t) return null;
      }
      if (/^e$/i.test(t)) return Math.E;
      var em = t.match(/^e\\^\\(?([+-]?\\d+(?:\\.\\d+)?)\\)?$/i);
      if (em) return Math.pow(Math.E, parseFloat(em[1]));
      // numeric power b^k with optional parens: 10^(-7), 10^-7, (10)^3
      var pm = t.match(/^([+-]?\\d+(?:\\.\\d+)?)\\^\\(?([+-]?\\d+(?:\\.\\d+)?)\\)?$/);
      if (pm) { var bb = parseFloat(pm[1]), kk = parseFloat(pm[2]); return Math.pow(bb, kk); }
      if (/^[+-]?\\d+(?:\\.\\d+)?$/.test(t)) return parseFloat(t);
      var rf = t.match(/^([+-]?\\d+(?:\\.\\d+)?)\\/([+-]?\\d+(?:\\.\\d+)?)$/);
      if (rf && parseFloat(rf[2]) !== 0) return parseFloat(rf[1]) / parseFloat(rf[2]);
      return null;
    }"""
patch("G1-constvalue", OLD, NEW)

# --- G2: 10a routing — eval / defer / expand ----------------------------------
OLD2 = """        if (lshape) {
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
          if (lshape.__defer) { /* fall through to 10b/10d */ }
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
        }"""
NEW2 = """        if (lshape) {
          // __ENGINE_V4_4__: routing order matters.
          //  (a) both sides pure logs AND an rhs -> log-sum EQUATION:
          //      defer to the 10d solver (condense A(+/-)B = C -> A*B = C).
          //  (b) every argument a constant -> numeric EVAL via change of base.
          //  (c) otherwise -> symbolic structural EXPAND (product/quotient).
          const allLogL = lshape.lhs.terms.every(t => t.kind === 'log');
          const allLogR = !lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'log');
          const allConst = lshape.lhs.terms.every(t => t.kind === 'const' || t.argConst !== null)
                        && (!lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'const' || t.argConst !== null));
          if (allLogL && allLogR && lshape.hasRhs) {
            // fall through to 10d
          } else if (allConst) {
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
          } else if (!lshape.hasRhs) {
            return { type: 'log_expr', mode: 'expand', raw: logSrc, shape: lshape };
          }
          // mixed log + const with rhs: fall through to 10d as well
        }"""
patch("G2-logexpr-routing", OLD2, NEW2)

# --- G3: parseLogExprShape coefficient regex \b before '_' -------------------
OLD3 = """          else {
            var cm2 = s2.match(/^(\\d+(?:\\.\\d+)?)\\s*((?:ln|log)\\b.*)$/i);
            if (cm2) { coef = sign * parseFloat(cm2[1]); body = cm2[2].trim(); }
          }"""
NEW3 = """          else {
            // __ENGINE_V4_4__: \\b fails before '_' — accept [_ ( after log
            var cm2 = s2.match(/^(\\d+(?:\\.\\d+)?)\\s*((?:ln|log)[_(].*)$/i)
                    || s2.match(/^(\\d+(?:\\.\\d+)?)\\s*((?:ln|log)\\s.*)$/i);
            if (cm2) { coef = sign * parseFloat(cm2[1]); body = cm2[2].trim(); }
          }"""
patch("G3-logexpr-coef", OLD3, NEW3)

P.write_text(src, encoding="utf-8")
print("PATCHED v4:", ", ".join(patches))
py_compile.compile(str(P), doraise=True)
print("compiles OK")