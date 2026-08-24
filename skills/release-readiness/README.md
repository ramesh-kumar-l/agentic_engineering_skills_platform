# Release Readiness — quickstart

Deterministic diff-hygiene/structural-blast-radius/test-coverage engine,
wrapped by an agent-driven Release Readiness Checklist workflow. Composition
with `codebase-intelligence` is **required** (reuses `feature-planner`'s,
`root-cause-analyzer`'s, `architecture-decision`'s, `refactoring-safety`'s,
and `regression-hunter`'s ADR-010 pattern a sixth time). Composition with
`regression-hunter`'s and `security-context-guard`'s own reports is
**optional** — see ADR-016. See `SKILL.md` for the full skill contract
(when to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 78/78 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100% correct, judgment layer scored as computed (see
[`RESULTS.md`](../../evaluations/release-readiness/RESULTS.md), ninth skill
scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused a sixth time) +
[ADR-016](../../project-memory-bank/11-decisions.md) (new: the Release
Readiness Scorecard — five explicitly separate, non-blended readiness
signals per changed file, three always-available combined via a documented
rule table into a per-file tier, two optional surfaced but never blended
in, rolled up into one ALWAYS-ADVISORY overall verdict).

## Run the engine

```bash
cd skills/release-readiness

# Assess a diff's release readiness against a real codebase-intelligence report
python -m engine.cli path/to/diff.txt \
  --ci-report /path/to/codebase-intelligence-report.json \
  --regression-report /path/to/regression-hunter-report.json \
  --security-report /path/to/security-context-guard-report.json \
  --format both --out /path/to/output-dir
```

`--regression-report` and `--security-report` are both optional — omit
either or both and the scorecard is still produced from the three
always-available axes. Or pipe content via stdin:
`git diff | python -m engine.cli - --ci-report <report.json>`. Omit `--out`
to print to stdout instead of writing files. `--ci-report` is **required** —
the CLI exits non-zero with an actionable error if it's missing or doesn't
match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (per-file
hygiene flags + structural assessment + test-coverage status + optional
regression evidence + optional report-level security evidence + overall
verdict). The actual Release Readiness Checklist walk (is a flagged pattern
actually safe here, what does the overall verdict mean for THIS release) is
derived by the agent following `SKILL.md`'s Step 4, not by this CLI alone.
The `overall_verdict` field is always a **recommendation for a human to
review** — this skill never authorizes or executes a release itself.

## Run the tests

```bash
cd skills/release-readiness
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/release-readiness
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic hygiene/
structural/coverage/verdict layer and the judgment layer (this session's
actual checklist derivation vs. ground truth).
