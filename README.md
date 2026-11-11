# MAT 1340 College Algebra — Database & Universal Equation Solver

A fully offline, single-file study dashboard for a complete College Algebra
course: **39 answer sheets, 807 Pearson/MyMathLab-aligned questions, and a
live equation engine** that parses, solves, and graphs typed input in real
time. Zero CDN dependencies — the whole course ships in one HTML file.

**Live demo (GitHub Pages):** https://peteedoo.github.io/college-algebra-suite/

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     build pipeline (deterministic)                 │
│                                                                    │
│  assignments/Answers/*.md  ──┐                                     │
│  (39 answer sheets)          │                                     │
│                              ▼                                     │
│                    ┌──────────────────┐      ┌───────────────┐     │
│                    │ build_database.py │─────▶│   algebra.db  │     │
│                    │ (SQLite builder)  │      │ 39 assignmts │     │
│                    └────────┬─────────┘      │ 807 questions│     │
│                             │                │ 8058 eq-index│     │
│                             ▼                │ 19 topics     │     │
│                    ┌──────────────────┐      └───────────────┘     │
│                    │ sync_dashboard.py│──▶ dashboard.html (1.6 MB)  │
│                    │ (single-file gen) │   ┌──────────────────────┐│
│                    └──────────────────┘   │ embedded answers JSON ││
│                             ▲             │ embedded database JSON│
│                             │             │ + full JS math engine ││
│  test/test_all_assignments.js┘             │ + graphing canvas    ││
│  (headless JSC engine suite)               └──────────────────────┘│
└────────────────────────────────────────────────────────────────────┘
```

- **`build_database.py`** — parses every answer sheet into a relational
  schema (assignments, questions, equations_index, topics). Rebuilds
  `algebra.db` row-for-row identical to the reference database.
- **`sync_dashboard.py`** — regenerates `dashboard.html`: bundles all
  sheets + the database export into a self-contained page with the
  universal equation engine (AST parser, 20+ solver tools, canvas
  graphing, inline editing, catalog search).
- **`test/test_all_assignments.js`** — headless Node suite that drives the
  real engine (extracted from `dashboard.html`) across all 807 questions
  plus boundary units (open-interval poles, exact fractions, log domains,
  conic general form, log-sum equations with extraneous-root filtering).

## Curriculum sitemap (Chapters 1.1 – 9.5+)

| Ch | Build Understanding | Pre-work | Qs |
|----|---------------------|----------|----|
| 1.3 | Complex Numbers | Complex Numbers | 42 |
| 1.8 | Absolute Value Inequalities | — | 14 |
| 2.2 | Circles | Circles | 32 |
| 3.1 | Quadratic Functions & Models | Quadratic Functions | 59 |
| 3.2 | Synthetic Division | Synthetic Division | 39 |
| 3.3 | Zeros of Polynomial Functions | Zeros of Polynomial Functions | 37 |
| 3.4 | Polynomial Graphs & Models | Polynomial Graphs & Applications | 49 |
| 3.5 | Rational Functions | Rational Functions Graphs & Applications | 62 |
| 3.6 | Polynomial & Rational Inequalities | Polynomial & Rational Inequalities | 44 |
| 4.1 | Inverse Functions | Inverse Functions | 56 |
| 4.2 | Exponential Functions | Exponential Functions | 75 |
| 4.3 | Logarithmic Functions | Logarithmic Functions | 54 |
| 4.4 | Evaluating Logs & Change of Base | Change of Base Theorem | 38 |
| 4.5 | Exponential & Logarithmic Equations | Exponential & Logarithmic Equations | 41 |
| 4.6 | Exponential Growth & Decay | Growth & Decay | 22 |
| 9.1 | Systems of Linear Equations | Systems of Linear Equations | 28 |
| 9.5 | Nonlinear Systems | Non-Linear Systems | 23 |
| 10.2 | Ellipses | Ellipses | 35 |
| 10.3 | Hyperbolas | Hyperbolas | 35 |
| — | Quiz 2 · Test 2 Study Guide | | 22 |
| | **39 sheets total** | | **807** |

## Run locally (100% offline)

```bash
python3 sync_dashboard.py     # rebuilds algebra.db + dashboard.html (exit 0)
node test/test_all_assignments.js   # optional: full engine suite
```

Then open the dashboard directly — no server needed:

```
file:///home/you/college-algebra-suite/dashboard.html
```

Everything runs in the page: type any equation (`x^2 - 5x + 6 = 0`,
`log_2(x + 3) = 4`, `(x^2 + 12x) + (y^2 - 14y) = 5`, `y = x^2 - 4, y = 2x - 1`)
into the omni-search bar, or edit the numbers inside any question card —
answers, work steps, and graphs update live without a reload.

## Repository layout

```
├── dashboard.html            # generated single-file app (the deliverable)
├── index.html                # Pages entry point → dashboard.html
├── sync_dashboard.py         # generator (source of truth for the engine)
├── build_database.py         # SQLite builder (row-exact reproduction)
├── algebra.db                # 39 assignments · 807 questions · queryable
├── requirements.txt          # stdlib-only; documents tested env
├── assignments/Answers/      # 39 answer sheets (.md)
├── data/                     # catalog metadata + topics
├── test/                     # headless engine suite (node)
└── .reference/               # original materials + recovery tooling
```

## Engine coverage (verified by the headless suite)

- 807 questions: **627 AST-solved**, 14 compiled-graph, 165 conceptual/
  informational (prose, echo answers, notation, applets) — 3 documented
  residuals (multi-variable symbolic log expansions, one multi-part
  decibel formula) listed in the suite's failure report.
- Boundary guarantees: rational-inequality poles never produce closed
  brackets; exact simplified fractions and radicals (not floats); log-sum
  equations reject extraneous roots via domain checks; conic general form
  `4x² + 4x + 4y² − 32y − 79 = 0` → center (−0.5, 4), r = 6.

## Deployment (GitHub Pages)

```bash
git remote add origin git@github.com:<owner>/college-algebra-suite.git
git push -u origin main
# Settings → Pages → Deploy from branch → main / (root)
```

`index.html` redirects to `dashboard.html`, so the Pages URL serves the
app immediately. The dashboard has zero external requests, so the hosted
copy is byte-for-byte as capable as the offline one.
