# Root Cause Analyzer — quickstart

Deterministic stack-trace/keyword candidate-location engine, wrapped by an
agent-driven Root Cause Investigation Checklist workflow. Composition with
`codebase-intelligence` is **required** (reuses `feature-planner`'s ADR-010
pattern a second time, see ADR-012). See `SKILL.md` for the full skill
contract (when to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 32/32 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100% correct, judgment layer precision/recall (self-authored/
single-rater, fifth skill scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) — the first of
the five that did **not** score perfectly on every fixture (case-03: 0.67/
0.67, disclosed as-is) · zero runtime dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition,
reused) + [ADR-012](../../project-memory-bank/11-decisions.md) (new:
stack-trace evidence always outranks keyword overlap).

## Run the engine

```bash
cd skills/root-cause-analyzer

# Diagnose a symptom against a real codebase-intelligence report
python -m engine.cli path/to/symptom.txt \
  --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Or pipe content via stdin: `echo "..." | python -m engine.cli - --ci-report <report.json>`.
Omit `--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic candidate/evidence packet
(symptom flags + ranked candidate locations, stack-trace tier vs. keyword
tier). The actual investigation (ruled-out candidates, confirmation step,
fix-risk note) is derived by the agent following `SKILL.md`'s Step 3, not by
this CLI alone.

## Run the tests

```bash
cd skills/root-cause-analyzer
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/root-cause-analyzer
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic candidate-scoring
layer and the judgment layer (this session's actual investigation derivation
vs. ground truth).
