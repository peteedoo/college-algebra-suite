#!/usr/bin/env python3
"""One-time RECOVERY tool (kept out of the shipped repo).

The original build_database.py was lost; the authoritative catalog metadata
(topic tags + equations indexes per question) lives only inside the current
production build (dashboard-3.html) and its SQLite db (algebra-3.db).

This script:
  1. Extracts the 39 answer-sheet markdown files from the embedded JSON.
  2. Dumps the catalog/topics ground truth into .reference/ for verification.
  3. Emits data/catalog_metadata.json (topic + equations per question) which
     build_database.py merges with freshly-parsed markdown fields.
  4. Audits the SQLite schema of the current db.
"""
import json, re, sqlite3, sys
from pathlib import Path

SRC = Path("/home/faulty/.hermes/attachments/dashboard-3.html")
DB_SRC = Path("/home/faulty/.hermes/attachments/algebra-3.db")
PROJ = Path("/home/faulty/projects/college-algebra-suite")
ANS = PROJ / "assignments" / "Answers"
REF = PROJ / ".reference"
DATA = PROJ / "data"


def extract_block(html, marker):
    start_tag = f'<script id="{marker}" type="application/json">'
    i = html.find(start_tag)
    if i < 0:
        sys.exit(f"FATAL: marker {marker} not found")
    j = html.find("</script>", i)
    return html[i + len(start_tag):j].strip()


html = SRC.read_text(encoding="utf-8")
answers = json.loads(extract_block(html, "embedded-data"))
dbjs = json.loads(extract_block(html, "database-data"))
catalog, topics = dbjs["catalog"], dbjs["topics"]

print("answer sheets:", len(answers))
print("catalog questions:", len(catalog))
print("topic entries:", len(topics))
print("catalog field order:", list(catalog[0].keys()))
print("topic field order:", list(topics[0].keys()))

# 1. write the answer sheets
ANS.mkdir(parents=True, exist_ok=True)
for k, v in answers.items():
    (ANS / k).write_text(v, encoding="utf-8")
print("wrote", len(answers), "md files to", ANS)

# round-trip: re-read in get_all_answers order and compare
def sort_key(path_obj):
    name = path_obj.name
    m = re.search(r'(\d+)\.(\d+)', name)
    if m:
        ch, sec = int(m.group(1)), int(m.group(2))
        kind = 0 if "Build Understanding" in name else (1 if "Pre-work" in name else 2)
        return (0, ch, sec, kind, name)
    return (1, 99, 99, 0, name)

rt = {}
for f in sorted(ANS.iterdir(), key=sort_key):
    if f.suffix == ".md":
        rt[f.name] = f.read_text(encoding="utf-8")
print("round-trip identical to embedded:", rt == answers)
print("key order identical:", list(rt) == list(answers))

# 2. ground truth dumps
(REF / "gt_catalog.json").write_text(json.dumps(catalog, ensure_ascii=True), encoding="utf-8")
(REF / "gt_topics.json").write_text(json.dumps(topics, ensure_ascii=True), encoding="utf-8")

# 3. metadata sidecar (what build_database.py cannot derive from prose)
meta = [{"assignment": c["assignment"], "qNum": c["qNum"],
         "topic": c["topic"], "equations": c["equations"]} for c in catalog]
(DATA / "catalog_metadata.json").write_text(
    json.dumps(meta, ensure_ascii=True, indent=1) + "\n", encoding="utf-8")
print("metadata sidecar:", len(meta), "entries")

# catalog ordering audit
seen = []
for c in catalog:
    if c["assignment"] not in seen:
        seen.append(c["assignment"])
print("catalog assignment order:")
for a in seen:
    n = sum(1 for c in catalog if c["assignment"] == a)
    cid = min(c["id"] for c in catalog if c["assignment"] == a)
    print(f"   ids {cid:>4}..{cid + n - 1:>4} ({n:>2} q)  {a}")

ids = [c["id"] for c in catalog]
print("ids: min", min(ids), "max", max(ids), "unique:", len(set(ids)) == len(ids))

# 4. current db schema audit
con = sqlite3.connect(f"file:{DB_SRC}?mode=ro", uri=True)
for row in con.execute("SELECT type, name, sql FROM sqlite_master ORDER BY type DESC, name"):
    print(f"DB {row[0]}: {row[1]}")
    if row[2]:
        print("   ", " ".join(row[2].split()))
for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    n = con.execute(f"SELECT COUNT(*) FROM \"{t}\"").fetchone()[0]
    cols = [d[1] for d in con.execute(f"PRAGMA table_info(\"{t}\")")]
    print(f"table {t}: rows={n} cols={cols}")
    for r in con.execute(f"SELECT * FROM \"{t}\" LIMIT 2"):
        print("   sample:", str(r)[:400])
con.close()
print("DONE")