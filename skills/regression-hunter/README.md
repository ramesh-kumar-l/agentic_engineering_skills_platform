# Regression Hunter — quickstart

Deterministic diff-pattern/structural-blast-radius/test-coverage engine,
wrapped by an agent-driven Regression Risk Checklist workflow. Composition
with `codebase-intelligence` is **required** (reuses `feature-planner`'s,
`root-cause-analyzer`'s, `architecture-decision`'s, and
`refactoring-safety`'s ADR-010 pattern a fifth time, see ADR-015). See
`SKILL.md` for the full skill contract (when to use it, security
constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 64/64 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100% correct, judgment layer scored as computed (see
[`RESULTS.md`](../../evaluations/regression-hunter/RESULTS.md), eighth skill
scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition,
reused a fifth time) + [ADR-015](../../project-memory-bank/11-decisions.md)
(new: three explicitly separate, non-blended regression signals per changed
file — diff-pattern flags, structural blast radius, test coverage — combined
via a documented rule table into one overall tier, never blended into a
single opaque score).

## Run the engine

```bash
cd skills/regression-hunter

# Assess a diff's regression risk against a real codebase-intelligence report
python -m engine.cli path/to/diff.txt \
  --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Or pipe content via stdin: `git diff | python -m engine.cli - --ci-report <report.json>`.
Omit `--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (per-file
diff-pattern flags + structural assessment + test-coverage status + overall
tier). The actual Regression Risk Checklist walk (is a flagged pattern
actually safe here, is a missing-coverage file acceptable) is derived by the
agent following `SKILL.md`'s Step 3, not by this CLI alone.

## Run the tests

```bash
cd skills/regression-hunter
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/regression-hunter
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic diff-pattern/
structural/coverage layer and the judgment layer (this session's actual
checklist derivation vs. ground truth).
