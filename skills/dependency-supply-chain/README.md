# Dependency / Supply Chain — quickstart

Deterministic pin-status/known-risk-name/duplicate-version/surface-area
scanner, wrapped by an agent-driven Dependency Risk Checklist workflow.
Composition with `codebase-intelligence` is **required** (reuses
`feature-planner`'s, `root-cause-analyzer`'s, `architecture-decision`'s,
`refactoring-safety`'s, `regression-hunter`'s, and `release-readiness`'s
ADR-010 pattern a seventh time). See `SKILL.md` for the full skill contract
(when to use it, security constraints, outputs, and what this skill
explicitly does NOT check — no live CVE lookup, no license-risk detection).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 46/46 tests
passing (CLI test file written from the start) · zero runtime dependencies ·
architecture pattern: [ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused a seventh time) + a new ADR (see
`project-memory-bank/11-decisions.md`) covering the explicit no-live-
vulnerability-DB scope decision and the ADR-011-style advisory-only,
fail-closed verdict.

## Run the engine

```bash
cd skills/dependency-supply-chain

# Scan a repo's declared dependencies against a real codebase-intelligence report
python -m engine.cli --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Omit `--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (pin-status
per dependency, known-risk-name/duplicate-version flags, surface-area
stats, advisory `suggested_risk_level`). The actual Dependency Risk
Checklist walk (is a flagged unpinned range actually dangerous here, is a
known-risk name still relevant) is derived by the agent following
`SKILL.md`'s Step 3, not by this CLI alone. `suggested_risk_level` is
always a **recommendation for a human to review** — this skill never blocks
a merge or install itself.

## Run the tests

```bash
cd skills/dependency-supply-chain
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/dependency-supply-chain
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic scanning layer
and the judgment layer (this session's actual checklist derivation vs.
ground truth).
