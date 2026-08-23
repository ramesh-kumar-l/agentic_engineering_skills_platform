# Architecture Decision — quickstart

Deterministic option-parsing/blast-radius-scoring engine, wrapped by an
agent-driven Architecture Decision Record checklist workflow. Composition
with `codebase-intelligence` is **required** (reuses `feature-planner`'s and
`root-cause-analyzer`'s ADR-010 pattern a third time, see ADR-013). See
`SKILL.md` for the full skill contract (when to use it, security
constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 34/34 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100% correct, judgment layer perfect precision/recall (self-authored/
single-rater, sixth skill scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition,
reused a third time) + [ADR-013](../../project-memory-bank/11-decisions.md)
(new: per-option blast radius scored against real fan-in/fan-out/hotspot
data) · the real dogfood run found and fixed a real gap in the
tradeoff-detection regex, and separately disclosed (without fixing) a
keyword-collision limitation that sharpens at full-repo scale — see
`examples/architecture-decision/example-run.md`.

## Run the engine

```bash
cd skills/architecture-decision

# Assess a decision's options against a real codebase-intelligence report
python -m engine.cli path/to/decision.txt \
  --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Or pipe content via stdin: `echo "..." | python -m engine.cli - --ci-report <report.json>`.
Omit `--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (decision
flags + per-option blast-radius impact). The actual decision record
(consequences, reversibility, evidence, revisit trigger) is derived by the
agent following `SKILL.md`'s Step 3, not by this CLI alone.

## Run the tests

```bash
cd skills/architecture-decision
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/architecture-decision
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic decision-flag/
blast-radius layer and the judgment layer (this session's actual
decision-record derivation vs. ground truth).
