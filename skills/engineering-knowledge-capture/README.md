# Engineering Knowledge Capture — quickstart

Deterministic decision/lesson/limitation/workaround candidate scanner,
each candidate resolved against real structural data where a module is
named, wrapped by an agent-driven Knowledge Capture Checklist workflow.
Composition with `codebase-intelligence` is **required** (reuses
`feature-planner`'s, `root-cause-analyzer`'s, `architecture-decision`'s,
`refactoring-safety`'s, `regression-hunter`'s, `release-readiness`'s, and
`dependency-supply-chain`'s ADR-010 pattern an eighth time). See
`SKILL.md` for the full skill contract (when to use it, security
constraints, outputs, and what this skill explicitly does NOT do — no
commit-history parsing, no automatic memory-bank writes).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 47/47 tests
passing (CLI test file written from the start) · zero runtime dependencies ·
architecture pattern: [ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused an eighth time) + ADR-018 (see
`project-memory-bank/11-decisions.md`) covering the location resolver's
word-boundary-correct-from-day-one implementation and the fail-closed
priority default.

## Run the engine

```bash
cd skills/engineering-knowledge-capture

# Scan a narrative for capture candidates against a real codebase-intelligence report
python -m engine.cli /path/to/narrative.txt --ci-report /path/to/codebase-intelligence-report.json \
  --format both --out /path/to/output-dir
```

Pass `-` instead of a file path to read the narrative from stdin. Omit
`--out` to print to stdout instead of writing files. `--ci-report` is
**required** — the CLI exits non-zero with an actionable error if it's
missing or doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (candidate
list with category/evidence/resolved location/advisory priority). The
actual Knowledge Capture Checklist walk (is this genuinely new knowledge,
does it duplicate something already captured, what's the right canonical
entry to draft) is derived by the agent following `SKILL.md`'s Step 3, not
by this CLI alone. This skill never writes into `project-memory-bank/`
itself.

## Run the tests

```bash
cd skills/engineering-knowledge-capture
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/engineering-knowledge-capture
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic scanning layer
and the judgment layer (this session's actual checklist derivation vs.
ground truth).
