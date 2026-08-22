# 08 — Roadmap

The roadmap is adaptive. At every phase boundary, ask: "Is this next skill still
justified by evidence?" If no, update this file — do not build a planned skill
just because it was planned earlier. See [[16-assumptions-and-validation]].

## Phase list

```
PHASE 0  — Foundation                        ← COMPLETE
PHASE 1  — Codebase Intelligence             ← COMPLETE
PHASE 2  — Adversarial Diff Reviewer         ← COMPLETE (this phase)
PHASE 3  — Acceptance Test Engineer          ← proposed next, not started
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

## Phase 0 scope

Repository structure, memory bank, skill contract, evaluation framework,
assumptions ledger, security model, roadmap, contribution model, tracking. No
skill implementation, no product functionality.

## Phase 1 scope (this phase) — complete

Built `codebase-intelligence`: `SKILL.md` contract + a stdlib-only Python
engine (11 modules, each under 300 lines) + 23 passing tests + a 4-fixture
evaluation harness (all passing) + a dogfood run against this repo that found
and fixed a real bug pre-ship. See [[03-architecture]],
[[implementation-status.md]], [[12-known-limitations]]. Established the
"SKILL.md + deterministic engine" pattern (ADR-005/006 in [[11-decisions]])
for reuse by later skills where the underlying task is deterministic.

No real-world (non-agent) usage yet — see [[16-assumptions-and-validation]]
for what Phase 1 did and did not validate.

## Phase 2 scope (this phase) — complete

Built `adversarial-diff-reviewer`: a second architectural pattern
(deterministic risk-flagging engine + agent-driven adversarial review
workflow, ADR-007/008 in [[11-decisions]]) for judgment-based skills, the
counterpart to Phase 1's fully-deterministic pattern. `SKILL.md` contract +
19 passing tests + an 8-fixture evaluation harness scoring both the
deterministic layer (automated) and the judgment layer (this session's agent
actually performing the review, not fabricated) + a dogfood run against a
real diff that found and fixed two real bugs in sequence (L5, L6 in
[[12-known-limitations]]). See [[03-architecture]] Pattern 2,
[[implementation-status.md]].

Important honesty note: the judgment-layer evaluation's 100% precision/recall
is self-authored, single-rater evidence (L8) — the same agent wrote the
fixtures, ground truth, and review. Do not read it as proof of real-world
review quality; see [[16-assumptions-and-validation]] A5.
