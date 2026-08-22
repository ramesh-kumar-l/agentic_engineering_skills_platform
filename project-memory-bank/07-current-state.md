# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to.
Read this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-23 — end of Phase 4._

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
skills/feature-planner/             Skill 4 — SKILL.md + Python engine + agent workflow, required composition (ADR-010)
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
evaluations/acceptance-test-engineer/    Evaluation harness + 8 fixtures + RESULTS.md
evaluations/feature-planner/             Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
examples/acceptance-test-engineer/       Dogfood run against a real, already-shipped CLI's behavior
examples/feature-planner/                Dogfood run: fresh codebase-intelligence report + a real task
```

`workflows/` and `docs/` still do not exist — no reusable multi-skill
composed-workflow infrastructure (beyond feature-planner's single-skill
required composition, ADR-010, and one earlier manual, N=1 pilot — see
[[17-experiment-viability-check.md]]) or additional docs content yet.

## project-memory-bank/ contents

```
00-project-vision.md
01-product-thesis.md
02-requirements.md
03-architecture.md              updated this phase (Pattern 2 reused a third time, ADR-010 note)
04-skill-contract.md
05-evaluation-framework.md      updated this phase (Plan Quality checklist added)
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md                   updated this phase (Phase 4 complete, Phase 5 proposed next)
11-decisions.md                 updated this phase (ADR-010)
12-known-limitations.md         updated this phase (L13-L15)
16-assumptions-and-validation.md   updated this phase (A5, A10)
17-experiment-viability-check.md
implementation-status.md        updated this phase
active-context.md               updated this phase
sprint-history/SPRINT-00.md
sprint-history/SPRINT-01.md
sprint-history/SPRINT-02.md
sprint-history/SPRINT-03.md
sprint-history/SPRINT-04.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no reusable
composed workflows yet), `10-ui-ux-principles.md` (no UI yet),
`13-lessons-learned.md`, `14-community-feedback.md`, `15-metrics.md` (no
external usage yet).

## What exists in practice

- **Four skills implemented**, all Level 2 (Evaluated) per
  [[04-skill-contract]]'s maturity model, all Trust Status EXPERIMENTAL:
  - `codebase-intelligence` — fully deterministic (Pattern 1, ADR-005/006).
  - `adversarial-diff-reviewer` — deterministic risk-flagging engine +
    agent-driven adversarial review workflow (Pattern 2, ADR-007/008).
  - `acceptance-test-engineer` — deterministic testability-flagging engine +
    agent-driven acceptance-case-derivation workflow (Pattern 2, reused
    as-is).
  - `feature-planner` — deterministic relevance-scoring/planning-flag
    engine + agent-driven structured-plan-derivation workflow (Pattern 2,
    reused a third time), plus new ADR-010: requires a `codebase-
    intelligence` report as a hard precondition, the first skill in this
    project where composition is mandatory rather than optional.
  Full detail in [[implementation-status.md]].
- **Four evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing), adversarial-diff-reviewer (8 fixtures, deterministic 100%,
  judgment 100% precision/recall), acceptance-test-engineer (8 fixtures,
  same pattern, same result), feature-planner (8 fixtures — each pairing a
  task with a synthetic codebase-intelligence report, same pattern, same
  result). All three judgment-layer scores carry the L8 self-authored/
  single-rater caveat — now applying a third time.
- **91 total unit/integration tests** across four skills (23 + 23 + 24 +
  21), all passing.
- **Five real bugs/gaps found and fixed via dogfooding**, not hypothetical:
  L1 (Phase 1, false-positive entry-point detection), L5/L6 (Phase 2, two
  successive secret-redaction gaps), L10 (Phase 3, `adversarial-diff-
  reviewer`'s CLI had zero test coverage — the first cross-skill dogfood
  finding), and L13 (Phase 4, `acceptance-test-engineer`'s CLI had zero
  test coverage — the second cross-skill dogfood finding, and the first
  found by a *planning* skill rather than a review/testability skill). See
  [[12-known-limitations]].
- **One real limitation found via dogfooding and deliberately left
  unfixed, with the two-layer architecture shown correcting for it in the
  same run**: L14 — `feature-planner`'s relevance scorer ranked the true
  target file 13th (not 1st) in a real dogfood run, because its keywords
  collided with a shared parent directory name; the agent's Step 3
  judgment correctly identified the right file anyway. This is the
  strongest concrete evidence yet (stronger than L7's fixture-count
  argument) that ADR-007's "leads, not verdicts" design does what it's
  meant to do.
- **A third judgment-based skill evaluated the same way as the first two**:
  feature-planner also scored 100% precision/recall against self-authored
  ground truth. Three-for-three perfect self-graded scores is now the
  established pattern, not a new finding — it continues to show this
  evaluation design cannot yet discriminate good derivation from mediocre,
  not that any of the three skills performs well in the world. Disclosed
  explicitly in all three skills' `RESULTS.md` and `SKILL.md`.
- **First skill with mandatory (not optional) composition**: `feature-
  planner` will not run without a valid `codebase-intelligence` report
  (ADR-010). The real dogfood run demonstrates this architecture executing
  correctly and being genuinely load-bearing — not just documented as a
  design intention. This is real evidence composition *works*, which is a
  different, weaker claim than Experiment B's "composition *outperforms*
  the alternative" — that claim still requires an independent baseline
  (ADR-009) and remains UNKNOWN in [[16-assumptions-and-validation]] A10.
- **Zero real-world usage by anyone other than this session's agent**, for
  any of the four skills. Assumptions A2/A3/A5/A10 have partial (synthetic,
  self-authored, or single-pilot/single-architecture) evidence only — not
  real-world validation, not independent-rater validation.
- **Zero reusable multi-skill composed-workflow infrastructure, zero UI,
  zero product code beyond these four skills.**

## What Phase 4 established

Reused Pattern 2 (deterministic pre-processor + agent-driven workflow,
ADR-007) for a third judgment-based skill without needing a new base-pattern
ADR — now evidence the pattern generalizes across three different judgment
domains (diff review, requirement testability, task planning). Added a
reusable Plan Quality checklist to [[05-evaluation-framework]], confirming
the category-10-honesty-valve convention across all three checklists.
Established a new architectural decision (ADR-010) making composition with
`codebase-intelligence` mandatory — the first time in this project a missing
upstream skill output is a hard failure rather than a degraded path.
Produced the second cross-skill dogfood finding (L13) and the first
documented-but-unfixed relevance-ranking limitation with real evidence the
two-layer architecture compensates for it in practice (L14).

## Immediate next decision point

Phase 5 (`Security Context Guard`) is next per [[08-roadmap]], but has
**not** been started and requires explicit user go-ahead — per the
adaptive-roadmap rule, it must be re-justified against evidence at that
time, not assumed. See the Phase 4 completion report for the
recommendation.
