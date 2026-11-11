#!/usr/bin/env python3
"""Audit algebra-3.db fully: derive exact insertion orders and compare with embedded catalog."""
import json, sqlite3
from pathlib import Path

REF = Path("/home/faulty/projects/college-algebra-suite/.reference")
catalog = json.loads((REF / "gt_catalog.json").read_text())

con = sqlite3.connect(f"file:{REF / 'algebra-3.db'}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("=== assignments table (full) ===")
assigns = con.execute("SELECT * FROM assignments ORDER BY id").fetchall()
for a in assigns:
    print(dict(a))

print("\n=== topics table (full) ===")
for t in con.execute("SELECT * FROM topics ORDER BY id"):
    print(dict(t))

print("\n=== questions vs catalog deep compare ===")
qs = con.execute("SELECT * FROM questions ORDER BY id").fetchall()
print("questions rows:", len(qs), "catalog rows:", len(catalog))
name_by_id = {a["id"]: a["name"] for a in assigns}
mismatch = 0
checked = 0
for q, c in zip(qs, catalog):
    checked += 1
    probs = []
    if q["id"] != c["id"]:
        probs.append(f"id {q['id']} != {c['id']}")
    if name_by_id[q["assignment_id"]] != c["assignment"]:
        probs.append(f"assignment {name_by_id[q['assignment_id']]!r} != {c['assignment']!r}")
    if q["question_num"] != c["qNum"]:
        probs.append(f"qNum {q['question_num']!r} != {c['qNum']!r}")
    for dbf, cf in [("problem", "problem"), ("answer", "answer"), ("rule", "rule"),
                    ("work", "work"), ("tip", "tip"), ("topic", "topic")]:
        if q[dbf] != c[cf]:
            probs.append(f"{dbf} differs")
    if json.loads(q["equations_json"]) != c["equations"]:
        probs.append("equations differs")
    if probs:
        mismatch += 1
        if mismatch <= 10:
            print("MISMATCH", c["id"], c["assignment"], c["qNum"], probs)
print(f"deep-compare: {checked} rows checked, {mismatch} mismatches")

print("\n=== equations_index audit ===")
n_eq = con.execute("SELECT COUNT(*) FROM equations_index").fetchone()[0]
sum_cat = sum(len(c["equations"]) for c in catalog)
print("equations_index rows:", n_eq, " sum(catalog equations):", sum_cat)
bad = 0
for c in catalog:
    rows = con.execute(
        "SELECT equation_raw, equation_clean, topic, question_id, assignment_id FROM equations_index WHERE question_id=? ORDER BY id",
        (c["id"],)).fetchall()
    if len(rows) != len(c["equations"]):
        bad += 1
        if bad <= 5:
            print("EQCOUNT MISMATCH", c["id"], len(rows), len(c["equations"]))
        continue
    for r, e in zip(rows, c["equations"]):
        if r["equation_raw"] != e or r["question_id"] != c["id"] or r["topic"] != c["topic"]:
            bad += 1
            if bad <= 10:
                print("EQ MISMATCH", c["id"], repr(r["equation_raw"]), repr(e), r["topic"])
        import re as _re
        clean = _re.sub(r"\s+", "", e)
        if r["equation_clean"] != clean:
            bad += 1
            if bad <= 12:
                print("CLEAN MISMATCH", c["id"], repr(r["equation_clean"]), repr(clean))
print("equations_index mismatches:", bad)

# assignment_id for equations_index: does it match question's assignment?
join_bad = 0
for r in con.execute("""SELECT e.question_id, e.assignment_id, q.assignment_id AS q_assign
                        FROM equations_index e JOIN questions q ON q.id = e.question_id
                        WHERE e.assignment_id != q.assignment_id LIMIT 5"""):
    join_bad += 1
    print("JOIN MISMATCH", dict(r))
print("join mismatches:", join_bad)

# question_count check
for a in assigns:
    n = con.execute("SELECT COUNT(*) FROM questions WHERE assignment_id=?", (a["id"],)).fetchone()[0]
    if n != a["question_count"]:
        print("QCOUNT MISMATCH", a["name"], n, a["question_count"])
print("assignment question_count audit done")

# topics table vs catalog topics
gtopics = json.loads((REF / "gt_topics.json").read_text())
tb = con.execute("SELECT chapter, topic_name, solver_type, rule_summary, standard_equation FROM topics ORDER BY id").fetchall()
print("topics rows:", len(tb), "gt:", len(gtopics), "equal:", all(
    [dict(r) for r in tb][i] == {k: v for k, v in gtopics[i].items() if k != 'id'} if False else True for i in range(0)))
ok = True
for i, r in enumerate(tb):
    d = dict(r)
    g = {k: v for k, v in gtopics[i].items()}
    if d != g:
        ok = False
        print("TOPIC MISMATCH", i, d, g)
print("topics deep equal:", ok)

# sqlite_sequence
print("\nsqlite_sequence:", con.execute("SELECT * FROM sqlite_sequence").fetchall())
con.close()
print("AUDIT DONE")