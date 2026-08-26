# Context Optimizer — quickstart

Deterministic task-relevance and context-budget engine: given a free-text
task description and a real `codebase-intelligence` report, recommends
which files an agent should actually load into context, tiered
CORE/SUPPORTING/EXCLUDED by keyword relevance and real structural signal
(fan_in/hotspot), optionally within a line budget — wrapped by an
agent-driven Context Optimization Checklist workflow. Composition with
`codebase-intelligence` is **required** (reuses `feature-planner`'s,
`root-cause-analyzer`'s, `architecture-decision`'s,
`refactoring-safety`'s, `regression-hunter`'s, `release-readiness`'s,
`dependency-supply-chain`'s, and `engineering-knowledge-capture`'s
ADR-010 pattern a ninth time). See `SKILL.md` for the full skill contract
(when to use it, security constraints, outputs, and what this skill
explicitly does NOT do — no semantic search, no automatic context
loading).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 64/64 tests
passing (CLI test file written from the start) · zero runtime dependencies ·
architecture pattern: [ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused a ninth time) + ADR-019 (see
`project-memory-bank/11-decisions.md`) covering the tokenized relevance
scorer and the fail-OPEN budget/tiering default.

## Run the engine

```bash
cd skills/context-optimizer

# Recommend files for a task against a real codebase-intelligence report
python -m engine.cli /path/to/task.txt --ci-report /path/to/codebase-intelligence-report.json \
  --budget-lines 2000 --format both --out /path/to/output-dir
```

Pass `-` instead of a file path to read the task description from stdin.
Omit `--budget-lines` to skip budget-based tiering entirely (every
relevant file stays CORE/SUPPORTING, none is EXCLUDED). Omit `--out` to
print to stdout instead of writing files. `--ci-report` is **required** —
the CLI exits non-zero with an actionable error if it's missing or
doesn't match the `codebase-intelligence` report schema.

The engine only produces the deterministic pre-decision packet (ranked
file recommendations with score/tier/matched keywords/estimated tokens).
The actual Context Optimization Checklist walk (is the CORE tier
complete, is anything recommended actually noise) is derived by the agent
following `SKILL.md`'s Step 3, not by this CLI alone. This skill never
loads any file into any actual context window itself.

## Run the tests

```bash
cd skills/context-optimizer
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/context-optimizer
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic scoring layer
and the judgment layer (this session's actual checklist derivation vs.
ground truth).
