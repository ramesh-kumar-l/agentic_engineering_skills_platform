# Workflow Composer — real dogfood run

A real, non-dry-run execution of `understand-then-plan` against this
repository's own current (fourteen-skill) state — not a synthetic
stand-in. Command run from `skills/workflow-composer/`:

```bash
python -m engine.cli understand-then-plan \
  --repo-path <platform-root> \
  --task "Add a workflow-composer skill (the 14th skill in this
portfolio) that subprocess-orchestrates other skills' real CLIs, starting
from a required codebase-intelligence report, and produce a feature plan
for wiring it into the platform's memory-bank documentation and CI
matrix." \
  --out-dir <out-dir> --format both
```

This is the task description this session actually used to plan Phase 14
itself — the same "eat your own dog food on a real task from this
session" discipline every prior phase's example-run.md followed.

## What actually happened

Both real subprocess steps succeeded:

| Step | Skill | Exit code | Duration |
|---|---|---|---|
| 1 | `codebase-intelligence` | 0 | 1.513s |
| 2 | `feature-planner` | 0 | 0.797s |

Total chain duration: **2.31s** against the full, current repository
(1,010 files scanned). Zero compatibility issues — the registry's
declared `codebase-intelligence` marker was found in `feature-planner`'s
real `SKILL.md` Preconditions/Required Context sections, exactly as
`compatibility_checker.py` expects.

`codebase-intelligence`'s real dependency graph reported these hotspots
(top fan_in+fan_out modules across the whole repo):

```
skills/release-readiness/engine/models.py
skills/release-readiness/engine/report.py
skills/refactoring-safety/engine/models.py
skills/regression-hunter/engine/models.py
skills/context-optimizer/engine/report.py
skills/dependency-supply-chain/engine/models.py
skills/refactoring-safety/engine/report.py
skills/regression-hunter/engine/report.py
skills/architecture-decision/engine/models.py
skills/codebase-intelligence/engine/models.py
```

## The finding this run actually surfaced

`feature-planner`'s own relevance scoring (`ci_report_loader.py`-derived
`relevance.scores`, part of its real output, not something
workflow-composer computes itself) ranked
`skills/workflow-composer/tests/test_real_execution.py` as the **single
highest-scoring file in the entire repository** (score 29) — ahead of
every real engine implementation file, including
`skills/workflow-composer/engine/models.py` (score 25) and
`skills/codebase-intelligence/engine/models.py` (score 23). The task
description's own vocabulary ("workflow", "skill(s)", "real", "CLIs",
"plan", "into") is dense in this project's own test/doc boilerplate
across every skill, and a test file's docstrings and identifiers happened
to match more of those literal tokens than the actual implementation
files central to the task.

This is a **new, concrete instance of an already-named mechanism class**
(L14/L19/L21/L29) — but the first time it was observed directly inside
`feature-planner`'s own scorer rather than `context-optimizer`'s. It
confirms the flooding susceptibility isn't specific to `context-
optimizer`'s tokenized scorer design (ADR-019's own docstring reasoning);
it's shared by every keyword-relevance engine in this portfolio built the
same general way, `feature-planner`'s (Phase 4, the oldest of them)
included.

**Directly relevant to workflow-composer's own scope**: this skill's
executor and compatibility checker worked exactly as designed — the chain
ran, both steps succeeded, no wiring broke. But `workflow-composer`
composes with `feature-planner` *as-is*; it does not filter, re-rank, or
otherwise improve the composed skill's own output. A caller trusting
`understand-then-plan`'s step-2 output at face value, without applying
`feature-planner`'s own Known Limitations (or the human review its
Agent Responsibilities section already calls for), would end up trusting
a plan that leads with a test file over the real implementation. Logged
as a disclosed limitation, not fixed here — see
`project-memory-bank/12-known-limitations.md` L30.
