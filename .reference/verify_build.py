#!/usr/bin/env python3
"""Verify build_database.py reproduces the production build EXACTLY."""
import json, sqlite3, sys
from pathlib import Path

PROJ = Path("/home/faulty/projects/college-algebra-suite")
sys.path.insert(0, str(PROJ))
import build_database as bd

REF_HTML = Path("/home/faulty/.hermes/attachments/dashboard-3.html")
REF_DB = Path("/home/faulty/.hermes/attachments/algebra-3.db")


def raw_embedded(marker):
    html = REF_HTML.read_text(encoding="utf-8")
    tag = f'<script id="{marker}" type="application/json">'
    i = html.find(tag)
    j = html.find("</script>", i)
    return html[i + len(tag):j].strip()


raw_answers = raw_embedded("embedded-data")
raw_dbjson = raw_embedded("database-data")

# 1. rebuild
bd.init_database()
n_q, n_a, n_e = bd.populate_database()
export = bd.export_json_database()
print(f"rebuilt: {n_a} assignments, {n_q} questions, {n_e} equations")

# 2. answers round-trip via sync_dashboard.get_all_answers
import sync_dashboard as sd
answers = sd.get_all_answers()
print("get_all_answers == embedded:", json.dumps(answers) == raw_answers,
      f"({len(answers)} sheets)")

# 3. catalog export byte-equality
my_dbjson = json.dumps(export, ensure_ascii=True)
print("export json.dumps == embedded database-data:", my_dbjson == raw_dbjson)
if my_dbjson != raw_dbjson:
    gt = json.loads(raw_dbjson)
    mine = export
    print("  catalog len:", len(mine["catalog"]), "gt:", len(gt["catalog"]))
    nbad = 0
    for a, b in zip(mine["catalog"], gt["catalog"]):
        if a != b:
            nbad += 1
            if nbad <= 8:
                diffs = [k for k in b if a.get(k) != b[k]]
                print("   DIFF", b["id"], b["assignment"], b["qNum"], "fields:", diffs)
                for k in diffs:
                    if k not in ("equations",):
                        print("     mine:", repr(a.get(k))[:220])
                        print("     gt  :", repr(b[k])[:220])
    print("  topics equal:", mine["topics"] == gt["topics"])
    print("  total diffs:", nbad)

# 4. SQLite content equality vs production db
def dump(db_path):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    out = {}
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name"):
        rows = con.execute(f'SELECT * FROM "{t}" ORDER BY rowid').fetchall()
        out[t] = rows
    con.close()
    return out

mine_d = dump(PROJ / "algebra.db")
gt_d = dump(REF_DB)
for t in sorted(set(mine_d) | set(gt_d)):
    if t not in mine_d or t not in gt_d:
        print(f"TABLE MISSING: {t}")
        continue
    same = mine_d[t] == gt_d[t]
    print(f"table {t}: {len(mine_d[t])} vs {len(gt_d[t])} rows, equal={same}")
    if not same and len(mine_d[t]) == len(gt_d[t]):
        n = 0
        for a, b in zip(mine_d[t], gt_d[t]):
            if a != b:
                n += 1
                if n <= 5:
                    print("   ROW DIFF:", str(a)[:300])
                    print("        GT  :", str(b)[:300])
        print("   row diffs:", n)

# 5. equations_clean rule check against gt
bad_clean = 0
con = sqlite3.connect(f"file:{REF_DB}?mode=ro", uri=True)
for raw, clean in con.execute("SELECT equation_raw, equation_clean FROM equations_index"):
    import re
    if clean != re.sub(r"\s+", "", raw).lower():
        bad_clean += 1
print("clean rule mismatches in GT db:", bad_clean)
con.close()
print("VERIFY DONE")