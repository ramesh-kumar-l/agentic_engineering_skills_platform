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
seeded-defect fixtures plus a real in-session diff. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Proposed next: Phase 3 — Acceptance Test Engineer.** Not started; requires
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
