# Refactoring Safety — quickstart

Deterministic operation-parsing/target-resolution/risk-scoring engine,
wrapped by an agent-driven Refactoring Safety Checklist workflow.
Composition with `codebase-intelligence` is **required** (reuses
`feature-planner`'s, `root-cause-analyzer`'s, and `architecture-decision`'s
ADR-010 pattern a fourth time, see ADR-014). See `SKILL.md` for the full
skill contract (when to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 62/62 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100% correct, judgment layer perfect precision/recall (self-authored/
single-rater, seventh skill scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition,
reused a fourth time) + [ADR-014](../../project-memory-bank/11-decisions.md)
(new: per-target risk tier scored from real fan-in/hotspot data AND a
distinct test-coverage signal, kept separate rather than blended) · the real
dogfood run disclosed (without fixing) a real cross-skill limitation where
`codebase-intelligence`'s own `fan_in` count undercounts a real caller — see
`examples/refactoring-safety/example-run.md`.

## Run the engine

```bash
cd skills/refactoring-safety

# Assess a refactor's blast radius against a real codebase-intelligence report
python -m engine.cli path/to/refactor.txt \
  --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Or pipe content via stdin: `echo "..." | python -m engine.cli - --ci-report <report.json>`.
Omit `--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (safety flags
+ per-target risk assessment). The actual Refactoring Safety Checklist walk
(rollback plan adequacy, verification adequacy, behavioral-equivalence
scope) is derived by the agent following `SKILL.md`'s Step 3, not by this
CLI alone.

## Run the tests

```bash
cd skills/refactoring-safety
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/refactoring-safety
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic safety-flag/
risk-tier layer and the judgment layer (this session's actual checklist
derivation vs. ground truth).
