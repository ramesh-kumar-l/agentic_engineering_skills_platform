# Feature Planner — quickstart

Deterministic relevance-scoring + planning-anti-pattern engine, wrapped by an
agent-driven structured-plan-derivation workflow. Requires a
`codebase-intelligence` `report.json` as a hard precondition (ADR-010 — see
`project-memory-bank/11-decisions.md`). See `SKILL.md` for the full skill
contract (when to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 21/21 tests
passing · 8/8 fixtures: deterministic layer 100%, judgment layer 100%
precision/recall (self-authored/single-rater — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern: [ADR-007](../../project-memory-bank/11-decisions.md)
+ [ADR-010](../../project-memory-bank/11-decisions.md) (the only skill in
the platform where composition with `codebase-intelligence` is mandatory,
not optional). Known relevance-ranking limitation, found via real
dogfooding and deliberately left unfixed:
[`L14`](../../project-memory-bank/12-known-limitations.md).

## Run the engine

```bash
# 1. Generate a codebase-intelligence report first (required)
cd skills/codebase-intelligence
python -m engine.cli /path/to/repo --format json --out /path/to/ci-out

# 2. Run feature-planner against a task description, composed with that report
cd ../feature-planner
echo "Only add a --verbose flag to the CLI. Verify via a new test." | \
  python -m engine.cli - --ci-report /path/to/ci-out/report.json --format both --out /path/to/output-dir
```

Or point it at a saved task file: `python -m engine.cli path/to/task.txt --ci-report report.json`.
Omit `--out` to print to stdout instead of writing files.

The engine only produces the deterministic pre-planning packet (planning
flags + relevance report). The actual structured plan is derived by the
agent following `SKILL.md`'s Step 3, not by this CLI alone.

## Run the tests

```bash
cd skills/feature-planner
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/feature-planner
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic planning-flag/
relevance layer and the judgment layer (this session's actual plan
derivation vs. ground truth).
