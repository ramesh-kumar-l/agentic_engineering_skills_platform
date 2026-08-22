# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to.
Read this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-23 — end of Phase 3._

## Repository contents

```
LICENSE                    Apache-2.0 (pre-existing, unmodified)
README.md                  Project overview, points to memory bank
CONTRIBUTING.md            How to propose a skill
SECURITY.md                Vulnerability reporting policy
ROADMAP.md                 Public pointer to 08-roadmap.md
CHANGELOG.md                Keep-a-Changelog format
project-memory-bank/       This memory bank (see below)
skills/codebase-intelligence/       Skill 1 — SKILL.md + Python engine
skills/adversarial-diff-reviewer/   Skill 2 — SKILL.md + Python engine + agent workflow
skills/acceptance-test-engineer/    Skill 3 — SKILL.md + Python engine + agent workflow
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
evaluations/acceptance-test-engineer/    Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
examples/acceptance-test-engineer/       Dogfood run against a real, already-shipped CLI's behavior
```

`workflows/` and `docs/` still do not exist — no composed workflows (beyond
one manual, N=1 pilot — see [[17-experiment-viability-check.md]]) or
additional docs content yet.

## project-memory-bank/ contents

```
00-project-vision.md
01-product-thesis.md
02-requirements.md
03-architecture.md              updated this phase (Pattern 2 reused, not re-derived)
04-skill-contract.md
05-evaluation-framework.md      updated this phase (acceptance-coverage checklist added)
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md
11-decisions.md                 updated this phase (ADR-009)
12-known-limitations.md         updated this phase (L10-L12)
16-assumptions-and-validation.md   updated this phase (A2, A5, A10)
17-experiment-viability-check.md   NEW this phase
implementation-status.md        updated this phase
active-context.md               updated this phase
sprint-history/SPRINT-00.md
sprint-history/SPRINT-01.md
sprint-history/SPRINT-02.md
sprint-history/SPRINT-03.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no composed
workflows yet), `10-ui-ux-principles.md` (no UI yet), `13-lessons-learned.md`,
`14-community-feedback.md`, `15-metrics.md` (no external usage yet).

## What exists in practice

- **Three skills implemented**, all Level 2 (Evaluated) per
  [[04-skill-contract]]'s maturity model, all Trust Status EXPERIMENTAL:
  - `codebase-intelligence` — fully deterministic (Pattern 1, ADR-005/006).
  - `adversarial-diff-reviewer` — deterministic risk-flagging engine +
    agent-driven adversarial review workflow (Pattern 2, ADR-007/008).
  - `acceptance-test-engineer` — deterministic testability-flagging engine +
    agent-driven acceptance-case-derivation workflow (Pattern 2, reused
    as-is — no new ADR needed, itself evidence the pattern generalizes).
  Full detail in [[implementation-status.md]].
- **Three evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing), adversarial-diff-reviewer (8 fixtures, deterministic 100%,
  judgment 100% precision/recall), acceptance-test-engineer (8 fixtures, same
  pattern, same result) — both judgment-layer scores carry the L8
  self-authored/single-rater caveat.
- **66 total unit/integration tests** across three skills (23 + 23 + 20),
  all passing.
- **Four real bugs/gaps found and fixed via dogfooding**, not hypothetical:
  L1 (Phase 1, false-positive entry-point detection), L5/L6 (Phase 2, two
  successive secret-redaction gaps), and L10 (Phase 3, `adversarial-diff-
  reviewer`'s CLI had zero test coverage — the first cross-skill dogfood
  finding, surfaced by Phase 3's skill against Phase 2's shipped code). See
  [[12-known-limitations]].
- **A second judgment-based skill evaluated the same way as the first**:
  acceptance-test-engineer also scored 100% precision/recall against
  self-authored ground truth. Two-for-two perfect self-graded scores is now
  itself the notable finding — it shows this evaluation design cannot yet
  discriminate good derivation from mediocre, not that either skill performs
  well in the world. Disclosed explicitly in both skills' `RESULTS.md` and
  `SKILL.md`.
- **First Experiment A/B viability check**: [[17-experiment-viability-check.md]]
  assesses what's actually missing to run either experiment for real (an
  independent party, above all) and runs two explicitly-labeled internal
  pilots (N=1, self-run, un-blinded) that found plausible signal without
  being evidence at the required rigor — governed by new ADR-009 (pilots must
  never be presented as the validated experiment).
- **Zero real-world usage by anyone other than this session's agent**, for
  any of the three skills. Assumptions A2/A3/A5/A10 have partial (synthetic,
  self-authored, or single-pilot) evidence only — not real-world validation,
  not independent-rater validation.
- **Zero reusable composed-workflow infrastructure, zero UI, zero product
  code beyond these three skills.**

## What Phase 3 established

Reused Pattern 2 (deterministic pre-processor + agent-driven workflow,
ADR-007) for a second judgment-based skill without needing a new base-pattern
ADR — evidence the pattern generalizes across at least two different
judgment domains (diff review, requirement testability). Added a reusable
acceptance-coverage checklist to [[05-evaluation-framework]]. Produced the
first cross-skill dogfood finding (L10). Delivered the first Experiment A/B
viability assessment plus two honestly-bounded pilots, and a new process rule
(ADR-009) for how to handle "not-yet-viable" experiments without inflating
their evidentiary weight.

## Immediate next decision point

Phase 4 (`Feature Planner`) is next per [[08-roadmap]], but has **not** been
started and requires explicit user go-ahead — per the adaptive-roadmap rule,
it must be re-justified against evidence at that time, not assumed. See the
Phase 3 completion report for the recommendation.
