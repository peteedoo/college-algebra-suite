#!/usr/bin/env python3
"""Engine v4.5: splitTopLevelOps letter class + E3 power-aware bare-arg wrap."""
from pathlib import Path
import py_compile

P = Path("/home/faulty/projects/college-algebra-suite/sync_dashboard.py")
src = P.read_text(encoding="utf-8")
assert "__ENGINE_V4_5__" not in src
done = []

def patch(tag, anchor, repl):
    global src
    n = src.count(anchor)
    assert n == 1, f"{tag}: {n} hits"
    src = src.replace(anchor, repl, 1)
    done.append(tag)

# Fix 1: allow splits after ANY variable letter (y, z, t, ...), not just x
patch("S1-splitclass",
      r"""`                 /[0-9x)\]]\s*$/.test(str.slice(0, i)) && i + 1 < str.length &&""",
      r"""`                 // __ENGINE_V4_5__: any variable letter may precede an operator
                 /[0-9a-z)\]]\s*$/i.test(str.slice(0, i)) && i + 1 < str.length &&""")

# Fix 2: E3-style bare-arg wrap must not cut numeric powers off their base:
# 'log 10^(-7)' must become log(10^(-7)), not log(10)^(-7)
patch("S2-barearg-power",
      r"""`.replace(/\b(ln|log(?:_?\d+(?:\.\d+)?|_?sqrt\(\d+(?:\.\d+)?\))?)\s+(\([^()]*\)|[A-Za-z0-9][A-Za-z0-9.]*)/gi, '$1($2)')""",
      r"""`.replace(/\b(ln|log(?:_?\d+(?:\.\d+)?|_?sqrt\(\d+(?:\.\d+)?\))?)\s+(\([^()]*\)|[A-Za-z0-9][A-Za-z0-9.]*(?:\^\(?[+-]?\d+(?:\.\d+)?\)?)?)/gi, '$1($2)')`""")

P.write_text(src, encoding="utf-8")
print("PATCHED v4.5:", ", ".join(done))
py_compile.compile(str(P), doraise=True)
print("compiles OK")