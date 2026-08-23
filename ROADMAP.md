# Roadmap

The full, current roadmap lives in
[`project-memory-bank/08-roadmap.md`](project-memory-bank/08-roadmap.md) — this
file is a short public pointer, not a duplicate.

## Current phase

**Phase 0 — Foundation** (complete): repository structure, memory bank, skill
contract, evaluation framework, security model, assumptions ledger.

**Phase 1 — Codebase Intelligence** (complete): first real skill —
`skills/codebase-intelligence/` — with a tested engine, evaluation harness,
and a dogfood run against this repo.

**Phase 2 — Adversarial Diff Reviewer** (complete): second skill —
`skills/adversarial-diff-reviewer/` — combining a deterministic risk-flagging
engine with an agent-driven adversarial review workflow, evaluated on 8
seeded-defect fixtures plus a real in-session diff.

**Phase 3 — Acceptance Test Engineer** (complete): third skill —
`skills/acceptance-test-engineer/` — reusing the same deterministic +
agent-driven pattern to turn a requirement into structured acceptance test
cases, evaluated on 8 fixtures plus a real dogfood run that found and fixed a
test-coverage gap in Phase 2's CLI. Also ran a first, explicitly-labeled
viability check for the product thesis's Experiment A/B — see
[`project-memory-bank/17-experiment-viability-check.md`](project-memory-bank/17-experiment-viability-check.md).

**Phase 4 — Feature Planner** (complete): fourth skill —
`skills/feature-planner/` — reusing the same pattern a third time to turn a
task description into a structured plan, evaluated on 8 fixtures plus a real
dogfood run against this repo's own current state. New this phase: composing
on `codebase-intelligence`'s output is a **required precondition**, not
optional context (ADR-010) — the real dogfood run found and fixed a
test-coverage gap in Phase 3's CLI, and documented (without fixing) a real
limitation in this skill's own relevance-ranking logic.

**Phase 5 — Security Context Guard** (complete): fifth skill —
`skills/security-context-guard/` — reusing the same pattern a fourth time to
classify content/actions and recommend (never self-authorize) whether an
action needs human approval, evaluated on 8 fixtures plus a real dogfood run
against this phase's own real source and a real pending git-push decision.
New this phase: the engine's recommendation is a hard-rule **advisory
only** (ADR-011) — the real dogfood run found and fixed a real bug in the
skill's own action classifier, and doubled as the first internal pilot
toward Assumption A7 (does security handling increase trust). See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Phase 6 — Root Cause Analyzer** (complete): sixth skill —
`skills/root-cause-analyzer/` — reusing the same pattern a fifth time to
turn a bug report (with or without a stack trace) into ranked, evidence-
tiered candidate root-cause locations, evaluated on 8 fixtures plus a real
dogfood run that regenerated a fresh `codebase-intelligence` report and
retrospectively diagnosed a natural-language description of Phase 5's own
L16 defect. New this phase: candidate locations are scored in two explicit,
non-blended evidence tiers — stack-trace-confirmed vs. keyword-inferred
(ADR-012) — and this skill reuses Phase 4's mandatory-composition rule
(ADR-010) a second time. This phase also produced the project's first
non-perfect judgment-layer evaluation score, disclosed as-is. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Phase 7 — Architecture Decision** (complete): seventh skill —
`skills/architecture-decision/` — reusing the same pattern a sixth time to
turn a decision description into per-option, blast-radius-scored impact
against a real dependency graph, evaluated on 8 fixtures (all 8 scored
perfect on both layers) plus a real dogfood run against a genuine in-flight
decision this phase's own build faced. New this phase: **ADR-013** — each
option's structural blast radius is scored as an explicit `low`/`medium`/
`high` tier from real fan-in/hotspot data, not a bare relevance number —
and this skill reuses Phase 4's mandatory-composition rule (ADR-010) a
third time. The real dogfood run found and fixed a real gap in the
tradeoff-detection regex, and separately disclosed (without fixing) a
sharper version of the coincidental-keyword-match limitation at
full-repository scale. Note: this roadmap previously proposed Refactoring
Safety for Phase 7 — the actual Phase 7 instruction named Architecture
Decision instead, so Refactoring Safety now sits at Phase 8. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Proposed next: Phase 8 — Refactoring Safety.** Not started; requires
explicit maintainer approval and re-justification against evidence before
work begins.

## How phases work here

Phases are executed one at a time, each ending in a completion report and a
hard stop. A phase is **not** pre-committed just because it appears later in
the list — before starting any phase, we re-check whether it's still justified
by evidence gathered so far (see the assumptions ledger). Expect this roadmap
to change as real usage teaches us things the original plan didn't anticipate.

## Long-term shape (subject to the above)

Foundation skills → Engineering Lifecycle skills → Advanced skills (composition,
registry, engineering memory). See
[`project-memory-bank/08-roadmap.md`](project-memory-bank/08-roadmap.md) for the
full phase and skill-portfolio list.
