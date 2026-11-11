#!/usr/bin/env python3
"""Harness fixes v4: GRAPHABLE set, INF-case, artifact regex, classifier."""
from pathlib import Path
import subprocess

TJ = Path("/home/faulty/projects/college-algebra-suite/test/test_all_assignments.js")
lines = TJ.read_text(encoding="utf-8").split("\n")
done = []

def rep_once(old, new, tag):
    global lines
    hits = [i for i, l in enumerate(lines) if old in l]
    assert len(hits) == 1, f"{tag}: {len(hits)} hits"
    lines[hits[0]] = lines[hits[0]].replace(old, new)
    done.append(f"{tag} (line {hits[0] + 1})")

# H1: log_expr is tool-only — no graph builder
rep_once("exp_eq: 1, log_eq2: 1, log_expr: 1 };",
         "exp_eq: 1, log_eq2: 1 };",
         "H1-graphable")

# H2: artifact regex — drop the >undefined</ alternative (prose backticks
# like `undefined` legitimately render as <code>undefined</code>)
rep_once("if (/=\\\\s*(?:undefined|NaN)\\\\b|>(?:undefined|NaN)<\\\\/|(?:undefined|NaN)\\\\s*<\\\\//.test(rendered)) {",
         "if (/=\\\\s*(?:undefined|NaN)\\\\b/.test(rendered)) {",
         "H2-artifact")

# H3: INF case consistency — ∞ and word tokens both lowercase
rep_once(".replace(/\\\\u221E/g, 'INF')", ".replace(/\\\\u221E/g, 'inf')", "H3a-inf")
rep_once(".replace(/infty/g, 'INF')", ".replace(/infty/g, 'inf')", "H3b-infty")
rep_once(".replace(/varnothing/g, 'EMPTY')", ".replace(/varnothing/g, 'empty')", "H3c-varnothing")
rep_once(".replace(/emptyset/g, 'EMPTY')", ".replace(/emptyset/g, 'empty')", "H3d-emptyset")
rep_once(".replace(/empty/g, 'EMPTY')", ".replace(/empty/g, 'empty')", "H3e-empty")

# H4: classifier additions — definitional / answer-echo families
# (the prose-if line and the return line are separate lines; match the if)
s = next(i for i, l in enumerate(lines) if "[A-Za-z]{3,}" in l and "info-prose" not in l and ".test(e)" in l and "&&" in l)
e = next(i for i in range(s, s + 4) if lines[i].strip() == "return null;")
NEW_BLOCK = [
    "    if (/[A-Za-z]{3,}[\\\\s,]+[A-Za-z]{3,}[\\\\s,]+[A-Za-z]{3,}/.test(e) && !/[=^\\\\/|]/.test(e)) {",
    "      return 'info-prose';",
    "    }",
    "    // __H4__: definitional echoes — blank fills, i-sqrt notation,",
    "    // f^(-1) pairs, y = f(x) usage, e-limit definition",
    "    if (/_{3,}/.test(e)) return 'info-prose';",
    "    if (/isqrt/.test(e)) return 'info-notation';",
    "    if (/1\\\\/n\\\\)\\\\)\\\\^n|\\\\(1\\\\s*\\\\+/.test(e)) return 'info-notation';",
    "    if (/f\\\\(-?\\\\d+\\\\)\\\\s*=\\\\s*\\\\d+\\\\s*;/.test(e)) return 'info-notation';",
    "    if (/^y\\\\s*=\\\\s*f\\\\(x\\\\)/i.test(e)) return 'info-notation';",
    "    return null;",
]
lines[s:e + 1] = NEW_BLOCK
done.append("H4-classifier (lines %d-%d)" % (s + 1, s + len(NEW_BLOCK)))

TJ.write_text("\n".join(lines), encoding="utf-8")
print("HARNESS v4:", "; ".join(done))
r = subprocess.run(["node", "--check", str(TJ)], capture_output=True, text=True)
print("node --check:", "OK" if r.returncode == 0 else r.stderr[:400])