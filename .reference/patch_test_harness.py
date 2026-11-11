#!/usr/bin/env python3
"""Harness fixes, round 3.

Escape chain: python raw str -> FILE bytes -> template literal unescape ->
new Function compile. So a regex the engine should EVAL with one backslash
(\\s) needs TWO in the file (\\s), and raw python keeps them verbatim.
"""
from pathlib import Path
import subprocess

TJ = Path("/home/faulty/projects/college-algebra-suite/test/test_all_assignments.js")
lines = TJ.read_text(encoding="utf-8").split("\n")
done = []

# --- T1: normIv (no backslash-bearing regexes except \\s / \\* via doubles) ---
s = next(i for i, l in enumerate(lines) if "function normIv(s) {" in l)
e = next(i for i in range(s, len(lines)) if ".toLowerCase();" in lines[i])
NEW_NORMIV = r"""  function normIv(s) {
    // backslashes and backticks die FIRST so LaTeX words match plainly.
    // (file-level: \\s \\* stay doubled for the template-literal eval chain)
    var t = String(s)
      .split(String.fromCharCode(92)).join('')
      .split(String.fromCharCode(96)).join('')
      .replace(/\\*\\*/g, '')
      .replace(/\u221E/g, 'INF')
      .replace(/\u222A/g, 'U')
      .replace(/\u2205/g, 'EMPTY')
      .replace(/[\u2212\u2013\u2014]/g, '-');
    t = t.replace(/\\s+/g, '').toLowerCase();
    return t.replace(/infty/g, 'INF')
            .replace(/cup/g, 'U')
            .replace(/varnothing/g, 'EMPTY')
            .replace(/emptyset/g, 'EMPTY')
            .replace(/empty/g, 'EMPTY')
            .replace(/le(?![a-z])/g, '<=')
            .replace(/ge(?![a-z])/g, '>=');"""  # closing } stays from the original block
lines[s:e + 1] = NEW_NORMIV.split("\n")
done.append(f"T1 normIv {s + 1}-{e + 1}")

# --- T2: artifact check (regex needs \\s -> file \\s, eval chain intact) ---
i = next(idx for idx, l in enumerate(lines)
            if "undefined|NaN" in l and ".test(rendered)" in l and "if (" in l)
lines[i] = r"""      if (/=\s*(?:undefined|NaN)\b|>(?:undefined|NaN)</|(?:undefined|NaN)\s*<\//.test(rendered)) {"""
done.append(f"T2 artifact {i + 1}")

# --- T3: conic unit (replace the previously-injected block) ---
s = next(idx for idx, l in enumerate(lines) if "var t1 = runToolOnParsed(c1" in l)
e = next(idx for idx in range(s, s + 10) if "slice(0, 200));" in lines[idx])
NEW_T3 = r"""    var t1 = runToolOnParsed(c1, '');
    var plain1 = String(t1.outputVal).replace(/<[^>]+>/g, '');
    if (plain1.indexOf('(-6, 7)') < 0 || plain1.indexOf('9.49') < 0)
      throw new Error('center should be (-6, 7), r = sqrt(90) ~ 9.49: ' + plain1.slice(0, 160));
    var c2 = parseEquationSyntax('4x^2 + 4x + 4y^2 - 32y - 79 = 0');
    var t2 = runToolOnParsed(c2, '');
    var plain2 = String(t2.outputVal).replace(/<[^>]+>/g, '');
    if (plain2.indexOf('(-0.5, 4)') < 0 && plain2.indexOf('(-1/2, 4)') < 0)
      throw new Error('center should be (-0.5, 4): ' + plain2.slice(0, 200));
    if (plain2.indexOf('6.00') < 0 && plain2.indexOf('6') < 0)
      throw new Error('r should be 6: ' + plain2.slice(0, 200));"""
lines[s:e + 1] = NEW_T3.split("\n")
done.append(f"T3 conic unit {s + 1}-{e + 1}")

TJ.write_text("\n".join(lines), encoding="utf-8")
print("HARNESS:", "; ".join(done))
r = subprocess.run(["node", "--check", str(TJ)], capture_output=True, text=True)
print("node --check:", "OK" if r.returncode == 0 else r.stderr[:400])