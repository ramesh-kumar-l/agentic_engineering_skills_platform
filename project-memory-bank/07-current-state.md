# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to. Read
this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-24 — end of Phase 10. **Superseded in part by
2026-08-26 events (mentor-review follow-up + Phase 11,
`dependency-supply-chain` + Phase 12, `engineering-knowledge-capture` +
Phase 13, `context-optimizer` + Phase 14, `workflow-composer`) — see
[[active-context.md]] for the current picture; this file's detailed
Phase 10 walkthrough below is still accurate for Phases 1-10, but test
counts and "Phase 11 proposed next" language are stale.**_

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
skills/engineering-knowledge-capture/  Skill 12 — SKILL.md + Python engine + agent workflow (Phase 12, 2026-08-26)
skills/context-optimizer/          Skill 13 — SKILL.md + Python engine + agent workflow (Phase 13, 2026-08-26)
skills/workflow-composer/          Skill 14 — SKILL.md + Python engine + agent workflow, first skill executing other skills' real code, required composition (ADR-010, reused a tenth time) (Phase 14, NEW 2026-08-26)
skills/acceptance-test-engineer/    Skill 3 — SKILL.md + Python engine + agent workflow
skills/feature-planner/             Skill 4 — SKILL.md + Python engine + agent workflow, required composition (ADR-010)
skills/security-context-guard/      Skill 5 — SKILL.md + Python engine + agent workflow, optional composition, advisory-only verdict (ADR-011)
skills/root-cause-analyzer/         Skill 6 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused), tiered evidence scoring (ADR-012)
skills/architecture-decision/       Skill 7 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a third time), per-option blast-radius tiering (ADR-013)
skills/refactoring-safety/          Skill 8 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a fourth time), per-target risk tier + independent test-coverage signal (ADR-014)
skills/regression-hunter/           Skill 9 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a fifth time), three-axis non-blended regression-risk scoring (ADR-015)
skills/release-readiness/           Skill 10 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a sixth time), Release Readiness Scorecard (ADR-016), first skill also composing OPTIONALLY with two other skills' own reports
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
evaluations/acceptance-test-engineer/    Evaluation harness + 8 fixtures + RESULTS.md
evaluations/feature-planner/             Evaluation harness + 8 fixtures + RESULTS.md
evaluations/security-context-guard/      Evaluation harness + 8 fixtures + RESULTS.md
evaluations/root-cause-analyzer/         Evaluation harness + 8 fixtures + RESULTS.md
evaluations/architecture-decision/       Evaluation harness + 8 fixtures + RESULTS.md
evaluations/refactoring-safety/          Evaluation harness + 8 fixtures + RESULTS.md
evaluations/regression-hunter/           Evaluation harness + 8 fixtures + RESULTS.md
evaluations/release-readiness/           Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
examples/acceptance-test-engineer/       Dogfood run against a real, already-shipped CLI's behavior
examples/feature-planner/                Dogfood run: fresh codebase-intelligence report + a real task
examples/security-context-guard/         Dogfood run: real source + a real pending git-push decision; also Pilot C
examples/root-cause-analyzer/            Dogfood run: fresh codebase-intelligence report + a real retrospective symptom (Phase 5's L16)
examples/architecture-decision/          Dogfood run: fresh codebase-intelligence report + a real decision this phase's build faced; found+fixed L20, disclosed L21
examples/refactoring-safety/             Dogfood run: fresh codebase-intelligence report + a real refactor this phase's build produced; disclosed L22
examples/regression-hunter/              Dogfood run: fresh codebase-intelligence report + a real git diff this phase's build produced (a genuine codebase-intelligence scanner fix); disclosed L23
examples/release-readiness/              Dogfood run: fresh codebase-intelligence report + a real, staged-then-unstaged (never committed) git diff of this phase's own 78 new files; confirmed a predicted false-positive shape, disclosed L24
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
03-architecture.md              updated this phase (Pattern 2 reused a ninth time, ADR-016 note)
04-skill-contract.md
05-evaluation-framework.md      updated this phase (Release Readiness Checklist added)
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md                   updated this phase (Phase 10 complete, Phase 11 proposed next)
operating-charter.md            NEW 2026-08-26 — the previously-referenced-
                                 but-missing source document ADR-001 adopts
11-decisions.md                 updated this phase (ADR-016)
12-known-limitations.md         updated this phase (L24)
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
sprint-history/SPRINT-07.md
sprint-history/SPRINT-08.md
sprint-history/SPRINT-09.md
sprint-history/SPRINT-10.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no reusable
composed workflows yet), `10-ui-ux-principles.md` (no UI yet),
`13-lessons-learned.md`, `14-community-feedback.md`, `15-metrics.md` (no
external usage yet).

## What exists in practice

- **Ten skills implemented**, all Level 2 (Evaluated) per
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
  - `refactoring-safety` — deterministic operation-parsing/target-
    resolution/risk-scoring engine + agent-driven Refactoring Safety
    Checklist workflow (Pattern 2, reused a seventh time), plus ADR-014:
    each target's risk tier is scored from real fan-in/hotspot data
    (operation-type aware) and kept as a field distinct from an
    independently-computed test-coverage signal. Reuses `feature-
    planner`'s/`root-cause-analyzer`'s/`architecture-decision`'s
    mandatory-composition rule (ADR-010) a fourth time.
  - `regression-hunter` — deterministic diff-pattern/structural-blast-
    radius/test-coverage engine (5 mechanical diff-pattern checks scanned
    directly against a diff's own hunks, resolved against
    `codebase-intelligence`'s real dependency graph, plus an independent
    test-coverage signal) + agent-driven Regression Risk Checklist workflow
    (Pattern 2, reused an eighth time), plus ADR-015: three explicitly
    separate, non-blended regression signals per changed file, combined
    into one `overall_risk_tier` via a documented rule table rather than
    blended. Reuses `feature-planner`'s/`root-cause-analyzer`'s/
    `architecture-decision`'s/`refactoring-safety`'s mandatory-composition
    rule (ADR-010) a fifth time.
  - `release-readiness` — deterministic diff-hygiene/structural-blast-
    radius/test-coverage engine (debug leftovers, merge-conflict markers,
    hardcoded-secret-shaped literals, TODO-blocking markers scanned
    directly against the diff's own hunks) + agent-driven Release
    Readiness Checklist workflow (Pattern 2, reused a ninth time), plus
    ADR-016: three always-available, non-blended axes combine into a
    per-file `readiness_tier` via a documented rule table, and two
    OPTIONAL, cross-skill-composed axes (regression-hunter's and
    security-context-guard's own report evidence) are surfaced but
    deliberately not blended in. Reuses `feature-planner`'s/`root-cause-
    analyzer`'s/`architecture-decision`'s/`refactoring-safety`'s/
    `regression-hunter`'s mandatory-composition rule (ADR-010) a sixth
    time — the final skill in the Engineering Lifecycle group.
  Full detail in [[implementation-status.md]].
- **Ten evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing), adversarial-diff-reviewer (8 fixtures, deterministic 100%,
  judgment 100% precision/recall), acceptance-test-engineer (8 fixtures,
  same pattern, same result), feature-planner (8 fixtures, same pattern,
  same result), security-context-guard (8 fixtures, same pattern, same
  result), root-cause-analyzer (8 fixtures, deterministic 100%, judgment
  layer 7/8 perfect + 1/8 at 0.67/0.67 — the first non-perfect judgment
  score), architecture-decision (8 fixtures, deterministic 100%, judgment
  100% precision/recall on all 8), refactoring-safety (8 fixtures,
  deterministic 100%, judgment 100% precision/recall on all 8),
  regression-hunter (8 fixtures, deterministic 100%, judgment 100%
  precision/recall on all 8), release-readiness (8 fixtures, deterministic
  100%, judgment 100% precision/recall on all 8). All nine judgment-layer
  evaluations carry the L8 self-authored/single-rater caveat — now
  applying a ninth time.
- **474 total unit/integration tests** across eleven skills (24 + 23 + 24 +
  21 + 58 + 32 + 34 + 64 + 66 + 82 + 46), all passing — up from 420 as of
  Phase 10, after a 2026-08-26 mentor-review follow-up (+8 tests fixing
  L23/L24) and Phase 11's `dependency-supply-chain` (+46 tests). See
  [[active-context.md]] for the current, authoritative breakdown.
- **Eight real bugs/gaps found and fixed via dogfooding**, not hypothetical:
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
  Y") the dogfood decision's own text used twice. Phase 9's dogfood run
  found and fixed an eighth real gap: `codebase-intelligence`'s own
  `engine/scanner.py` did not exclude `*.egg-info` directories from repo
  scans, indexing generated packaging metadata as if it were real source —
  fixed with a new test (`test_scan_excludes_egg_info_dirs`), suite grew
  from 23 to 24. See [[12-known-limitations]].
- **One real limitation found via dogfooding and deliberately left
  unfixed, with the two-layer architecture shown correcting for it in the
  same run**: L14 — `feature-planner`'s relevance scorer ranked the true
  target file 13th (not 1st) in a real dogfood run; the agent's Step 3
  judgment correctly identified the right file anyway. Phase 7 surfaced a
  sharper version of the same mechanism class (L21) at full-repo scale —
  disclosed, not fixed, same discipline. Phase 9 surfaced the same
  mechanism class again in a new location (L23): `target_resolver.py`'s
  substring-based caller identification, shared as an independent copy
  between `refactoring-safety` and `regression-hunter`, inflates the
  caller list for a module whose stem is a short, common word. Phase 10
  sharpened this again into a more consequential form (L24): the same
  substring-matching pattern, reused a THIRD time in `release-readiness`,
  produces false-positive **test coverage**, not just an inflated caller
  list — a genuinely untested new module can look tested.
- **A fifth judgment-based skill evaluated the same way as the first
  four — and the first to break the perfect-score pattern**:
  root-cause-analyzer scored 7/8 fixtures perfect and 1/8 (case-03) at
  0.67/0.67 precision/recall against self-authored ground truth (L19 in
  [[12-known-limitations]]), disclosed as-is rather than adjusted.
  architecture-decision (the sixth), refactoring-safety (the seventh),
  regression-hunter (the eighth), and release-readiness (the ninth) all
  returned to a perfect 8/8 score — stated plainly as *not* evidence of
  higher judgment quality, since a single self-authored evaluation cannot
  support that comparison. Neither a perfect score nor an imperfect one, on
  self-authored single-rater fixtures, is evidence of real-world quality.
  Disclosed explicitly in all nine skills' `RESULTS.md` and `SKILL.md`.
- **First skill with mandatory (not optional) composition**: `feature-
  planner` (ADR-010, Phase 4) — now joined by `root-cause-analyzer` (Phase
  6), `architecture-decision` (Phase 7), `refactoring-safety` (Phase 8),
  `regression-hunter` (Phase 9), and `release-readiness` (Phase 10), the
  sixth skill to adopt the same rule.
- **First skill also composing OPTIONALLY with two other skills' own
  outputs, not just `codebase-intelligence`'s**: `release-readiness`
  (ADR-016) — a supplied `regression-hunter`/`security-context-guard`
  report is surfaced verbatim as a distinct field, never re-derived and
  never blended into this skill's own rule table, reusing
  `security-context-guard`'s ADR-011 optional-composition precedent for
  these two specifically (not ADR-010's mandatory rule).
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
- **First skill with a structural risk signal kept explicitly distinct from
  an independently-computed verification signal**: `refactoring-safety`
  (ADR-014) — a target's `risk_tier` and its `test_coverage_modules` are
  never blended into one number, so a structurally risky-but-covered
  target (case-01) is never confused with a risky-and-genuinely-unverified
  one (case-02/case-04), and the text-level "no test mentioned" signal is
  never conflated with the structural "no real coverage found" signal
  (case-03 exercises exactly this divergence).
- **First skill whose deterministic layer scans a diff's own hunks
  directly, rather than a free-text description**: `regression-hunter`
  (ADR-015) — three explicitly separate, non-blended regression signals
  (diff-pattern flags, structural blast radius, test coverage) are combined
  into one `overall_risk_tier` per changed file via a documented rule
  table, while all three fields stay visible and separately inspectable —
  a flagged-but-covered file (case-03/case-06) is never confused with an
  unflagged-but-uncovered hotspot (case-02), and the two axes are shown to
  genuinely diverge on real evaluation fixtures, not just in theory.
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
  any of the eleven skills (as of Phase 11). Assumptions A2/A3/A5/A7/A10
  have partial (synthetic, self-authored, or single-pilot/single-
  architecture) evidence only — not real-world validation, not
  independent-rater validation.
- **Zero reusable multi-skill composed-workflow infrastructure, zero UI,
  zero product code beyond these eleven skills.**

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

## What Phase 8 established

Reused Pattern 2 (ADR-007) for a seventh judgment-based skill and
`feature-planner`'s/`root-cause-analyzer`'s/`architecture-decision`'s
mandatory-composition rule (ADR-010) for a fourth skill — both stated
explicitly as *reuses*. Added a reusable Refactoring Safety Checklist (10
categories) to [[05-evaluation-framework]], a seventh checklist,
coverage-shaped like the acceptance-coverage/Plan Quality/Root Cause
Investigation/Architecture Decision Record checklists. Established a new
architectural decision (ADR-014): each target's structural risk tier is
kept as a field distinct from an independently-computed test-coverage
signal, rather than blended into one score. Ran a real dogfood run against
a genuine refactor this phase's own build actually produced (a duplicated
path-stem helper across two of this skill's own modules) that surfaced a
new category of finding: not a bug in this skill's own logic, but a real,
disclosed inconsistency in the composed upstream `codebase-intelligence`
data itself (L22 — `fan_in` undercounting a real caller). Also clarified an
instruction discrepancy before work began: the initial Phase 8 instruction
named "Architecture Decision," already built as Phase 7 — confirmed with
the user to mean the roadmap's actual next proposed skill, Refactoring
Safety, instead.

## What Phase 9 established

Reused Pattern 2 (ADR-007) for an eighth judgment-based skill and
`feature-planner`'s/`root-cause-analyzer`'s/`architecture-decision`'s/
`refactoring-safety`'s mandatory-composition rule (ADR-010) for a fifth
skill — both stated explicitly as *reuses*. Added a reusable Regression
Risk Checklist (10 categories) to [[05-evaluation-framework]], an eighth
checklist, coverage-shaped like the acceptance-coverage/Plan Quality/Root
Cause Investigation/Architecture Decision Record/Refactoring Safety
checklists. Established a new architectural decision (ADR-015): three
explicitly separate, non-blended regression signals per changed file
(diff-pattern flags scanned directly against the diff's own hunks — the
genuinely new deterministic-layer contribution, since no prior skill scans
a diff's hunks for regression shapes — plus structural blast radius and
test coverage, both reusing `refactoring-safety`'s pattern as independent
copies) are combined into one `overall_risk_tier` via a documented rule
table, rather than blended. Ran a real dogfood run against a genuine,
already-tested `codebase-intelligence` scanner fix this phase's own build
produced (excluding `*.egg-info` directories from repo scans) that
correctly scored the change as LOW risk on both real axes, and surfaced a
new cross-skill finding: not a bug in this skill's own new logic, but a
real, disclosed limitation shared between two skills' independent copies
of the same caller-identification heuristic (L23 — substring-based
matching inflating the caller list for short, common module stems).

## What Phase 10 established

Reused Pattern 2 (ADR-007) for a ninth judgment-based skill and
`feature-planner`'s/`root-cause-analyzer`'s/`architecture-decision`'s/
`refactoring-safety`'s/`regression-hunter`'s mandatory-composition rule
(ADR-010) for a sixth skill — both stated explicitly as *reuses*. Added a
reusable Release Readiness Checklist (10 categories) to
[[05-evaluation-framework]], a ninth checklist, coverage-shaped like the
acceptance-coverage/Plan Quality/Root Cause Investigation/Architecture
Decision Record/Refactoring Safety/Regression Risk checklists, but the
first to carry a non-negotiable framing category (verdict is advisory,
never an auto-gate) because this skill's output is this portfolio's single
highest-stakes recommendation. Established a new architectural decision
(ADR-016): the Release Readiness Scorecard — three always-available,
non-blended per-file signals (diff-hygiene flags, structural blast radius,
test coverage) combined into a `readiness_tier` via a documented rule
table, plus, for the first time in this portfolio, two OPTIONAL signals
composed from two OTHER skills' own real outputs (`regression-hunter`'s and
`security-context-guard`'s reports), surfaced verbatim but deliberately
excluded from the rule table so a different skill's already-rolled-up
verdict is never silently re-blended. Ran a real dogfood run against this
phase's own actual body of work (a real, staged-then-unstaged, never
committed `git diff` of all 78 new files) that confirmed a predicted
false-positive shape concretely (a legitimate CLI `print()` flagged as a
debug leftover) and surfaced a new, more consequential manifestation of the
L14/L19/L21/L23 substring-collision limitation class: `target_resolver.py`,
reused a third time, was shown to corrupt test-coverage matching, not just
caller-list display (L24).

## Immediate next decision point

**Superseded** — Phase 11 (`Dependency / Supply Chain`), Phase 12
(`Engineering Knowledge Capture`), Phase 13 (`Context Optimizer`), and
Phase 14 (`Workflow Composer`) all shipped 2026-08-26 at the user's
explicit direction (see [[active-context.md]] for the full account), not
because the independent-evidence gap (L8/A5) closed — Phase 14 also
directly overrode a named, phase-specific decision (A10) rather than only
the general freeze. Phase 15 onward remains frozen under the same rule
this section originally described: re-justify against real external
validation evidence before starting, not the next portfolio item by
default. The case for investing a phase in L8/A5 instead of a fifteenth
skill remains at least as strong as it was at the Phase 11, Phase 12,
Phase 13, and Phase 14 boundaries.
