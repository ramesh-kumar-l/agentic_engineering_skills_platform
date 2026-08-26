# Real dogfood run — context-optimizer

This is a real run, not a synthetic fixture: a fresh `codebase-intelligence`
report regenerated against this repo's current (thirteen-skill) state, and a
real task description drawn from this actual session's own work — what this
session was genuinely asked to build — not invented text.

## Commands run

```bash
cd skills/codebase-intelligence
python -m engine.cli ../../ --format json --out <scratch>/ci_out

cd ../context-optimizer
python -m engine.cli <scratch>/task.txt \
  --ci-report <scratch>/ci_out/report.json --budget-lines 1500 --format json
```

## Task description input

```
Build a thirteenth skill, context-optimizer, that composes on
codebase-intelligence's report to score file relevance against a task
description and recommend a budget-aware CORE/SUPPORTING/EXCLUDED tiered
file list, reusing ADR-010's required-composition pattern and the
fail-closed-under-uncertainty discipline. Update the evaluation harness
and the project memory bank.
```

## Actual output (summary)

- 556 files scored above zero relevance out of the full repo.
- Tier breakdown: 17 CORE, 10 SUPPORTING, 529 EXCLUDED (budget_lines=1500).
- Estimated tokens (CORE + SUPPORTING, crude line-count heuristic): 410,600.
- 9 files flagged `oversized_alone` (their own line count exceeds 1500
  alone — e.g. several `project-memory-bank/*.md` files).

Top-scoring CORE recommendations:

```
  56  evaluations/context-optimizer/run_evaluation.py
  45  skills/context-optimizer/engine/budget_selector.py
  45  skills/context-optimizer/engine/ci_report_loader.py
  44  evaluations/architecture-decision/run_evaluation.py       <-- NOISE
  44  evaluations/regression-hunter/run_evaluation.py           <-- NOISE
  44  evaluations/release-readiness/run_evaluation.py           <-- NOISE
  43  skills/context-optimizer/engine/cli.py
  42  evaluations/feature-planner/run_evaluation.py             <-- NOISE
  33  skills/context-optimizer/engine/report.py
  24  skills/context-optimizer/engine/size_estimator.py
  15  evaluations/context-optimizer/fixtures/.../ci_report.json
  15  evaluations/context-optimizer/fixtures/.../task.txt
  12  evaluations/context-optimizer/expected/case-01....json
  12  evaluations/context-optimizer/fixtures/.../task.txt
   6  evaluations/codebase-intelligence/fixtures/.../pkg/__init__.py  <-- NOISE
   6  skills/context-optimizer/engine/__init__.py
   6  skills/context-optimizer/tests/__init__.py
```

## What this confirms

The intended positive path works: `skills/context-optimizer/engine/`'s
own files (budget_selector.py, ci_report_loader.py, cli.py, report.py,
size_estimator.py, plus several evaluation fixtures) correctly score CORE
and rank near the top — a task description genuinely about
context-optimizer's own build surfaces context-optimizer's own files with
real, defensible keyword and structural signal. The `codebase-
intelligence` composition (ADR-010, ninth reuse) genuinely grounds every
score in real file/module data, not a guess.

## What this found — a new, real, disclosed-not-fixed limitation

**12 of the 17 CORE recommendations were genuinely `context-optimizer`
files — but 5 were not.** Four other skills' `evaluations/*/run_evaluation.py`
files (architecture-decision, regression-hunter, release-readiness,
feature-planner) scored 42-44 — as high as or higher than several
genuinely relevant `context-optimizer` engine files — plus one unrelated
`codebase-intelligence` fixture `__init__.py`. This is a real, concrete
instance of the same coincidental-keyword-collision mechanism class
`architecture-decision`'s L14/L19/L21 already disclosed, but a new
manifestation of it: not a short module stem, not a shared directory-name
token, but this project's own extensively duplicated evaluation-harness
docstring boilerplate ("skill", "report", "score", "task", "evaluation",
"harness", "project", "memory", "bank" — words nearly every
`run_evaluation.py` in this repo shares). A task description about
building a new skill in *this specific portfolio* necessarily uses this
project's own recurring vocabulary, and the keyword scorer has no way to
tell "genuinely about this task" apart from "happens to share this
project's own boilerplate everywhere."

This is now logged as **L29** in
`project-memory-bank/12-known-limitations.md`: disclosed, not fixed, the
same way `architecture-decision`'s L21 (the closest sibling finding) was
handled — a real fix would need TF-IDF-style down-weighting of
corpus-common terms or a minimum keyword-specificity threshold, neither
implemented, and this is now the second time this exact mechanism class
has been hit on a real dogfood run without either project having acted on
it.

## Honest comparison to the synthetic fixtures

The evaluation harness's 8 hand-authored fixtures (`evaluations/
context-optimizer/RESULTS.md`) each use small, isolated CI reports with 1-3
files and deliberately distinct vocabulary per file — none of them could
have caught this, because none of them contain the corpus-wide vocabulary
repetition a 143-module, thirteen-skill real repository actually has. This
is the same category of honest gap between "the workflow executes
correctly on fixtures" and "the workflow performs well at real scale" this
project's L8 caveat already generalizes — and the same gap
`architecture-decision`'s own dogfood run (L21) first demonstrated for a
structurally different skill, now confirmed a second time for a skill
built specifically to avoid repeating known bug classes.
