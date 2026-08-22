# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to. Read
this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-23 — end of Phase 5._

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
skills/security-context-guard/      Skill 5 — SKILL.md + Python engine + agent workflow, optional composition, advisory-only verdict (ADR-011)
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
evaluations/acceptance-test-engineer/    Evaluation harness + 8 fixtures + RESULTS.md
evaluations/feature-planner/             Evaluation harness + 8 fixtures + RESULTS.md
evaluations/security-context-guard/      Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
examples/acceptance-test-engineer/       Dogfood run against a real, already-shipped CLI's behavior
examples/feature-planner/                Dogfood run: fresh codebase-intelligence report + a real task
examples/security-context-guard/         Dogfood run: real source + a real pending git-push decision; also Pilot C
```

`workflows/` and `docs/` still do not exist — no reusable multi-skill
composed-workflow infrastructure (beyond feature-planner's single-skill
required composition, ADR-010, and manual, N=1 pilots — see
[[17-experiment-viability-check.md]]) or additional docs content yet.

## project-memory-bank/ contents

```
00-project-vision.md
01-product-thesis.md
02-requirements.md
03-architecture.md              updated this phase (Pattern 2 reused a fourth time, ADR-011 note)
04-skill-contract.md
05-evaluation-framework.md      updated this phase (Security Decision Checklist added)
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md                   updated this phase (Phase 5 complete, Phase 6 proposed next)
11-decisions.md                 updated this phase (ADR-011)
12-known-limitations.md         updated this phase (L16-L17)
16-assumptions-and-validation.md   updated this phase (A5, A7)
17-experiment-viability-check.md   updated this phase (Pilot C)
implementation-status.md        updated this phase
active-context.md               updated this phase
sprint-history/SPRINT-00.md
sprint-history/SPRINT-01.md
sprint-history/SPRINT-02.md
sprint-history/SPRINT-03.md
sprint-history/SPRINT-04.md
sprint-history/SPRINT-05.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no reusable
composed workflows yet), `10-ui-ux-principles.md` (no UI yet),
`13-lessons-learned.md`, `14-community-feedback.md`, `15-metrics.md` (no
external usage yet).

## What exists in practice

- **Five skills implemented**, all Level 2 (Evaluated) per
  [[04-skill-contract]]'s maturity model, all Trust Status EXPERIMENTAL:
  - `codebase-intelligence` — fully deterministic (Pattern 1, ADR-005/006).
  - `adversarial-diff-reviewer` — deterministic risk-flagging engine +
    agent-driven adversarial review workflow (Pattern 2, ADR-007/008).
  - `acceptance-test-engineer` — deterministic testability-flagging engine +
    agent-driven acceptance-case-derivation workflow (Pattern 2, reused
    as-is).
  - `feature-planner` — deterministic relevance-scoring/planning-flag
    engine + agent-driven structured-plan-derivation workflow (Pattern 2,
    reused a third time), plus ADR-010: requires a `codebase-
    intelligence` report as a hard precondition, the first skill in this
    project where composition is mandatory rather than optional.
  - `security-context-guard` — deterministic classify/minimize/sanitize
    engine (secret/PII/sensitive-path/action-category matching, in-place
    redaction) + agent-driven Security Decision Checklist workflow
    (Pattern 2, reused a fourth time), plus new ADR-011: the engine's
    `suggested_verdict` is always advisory — it classifies and
    recommends, never authorizes. Composition with `codebase-intelligence`
    stays optional here, unlike ADR-010.
  Full detail in [[implementation-status.md]].
- **Five evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing), adversarial-diff-reviewer (8 fixtures, deterministic 100%,
  judgment 100% precision/recall), acceptance-test-engineer (8 fixtures,
  same pattern, same result), feature-planner (8 fixtures, same pattern,
  same result), security-context-guard (8 fixtures, same pattern, same
  result). All four judgment-layer scores carry the L8 self-authored/
  single-rater caveat — now applying a fourth time.
- **149 total unit/integration tests** across five skills (23 + 23 + 24 +
  21 + 58), all passing.
- **Six real bugs/gaps found and fixed via dogfooding**, not hypothetical:
  L1 (Phase 1, false-positive entry-point detection), L5/L6 (Phase 2, two
  successive secret-redaction gaps), L10 (Phase 3, `adversarial-diff-
  reviewer`'s CLI had zero test coverage — the first cross-skill dogfood
  finding), L13 (Phase 4, `acceptance-test-engineer`'s CLI had zero test
  coverage — the second cross-skill dogfood finding), and L16 (Phase 5,
  `security-context-guard`'s own action classifier used a fixed-distance
  proximity window that real phrasing exceeded by 150+ characters — fixed
  by switching to same-sentence co-occurrence matching; the first dogfood
  finding located in the very skill being dogfooded, not a different one).
  See [[12-known-limitations]].
- **One real limitation found via dogfooding and deliberately left
  unfixed, with the two-layer architecture shown correcting for it in the
  same run**: L14 — `feature-planner`'s relevance scorer ranked the true
  target file 13th (not 1st) in a real dogfood run; the agent's Step 3
  judgment correctly identified the right file anyway.
- **A fourth judgment-based skill evaluated the same way as the first
  three**: security-context-guard also scored 100% precision/recall
  against self-authored ground truth. Four-for-four perfect self-graded
  scores is now the established pattern, not a new finding — it continues
  to show this evaluation design cannot yet discriminate good derivation
  from mediocre, not that any of the four skills performs well in the
  world. Disclosed explicitly in all four skills' `RESULTS.md` and
  `SKILL.md`.
- **First skill with mandatory (not optional) composition**: `feature-
  planner` (ADR-010, Phase 4) — unchanged this phase.
- **First skill whose engine output is explicitly advisory-only by
  design, not just by convention**: `security-context-guard` (ADR-011) —
  `classification.suggested_verdict` is never treated as an executed gate
  anywhere in the codebase; the actual authorization decision stays with
  the agent's Step 3 workflow and, ultimately, a human.
- **A first internal pilot toward A7** (does security handling increase
  trust): Pilot C, in [[17-experiment-viability-check.md]] — a real
  dogfood run against this session's own real pending git-push decision.
  One data point showed the structured recommendation matched what this
  session's existing bounded-autonomy behavior already produced on that
  case, so it did not demonstrate a changed decision; it did produce a
  concrete, auditable evidence trail and catch a real bug (L16) before it
  could mislead a real decision. A7 stays UNKNOWN — real qualitative
  feedback from an actual user remains the missing ingredient.
- **Zero real-world usage by anyone other than this session's agent**, for
  any of the five skills. Assumptions A2/A3/A5/A7/A10 have partial
  (synthetic, self-authored, or single-pilot/single-architecture) evidence
  only — not real-world validation, not independent-rater validation.
- **Zero reusable multi-skill composed-workflow infrastructure, zero UI,
  zero product code beyond these five skills.**

## What Phase 5 established

Reused Pattern 2 (deterministic pre-processor + agent-driven workflow,
ADR-007) for a fourth judgment-based skill without needing a new
base-pattern ADR — at four consecutive reuses, this is now the project's
default architecture for judgment-based skills, stated plainly rather than
re-justified each phase. Added a reusable Security Decision Checklist (7
categories) to [[05-evaluation-framework]], a fourth checklist shaped
differently from the other three (a decision-gate workflow, not a
coverage-enumeration list) but preserving the honesty-valve convention,
adapted to "fail closed under uncertainty." Established a new architectural
decision (ADR-011) making the engine's recommendation explicitly advisory-
only, extending ADR-008's redact-not-exclude discipline from diff-content
secrets to a general classify/minimize/sanitize surface covering secrets,
PII, and high-risk actions. Produced the third "real dogfood run on real
phrasing found a gap a synthetic fixture didn't" finding (L16) — the first
one found in the very skill being dogfooded — and ran Pilot C, the first
internal pilot toward A7.

## Immediate next decision point

Phase 6 (`Root Cause Analyzer`) is next per [[08-roadmap]], but has
**not** been started and requires explicit user go-ahead — per the
adaptive-roadmap rule, it must be re-justified against evidence at that
time, not assumed. See the Phase 5 completion report for the
recommendation.
