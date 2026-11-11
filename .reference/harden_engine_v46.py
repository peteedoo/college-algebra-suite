#!/usr/bin/env python3
"""Engine v4.6 (take 2): parameter-form log equations."""
from pathlib import Path
import py_compile, re

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")
assert "__ENGINE_V4_6__" not in src
done = []

def patch(tag, anchor, repl):
    global src
    n = src.count(anchor)
    assert n == 1, f"{tag}: {n} hits"
    src = src.replace(anchor, repl, 1)
    done.append(tag)

A1 = "      const logSrc = expClean\n"
patch("F1-flip", A1, A1 +
      "        // __ENGINE_V4_6__: reversed parameter forms 'K = log_b M' -> 'log_b M = K'\n"
      "        .replace(/^([+-]?\\d+(?:\\.\\d+)?)\\s*=\\s*((?:ln|log)\\b[\\s\\S]*)$/i, '$2 = $1')\n")

A2 = ("      const logMatch = logSrc.match(/^([+-]?\\d*\\.?\\d*)?\\s*\\*?\\s*"
      "(ln|log(?:_(\\d+(?:\\.\\d+)?))?)\\s*\\(\\s*([^()]+?)\\s*\\)\\s*"
      "([+-]\\s*\\d+(?:\\.\\d+)?)?(?:\\s*=\\s*(.+))?$/i);")
BLOCK = """      // 10a0. __ENGINE_V4_6__: parameter-form log equations — solve for
      //      a letter base, a letter argument, or a letter value; verify
      //      all-numeric statements like log_sqrt(5) 625 = 8.
      const logParam = logSrc.match(/^log[_](\\d+(?:\\.\\d+)?|sqrt\\(\\d+(?:\\.\\d+)?\\)|[a-z])\\s*(?:\\(\\s*([^()]+?)\\s*\\)|([A-Za-z0-9][A-Za-z0-9.]*))\\s*=\\s*([0-9]+(?:\\.[0-9]+)?|[a-z])\\s*$/i);
      if (logParam) {
        const bpRaw = logParam[1];
        const bpVal = /^\\d/.test(bpRaw) ? parseFloat(bpRaw)
                    : /^sqrt/i.test(bpRaw) ? Math.sqrt(parseFloat(bpRaw.replace(/^sqrt\\(|\\)$/g, '')))
                    : null;
        const apRaw = String(logParam[2] !== undefined ? logParam[2] : logParam[3]).trim();
        const apVal = /^[a-z]$/i.test(apRaw) ? null : parseConstValue(apRaw);
        const rpRaw = String(logParam[4]).trim();
        const rpVal = /^[a-z]$/i.test(rpRaw) ? null : parseFloat(rpRaw);
        if (bpVal !== null && apVal === null && /^[a-z]$/i.test(apRaw) && rpVal !== null) {
          // log_b(M) = K  ->  M = b^K
          return { type: 'log_eq2', roots: [Math.pow(bpVal, rpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpVal, kind: 'param-arg' };
        } else if (bpVal === null && /^[a-z]$/i.test(bpRaw) && apVal !== null && rpVal !== null && rpVal !== 0) {
          // log_b(K) = C  ->  b = K^(1/C)
          return { type: 'log_eq2', roots: [Math.pow(apVal, 1 / rpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpVal, kind: 'param-base' };
        } else if (bpVal !== null && bpVal > 0 && bpVal !== 1 && apVal !== null && apVal > 0 && rpVal === null && /^[a-z]$/i.test(rpRaw)) {
          // log_b(K) = y  ->  y = ln K / ln b
          return { type: 'log_eq2', roots: [Math.log(apVal) / Math.log(bpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpRaw, kind: 'param-value' };
        } else if (bpVal !== null && bpVal > 0 && bpVal !== 1 && apVal !== null && apVal > 0 && rpVal !== null) {
          // all numeric: verify ln K / ln b == rhs
          const lhsV = Math.log(apVal) / Math.log(bpVal);
          if (Math.abs(lhsV - rpVal) < 1e-9) {
            return { type: 'log_eq2', roots: [rpVal], baseExpr: bpRaw,
                     argExpr: apRaw, rhs: rpVal, kind: 'verify' };
          }
        }
      }

"""
patch("F2-param", A2, BLOCK + A2)

P.write_text(src, encoding="utf-8")
print("PATCHED v4.6:", ", ".join(done))
py_compile.compile(str(P), doraise=True)
print("compiles OK")