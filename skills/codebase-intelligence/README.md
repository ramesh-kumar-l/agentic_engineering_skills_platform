# Codebase Intelligence — quickstart

Deterministic, stdlib-only structural analysis of a repository. See `SKILL.md`
for the full skill contract (when to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 23/23 tests
passing · 4/4 evaluation fixtures passing · zero runtime dependencies
(architecture pattern: [ADR-005/ADR-006](../../project-memory-bank/11-decisions.md)).
Known limitations: [`L1`–`L4`](../../project-memory-bank/12-known-limitations.md).
This is the only skill in the platform that's fully deterministic — no agent
judgment step — see the [architecture pattern write-up](../../blogs/02-two-architectures-for-ai-agent-skills.md).

## Run it

```bash
cd skills/codebase-intelligence
python -m engine.cli /path/to/repo --format both --out /path/to/output-dir
```

Omit `--out` to print to stdout instead of writing files.

## Run the tests

```bash
cd skills/codebase-intelligence
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/codebase-intelligence
python run_evaluation.py
```

Writes `RESULTS.md` with actual scores against the 4 fixture repositories.
