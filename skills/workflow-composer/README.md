# Workflow Composer — quickstart

Real-execution orchestrator: given a registered template name, a target
repo, and a task description, subprocess-invokes a small, hardcoded chain
of this portfolio's own real skill CLIs — the first skill in the
portfolio whose deliverable is composed execution, not analysis. Every
template's first step is a required `codebase-intelligence` report
(reuses `feature-planner`'s, `root-cause-analyzer`'s,
`architecture-decision`'s, `refactoring-safety`'s, `regression-hunter`'s,
`release-readiness`'s, `dependency-supply-chain`'s,
`engineering-knowledge-capture`'s, and `context-optimizer`'s ADR-010
pattern a tenth time). Fails CLOSED (ADR-020) on any step failure or a
pre-execution compatibility drift — the opposite default from
`context-optimizer`'s ADR-019 content-inclusion inversion, for reasons
explained in `project-memory-bank/11-decisions.md`. See `SKILL.md` for
the full skill contract — when to use it, what it explicitly does NOT do
(no arbitrary skill chaining, no target-repo mutation, not Experiment B).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 51/51 tests
passing (including one genuinely real subprocess-based integration test) ·
zero runtime dependencies · architecture pattern:
[ADR-007](../../project-memory-bank/11-decisions.md) +
[ADR-010](../../project-memory-bank/11-decisions.md) (required composition
with codebase-intelligence, reused a tenth time) + ADR-020 (see
`project-memory-bank/11-decisions.md`) covering the fail-closed execution
default and the hardcoded 3-template registry.

## Run the engine

```bash
cd skills/workflow-composer

# List the registered templates
python -m engine.cli --list-templates

# Validate a plan cheaply first — zero subprocess calls
python -m engine.cli understand-then-plan --repo-path /path/to/repo \
  --dry-run --out-dir /path/to/output-dir

# Run it for real
python -m engine.cli understand-then-plan --repo-path /path/to/repo \
  --task "Add a subtract(a, b) helper next to add()." \
  --out-dir /path/to/output-dir --format both
```

`--repo-path` and `--out-dir` are always required; `--task` is required
unless `--dry-run` is set. Each real step's own output lands under
`--out-dir/stepN-<skill-name>/`, alongside the run's own
`workflow-run-report.json`/`.md`.

The engine only sequences and (optionally) executes the chain. The actual
Workflow Composition Checklist walk (does the task really fit this
template, is a compatibility issue trustworthy to ignore) is derived by
the agent following `SKILL.md`'s Step 4, not by this CLI alone. This
skill never mutates the target repo — every composed skill stays
read-only/advisory.

## Run the tests

```bash
cd skills/workflow-composer
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/workflow-composer
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic layer (real
registry templates against a bundled tiny fixture repo, plus fail-closed
paths against fixture fake skills for determinism) and the judgment layer
(this session's actual checklist derivation vs. ground truth).
