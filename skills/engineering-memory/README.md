# Engineering Memory — quickstart

Deterministic retrieval engine that scores this project's own memory-bank
ADRs and known limitations against a free-text task and a real
`codebase-intelligence` report, wrapped by an agent-driven Engineering
Memory Retrieval Checklist workflow. Composition with
`codebase-intelligence` is **required** (reuses `feature-planner`'s
through `workflow-composer`'s ADR-010 pattern an eleventh time). Unlike
every prior skill, the primary retrieval corpus is this project's **own**
`project-memory-bank/` markdown, not a target repo's external artifacts
(ADR-021's "self-referential composition"). See `SKILL.md` for the full
skill contract (when to use it, security constraints, outputs, and what
this skill explicitly does NOT do — no memory-bank writes, no
duplicate-detection bridge to `engineering-knowledge-capture`).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 57/57 tests
passing (CLI test file and a real end-to-end integration test written
from the start) · zero runtime dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused an eleventh time) + ADR-021 (see
`project-memory-bank/11-decisions.md`) covering the self-referential
corpus and the day-one word-boundary matching.

## Run the engine

```bash
cd skills/engineering-memory

# Retrieve relevant ADRs/limitations for a task against a real codebase-intelligence report
python -m engine.cli --task "your task description" \
  --ci-report /path/to/codebase-intelligence-report.json \
  --decisions-path /path/to/11-decisions.md \
  --limitations-path /path/to/12-known-limitations.md \
  --format both --out-dir /path/to/output-dir
```

Omit `--out-dir` to print to stdout instead of writing files. `--ci-report`,
`--decisions-path`, and `--limitations-path` are all **required** — the
CLI exits non-zero with an actionable error if any is missing.

The engine only produces the deterministic ranked retrieval packet (match
list with score/matched-keywords/matched-modules/staleness-flag). The
actual Engineering Memory Retrieval Checklist walk (is a match genuinely
relevant, how much weight does a staleness flag carry) is derived by the
agent following `SKILL.md`'s Step 3, not by this CLI alone. This skill
never writes into `project-memory-bank/` itself.

## Run the tests

```bash
cd skills/engineering-memory
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/engineering-memory
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic retrieval layer
and the judgment layer (this session's actual checklist derivation vs.
ground truth).
