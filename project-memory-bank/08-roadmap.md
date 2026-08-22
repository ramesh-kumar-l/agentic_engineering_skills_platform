# 08 — Roadmap

The roadmap is adaptive. At every phase boundary, ask: "Is this next skill still
justified by evidence?" If no, update this file — do not build a planned skill
just because it was planned earlier. See [[16-assumptions-and-validation]].

## Phase list

```
PHASE 0  — Foundation                        ← COMPLETE (this phase)
PHASE 1  — Codebase Intelligence             ← proposed next, not started
PHASE 2  — Adversarial Diff Reviewer
PHASE 3  — Acceptance Test Engineer
PHASE 4  — Feature Planner
PHASE 5  — Security Context Guard
PHASE 6  — Root Cause Analyzer
PHASE 7  — Refactoring Safety
PHASE 8  — Architecture Decision
PHASE 9  — Regression Hunter
PHASE 10 — Release Readiness
PHASE 11 — Dependency / Supply Chain
PHASE 12 — Knowledge Capture
PHASE 13 — Context Optimizer
PHASE 14 — Workflow Composer
PHASE 15 — Engineering Memory
```

Each phase ends with a completion report and a hard STOP for user instruction
(Section 39–40 of the operating charter). No phase auto-continues into the next.

## Full target skill portfolio (do not build all at once)

**Foundation**: codebase-intelligence, feature-planner, acceptance-test-engineer,
adversarial-diff-reviewer, security-context-guard.

**Engineering Lifecycle**: root-cause-analyzer, refactoring-safety,
architecture-decision, regression-hunter, release-readiness.

**Advanced**: dependency-supply-chain-reviewer, engineering-knowledge-capture,
context-optimizer, workflow-composer, engineering-memory.

First milestone is 3 genuinely useful, evaluated skills used on real work — not
all 15.

## First-five ordering decision

Chosen order: **Codebase Intelligence → Adversarial Diff Reviewer →
Acceptance Test Engineer → Feature Planner → Security Context Guard**, rather
than the original catalog order.

Rationale: the first three let the core thesis be tested fast —
`UNDERSTAND → VERIFY → DEFINE CORRECTNESS` — before any orchestration or planning
investment. Feature Planner then extends this to
`UNDERSTAND → PLAN → DEFINE → IMPLEMENT → VERIFY`, giving a stronger
experimental foundation before memory, registry, or UI work. Logged formally in
[[11-decisions]].

## Phase 0 scope (this phase)

Repository structure, memory bank, skill contract, evaluation framework,
assumptions ledger, security model, roadmap, contribution model, tracking. No
skill implementation, no product functionality.
