# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to. Read
this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-23 — end of Phase 7._

## Repository contents

```
LICENSE                    Apache-2.0 (pre-existing, unmodified)
README.md                  Full production-grade project overview (rewritten post-Phase-5)
QuickStarterGuide.md       First-run walkthrough for a new reader/contributor
DEPENDENCIES.md            Full dependency footprint explanation (it's ~empty, on purpose)
requirements.txt           The one real dependency: pytest>=7.0
CONTRIBUTING.md            How to propose a skill
SECURITY.md                Vulnerability reporting policy
ROADMAP.md                 Public pointer to 08-roadmap.md
CHANGELOG.md                Keep-a-Changelog format
blogs/                     5-post public technical blog series + index README (pre-Phase-6)
project-memory-bank/       This memory bank (see below)
skills/codebase-intelligence/       Skill 1 — SKILL.md + Python engine
skills/adversarial-diff-reviewer/   Skill 2 — SKILL.md + Python engine + agent workflow
skills/acceptance-test-engineer/    Skill 3 — SKILL.md + Python engine + agent workflow
skills/feature-planner/             Skill 4 — SKILL.md + Python engine + agent workflow, required composition (ADR-010)
skills/security-context-guard/      Skill 5 — SKILL.md + Python engine + agent workflow, optional composition, advisory-only verdict (ADR-011)
skills/root-cause-analyzer/         Skill 6 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused), tiered evidence scoring (ADR-012)
skills/architecture-decision/       Skill 7 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a third time), per-option blast-radius tiering (ADR-013)
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
evaluations/acceptance-test-engineer/    Evaluation harness + 8 fixtures + RESULTS.md
evaluations/feature-planner/             Evaluation harness + 8 fixtures + RESULTS.md
evaluations/security-context-guard/      Evaluation harness + 8 fixtures + RESULTS.md
evaluations/root-cause-analyzer/         Evaluation harness + 8 fixtures + RESULTS.md
evaluations/architecture-decision/       Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
examples/acceptance-test-engineer/       Dogfood run against a real, already-shipped CLI's behavior
examples/feature-planner/                Dogfood run: fresh codebase-intelligence report + a real task
examples/security-context-guard/         Dogfood run: real source + a real pending git-push decision; also Pilot C
examples/root-cause-analyzer/            Dogfood run: fresh codebase-intelligence report + a real retrospective symptom (Phase 5's L16)
examples/architecture-decision/          Dogfood run: fresh codebase-intelligence report + a real decision this phase's build faced; found+fixed L20, disclosed L21
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
03-architecture.md              updated this phase (Pattern 2 reused a sixth time, ADR-013 note)
04-skill-contract.md
05-evaluation-framework.md      updated this phase (Architecture Decision Record Checklist added)
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md                   updated this phase (Phase 7 complete + reordering note, Phase 8 now Refactoring Safety)
11-decisions.md                 updated this phase (ADR-013)
12-known-limitations.md         updated this phase (L20-L21)
16-assumptions-and-validation.md   updated this phase (A5, A10)
17-experiment-viability-check.md
implementation-status.md        updated this phase
active-context.md               updated this phase
sprint-history/SPRINT-00.md
sprint-history/SPRINT-01.md
sprint-history/SPRINT-02.md
sprint-history/SPRINT-03.md
sprint-history/SPRINT-04.md
sprint-history/SPRINT-05.md
sprint-history/SPRINT-06.md
sprint-history/SPRINT-07.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no reusable
composed workflows yet), `10-ui-ux-principles.md` (no UI yet),
`13-lessons-learned.md`, `14-community-feedback.md`, `15-metrics.md` (no
external usage yet).

## What exists in practice

- **Seven skills implemented**, all Level 2 (Evaluated) per
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
  - `root-cause-analyzer` — deterministic stack-trace/keyword tiered
    candidate-location engine + agent-driven Root Cause Investigation
    Checklist workflow (Pattern 2, reused a fifth time), plus ADR-012:
    stack-trace-confirmed evidence always outranks keyword overlap via a
    dominant, non-blended score tier. Reuses `feature-planner`'s
    mandatory-composition rule (ADR-010) a second time.
  - `architecture-decision` — deterministic option-parsing/blast-radius-
    scoring engine + agent-driven Architecture Decision Record Checklist
    workflow (Pattern 2, reused a sixth time), plus ADR-013: each option's
    blast radius is rolled up into a low/medium/high tier from real
    fan-in/hotspot data. Reuses `feature-planner`'s/`root-cause-analyzer`'s
    mandatory-composition rule (ADR-010) a third time.
  Full detail in [[implementation-status.md]].
- **Seven evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing), adversarial-diff-reviewer (8 fixtures, deterministic 100%,
  judgment 100% precision/recall), acceptance-test-engineer (8 fixtures,
  same pattern, same result), feature-planner (8 fixtures, same pattern,
  same result), security-context-guard (8 fixtures, same pattern, same
  result), root-cause-analyzer (8 fixtures, deterministic 100%, judgment
  layer 7/8 perfect + 1/8 at 0.67/0.67 — the first non-perfect judgment
  score), architecture-decision (8 fixtures, deterministic 100%, judgment
  100% precision/recall on all 8). All six judgment-layer evaluations carry
  the L8 self-authored/single-rater caveat — now applying a sixth time.
- **215 total unit/integration tests** across seven skills (23 + 23 + 24 +
  21 + 58 + 32 + 34), all passing.
- **Seven real bugs/gaps found and fixed via dogfooding**, not hypothetical:
  L1 (Phase 1, false-positive entry-point detection), L5/L6 (Phase 2, two
  successive secret-redaction gaps), L10 (Phase 3, `adversarial-diff-
  reviewer`'s CLI had zero test coverage — the first cross-skill dogfood
  finding), L13 (Phase 4, `acceptance-test-engineer`'s CLI had zero test
  coverage — the second cross-skill dogfood finding), and L16 (Phase 5,
  `security-context-guard`'s own action classifier used a fixed-distance
  proximity window that real phrasing exceeded by 150+ characters — fixed
  by switching to same-sentence co-occurrence matching; the first dogfood
  finding located in the very skill being dogfooded, not a different one).
  Phase 6's dogfood run found no new bug — it retrospectively validated
  that this skill's candidate scorer would have correctly ranked L16's
  true root-cause file first, given only a natural-language description.
  Phase 7's dogfood run found and fixed a seventh real gap: L20, a
  tradeoff-detection regex that matched only the noun form
  ("tradeoff"/"trade-off") and missed the verb phrasing ("trades X for
  Y") the dogfood decision's own text used twice. See
  [[12-known-limitations]].
- **One real limitation found via dogfooding and deliberately left
  unfixed, with the two-layer architecture shown correcting for it in the
  same run**: L14 — `feature-planner`'s relevance scorer ranked the true
  target file 13th (not 1st) in a real dogfood run; the agent's Step 3
  judgment correctly identified the right file anyway. Phase 7 surfaced a
  sharper version of the same mechanism class (L21) at full-repo scale —
  disclosed, not fixed, same discipline.
- **A fifth judgment-based skill evaluated the same way as the first
  four — and the first to break the perfect-score pattern**:
  root-cause-analyzer scored 7/8 fixtures perfect and 1/8 (case-03) at
  0.67/0.67 precision/recall against self-authored ground truth (L19 in
  [[12-known-limitations]]), disclosed as-is rather than adjusted.
  architecture-decision (the sixth) returned to a perfect 8/8 score —
  stated plainly as *not* evidence of higher judgment quality, since a
  single self-authored evaluation cannot support that comparison. Neither
  a perfect score nor an imperfect one, on self-authored single-rater
  fixtures, is evidence of real-world quality. Disclosed explicitly in all
  six skills' `RESULTS.md` and `SKILL.md`.
- **First skill with mandatory (not optional) composition**: `feature-
  planner` (ADR-010, Phase 4) — now joined by `root-cause-analyzer` (Phase
  6) and `architecture-decision` (Phase 7), the third skill to adopt the
  same rule.
- **First skill whose engine output is explicitly advisory-only by
  design, not just by convention**: `security-context-guard` (ADR-011) —
  `classification.suggested_verdict` is never treated as an executed gate
  anywhere in the codebase; the actual authorization decision stays with
  the agent's Step 3 workflow and, ultimately, a human.
- **First skill with explicit, non-blended evidence tiers**:
  `root-cause-analyzer` (ADR-012) — a stack-trace-confirmed candidate
  location is never scored or presented with the same confidence as a
  keyword-overlap-only one.
- **First skill with per-option structural blast-radius tiering**:
  `architecture-decision` (ADR-013) — an option touching a real hotspot is
  never scored or presented with the same confidence as one touching
  nothing real; a zero-match option is explicitly distinguished from a
  genuinely low-impact one only by the agent's Step 3 judgment, not the
  engine.
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
  any of the seven skills. Assumptions A2/A3/A5/A7/A10 have partial
  (synthetic, self-authored, or single-pilot/single-architecture) evidence
  only — not real-world validation, not independent-rater validation.
- **Zero reusable multi-skill composed-workflow infrastructure, zero UI,
  zero product code beyond these seven skills.**

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

## Documentation & developer-experience pass (after Phase 5, not a phase)

At the user's explicit request, a non-phase documentation pass added:
`requirements.txt` and `DEPENDENCIES.md` (dependency footprint, made
explicit rather than implicit), `QuickStarterGuide.md` (first-run
walkthrough), a fully rewritten root `README.md` (production-grade, with
architecture diagrams and an explicit evaluation-honesty section), a
5-post public blog series under `blogs/` written for external
publication (Medium + GitHub visibility), and a `**Status**` line added to
each of the five skills' own `README.md` (a sixth was added directly with
its own Status line when Phase 6 built it). See [[active-context.md]] and
[[implementation-status.md]] for full detail. No code, tests, contracts, or
evaluation results changed at the time — this was documentation only, and
did not count as or replace Phase 6.

## What Phase 6 established

Reused Pattern 2 (ADR-007) for a fifth judgment-based skill and
`feature-planner`'s mandatory-composition rule (ADR-010) for a second
skill — both stated explicitly as *reuses*, not new decisions, keeping the
"first skill composing on `codebase-intelligence`'s output" claim correctly
attributed to Phase 4, not re-claimed here. Added a reusable Root Cause
Investigation Checklist (10 categories) to [[05-evaluation-framework]], a
fifth checklist, coverage-shaped like the acceptance-coverage and Plan
Quality checklists. Established a new architectural decision (ADR-012):
candidate locations are scored in two explicit, non-blended evidence tiers
(stack-trace-confirmed vs. keyword-inferred) rather than one blended
score. Ran a real, explicitly-labeled *retrospective validation* dogfood —
not a new bug find — that correctly ranked a real historical root-cause
file (`action_patterns.py`, the source of Phase 5's L16) first out of 122
scored modules from a natural-language description alone. Produced this
project's first non-perfect judgment-layer evaluation score (L19),
disclosed as-is rather than adjusted to preserve the prior four-for-four
pattern.

## What Phase 7 established

Reused Pattern 2 (ADR-007) for a sixth judgment-based skill and
`feature-planner`'s/`root-cause-analyzer`'s mandatory-composition rule
(ADR-010) for a third skill — both stated explicitly as *reuses*. Added a
reusable Architecture Decision Record Checklist (10 categories) to
[[05-evaluation-framework]], a sixth checklist, coverage-shaped like the
acceptance-coverage/Plan Quality/Root Cause Investigation checklists.
Established a new architectural decision (ADR-013): each option's blast
radius is rolled up into a three-tier structural-risk band from real
fan-in/hotspot data, rather than a bare relevance number. Ran a real
dogfood run against a genuine in-flight decision (required vs. optional
composition for this very skill) that found and fixed a real gap in the
deterministic layer (L20) and separately disclosed, without fixing, a
sharper version of the coincidental-keyword-match limitation at
full-repository scale (L21). Also corrected a phase-ordering
discrepancy plainly in [[08-roadmap]]: the roadmap had proposed Refactoring
Safety for Phase 7; the user's actual Phase 7 instruction named
Architecture Decision instead, so Refactoring Safety moves to Phase 8.

## Immediate next decision point

Phase 8 (`Refactoring Safety`) is next per [[08-roadmap]], but has
**not** been started and requires explicit user go-ahead — per the
adaptive-roadmap rule, it must be re-justified against evidence at that
time, not assumed.
