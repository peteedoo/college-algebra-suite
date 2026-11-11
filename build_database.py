#!/usr/bin/env python3
"""
build_database.py — re-indexes every solved assignment sheet in
assignments/Answers/ into algebra.db and exports the JSON catalog that
sync_dashboard.py embeds into dashboard.html.

Recovered architecture (the original generator was lost; this module
reproduces its output byte-for-byte, verified by test/):

  assignments/Answers/*.md    39 answer sheets — source of truth for all
                              prose fields (problem/answer/rule/work/tip),
                              re-parsed from markdown on every run.
  data/catalog_metadata.json  per-question topic tag + equations index,
                              preserved verbatim from the previous
                              production build (not derivable from prose).
  data/topics.json            19 chapter-level solver reference entries.

Database layout (matches the production algebra.db):
  assignments(id, name, chapter, category, question_count)
  questions(id, assignment_id, question_num, problem, answer, rule,
            work, tip, topic, equations_json)
  equations_index(id, question_id, assignment_id, equation_raw,
                   equation_clean, topic)   [equation_clean = lowercase,
                   whitespace-stripped equation_raw]
  topics(id, chapter, topic_name, solver_type, rule_summary,
         standard_equation)

ID scheme: "Build Understanding" questions number 1..N in name order,
"Pre-work" questions 501..N in name order, general sheets (Quiz/Test)
continue at 786. Catalog JSON is ordered by (chapter, assignment name).
"""

import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ANSWERS_DIR = BASE_DIR / "assignments" / "Answers"
DB_FILE = BASE_DIR / "algebra.db"
DATA_DIR = BASE_DIR / "data"
METADATA_FILE = DATA_DIR / "catalog_metadata.json"
TOPICS_FILE = DATA_DIR / "topics.json"

ANSWERS_SUFFIX = " - Answers.md"

# ---------------------------------------------------------------------------
# Markdown parsing — kept byte-compatible with the dashboard card renderer
# ---------------------------------------------------------------------------

QUESTION_SPLIT_RE = re.compile(
    r'(?=\n\*\s+\*\*Question\s+\d+:?|\n\*\s+\*\*Q\d+:?|\n###\s+\*?\*?Questions?\s+)',
    re.IGNORECASE,
)

TITLE_RE = re.compile(
    r'(?:###\s+\*?\*?(Questions?[^\n*#]+)\*?\*?'
    r'|\*\s+\*?\*?(Question\s+\d+[a-zA-Z0-9\u2013-]*:?|Q\d+:?)\*?\*?)',
    re.IGNORECASE,
)

FIELD_BLOCK_RES = {
    "problem": re.compile(
        r'\*\s+\*\*Problem:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)', re.S),
    "answer": re.compile(
        r'\*\s+\*\*Answers?:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)', re.S),
    # NB: the label part must stay on one line and stop at its first colon
    # (JS `.` never crosses a newline; python re.S would).
    "rule": re.compile(
        r'\*\s+\*\*The (?:Universal )?Rule[^:\n]*:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)', re.S),
    "work": re.compile(
        r'\*\s+\*\*(?:Step-by-Step\s+)?(?:Work|Check|Steps):\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)', re.S),
    "tip": re.compile(
        r'\*\s+\*\*(?:Explanation|Pro-Tip|Watch Out|Tip):\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)', re.S),
}


def chapter_of(assignment_name):
    m = re.search(r'(\d+\.\d+)', assignment_name)
    return m.group(1) if m else "General"


def category_of(assignment_name):
    return "Pre-work" if assignment_name.startswith("Pre-work") else "Build Understanding"


def id_family_of(assignment_name):
    """ID counter family: BU sheets count from 1, Pre-work from 501,
    general sheets (Quiz/Test) from 786 — as recovered from the build."""
    if assignment_name.startswith("Pre-work"):
        return "Pre-work"
    if assignment_name.startswith("Build Understanding"):
        return "Build Understanding"
    return "General"


ID_BASES = {"Build Understanding": 1, "Pre-work": 501, "General": 786}


def parse_answer_sheet(md_text):
    """Parse one answer sheet into a list of question dicts
    {qNum, problem, answer, rule, work, tip} in sheet order."""
    sections = QUESTION_SPLIT_RE.split(md_text)
    questions = []
    for sec in sections[1:]:
        sec = sec.strip()
        if not sec:
            continue
        m = TITLE_RE.match(sec)
        if not m:
            continue
        title = (m.group(1) or m.group(2) or "").strip()
        # Question labels keep no colons: "Question 1: Foo: bar" -> "Question 1 Foo bar"
        q_num = title.replace(": ", " ").strip()
        entry = {"qNum": q_num}
        for field, rx in FIELD_BLOCK_RES.items():
            fm = rx.search(sec)
            entry[field] = fm.group(1).strip() if fm else ""
        questions.append(entry)
    return questions


def clean_equation(raw):
    """SQLite index normal form: drop $/` math delimiters, drop all
    whitespace, lowercase (e.g. '$(x + 2)^2$' -> '(x+2)^2')."""
    return re.sub(r"\s+", "", raw.replace("$", "").replace("`", "")).lower()


# ---------------------------------------------------------------------------
# Catalog construction
# ---------------------------------------------------------------------------

def _load_json(path):
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


def build_catalog():
    """Returns (catalog_rows_in_id_order, assignments_rows, topics_rows).
    catalog rows carry every exported field, in exported key order."""
    metadata = {}
    for e in _load_json(METADATA_FILE):
        metadata[(e["assignment"], e["qNum"])] = e

    assignment_rows = []   # (id, name, chapter, category, question_count)
    catalog = []           # full question dicts, in id order

    sheets = sorted(p.name[:-len(ANSWERS_SUFFIX)]
                   for p in ANSWERS_DIR.glob("*" + ANSWERS_SUFFIX))
    counters = dict(ID_BASES)  # per-family running counters (next id)

    for name in sheets:
        family = id_family_of(name)
        category = category_of(name)
        chapter = chapter_of(name)
        md = (ANSWERS_DIR / (name + ANSWERS_SUFFIX)).read_text(encoding="utf-8")
        sheet_questions = parse_answer_sheet(md)

        assignment_id = len(assignment_rows) + 1
        assignment_rows.append(
            (assignment_id, name, chapter, category, len(sheet_questions)))

        for q in sheet_questions:
            key = (name, q["qNum"])
            if key not in metadata:
                raise KeyError(
                    f"no preserved metadata for {key!r} — new/renamed question?")
            meta = metadata[key]
            qid = counters[family]
            counters[family] += 1
            catalog.append({
                "id": qid,
                "assignment": name,
                "chapter": chapter,
                "category": category,
                "qNum": q["qNum"],
                "problem": q["problem"],
                "answer": q["answer"],
                "rule": q["rule"],
                "work": q["work"],
                "tip": q["tip"],
                "topic": meta["topic"],
                "equations": meta["equations"],
            })

    topics = _load_json(TOPICS_FILE)
    return catalog, assignment_rows, topics


# ---------------------------------------------------------------------------
# SQLite
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    chapter TEXT,
    category TEXT,
    question_count INTEGER
);
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER,
    question_num TEXT,
    problem TEXT,
    answer TEXT,
    rule TEXT,
    work TEXT,
    tip TEXT,
    topic TEXT,
    equations_json TEXT,
    FOREIGN KEY(assignment_id) REFERENCES assignments(id)
);
CREATE TABLE equations_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    assignment_id INTEGER,
    equation_raw TEXT,
    equation_clean TEXT,
    topic TEXT,
    FOREIGN KEY(question_id) REFERENCES questions(id),
    FOREIGN KEY(assignment_id) REFERENCES assignments(id)
);
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter TEXT,
    topic_name TEXT,
    solver_type TEXT,
    rule_summary TEXT,
    standard_equation TEXT
);
CREATE INDEX idx_eq_clean ON equations_index(equation_clean);
CREATE INDEX idx_q_topic ON questions(topic);
"""


def init_database():
    """(Re)create algebra.db from scratch."""
    if DB_FILE.exists():
        DB_FILE.unlink()
    con = sqlite3.connect(DB_FILE)
    con.executescript(SCHEMA)
    con.commit()
    con.close()


def populate_database():
    """Rebuild every table from the answer sheets + preserved metadata."""
    catalog, assignment_rows, topics = build_catalog()
    assign_id_by_name = {r[1]: r[0] for r in assignment_rows}

    con = sqlite3.connect(DB_FILE)
    con.execute("BEGIN")
    for row in assignment_rows:
        con.execute(
            "INSERT INTO assignments (id, name, chapter, category, question_count) "
            "VALUES (?,?,?,?,?)", row)
    for c in catalog:
        con.execute(
            "INSERT INTO questions (id, assignment_id, question_num, problem, "
            "answer, rule, work, tip, topic, equations_json) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (c["id"], assign_id_by_name[c["assignment"]], c["qNum"], c["problem"],
             c["answer"], c["rule"], c["work"], c["tip"], c["topic"],
             json.dumps(c["equations"])))
        for eq in c["equations"]:
            con.execute(
                "INSERT INTO equations_index (question_id, assignment_id, "
                "equation_raw, equation_clean, topic) VALUES (?,?,?,?,?)",
                (c["id"], assign_id_by_name[c["assignment"]], eq,
                 clean_equation(eq), c["topic"]))
    for t in topics:
        con.execute(
            "INSERT INTO topics (chapter, topic_name, solver_type, "
            "rule_summary, standard_equation) VALUES (?,?,?,?,?)",
            (t["chapter"], t["topic_name"], t["solver_type"],
             t["rule_summary"], t["standard_equation"]))
    con.commit()
    con.close()
    return len(catalog), len(assignment_rows), sum(len(c["equations"]) for c in catalog)


def export_json_database():
    """Export the dashboard catalog exactly as sync_dashboard.py expects:
    {"catalog": [...807 questions in (chapter, name, id) order...],
     "topics": [...19 entries...]}"""
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    catalog = []
    for r in con.execute(
            "SELECT q.id, a.name, a.chapter, a.category, q.question_num, "
            "q.problem, q.answer, q.rule, q.work, q.tip, q.topic, q.equations_json "
            "FROM questions q JOIN assignments a ON a.id = q.assignment_id "
            "ORDER BY a.chapter, a.name, q.id"):
        catalog.append({
            "id": r["id"],
            "assignment": r["name"],
            "chapter": r["chapter"],
            "category": r["category"],
            "qNum": r["question_num"],
            "problem": r["problem"],
            "answer": r["answer"],
            "rule": r["rule"],
            "work": r["work"],
            "tip": r["tip"],
            "topic": r["topic"],
            "equations": json.loads(r["equations_json"]),
        })
    topics = []
    for r in con.execute("SELECT chapter, topic_name, solver_type, rule_summary, "
                         "standard_equation FROM topics ORDER BY id"):
        topics.append({
            "chapter": r["chapter"],
            "topic_name": r["topic_name"],
            "solver_type": r["solver_type"],
            "rule_summary": r["rule_summary"],
            "standard_equation": r["standard_equation"],
        })
    con.close()
    return {"catalog": catalog, "topics": topics}


if __name__ == "__main__":
    init_database()
    n_q, n_a, n_e = populate_database()
    db = export_json_database()
    print(f"algebra.db rebuilt: {n_a} assignments, {n_q} questions, "
          f"{n_e} equations, {len(db['topics'])} topics.")