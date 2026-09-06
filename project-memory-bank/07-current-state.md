# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to. Read
this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-29 — ADR-022 (Java/Kotlin multi-language support).
Phase 15 (`engineering-memory`, 2026-08-26) completed the originally-
scoped 15-skill portfolio named in [[08-roadmap]] — there is no Phase 16
in that list, and ADR-022 is NOT a new phase: it is user-directed,
cross-cutting scope touching `codebase-intelligence` and 5 downstream
skills (see [[11-decisions]] ADR-022), not a new skill. Test count rose
from 693 to 733; the other 9 skills are unchanged. See
[[active-context.md]] and [[implementation-status.md]] for anything more
recent than this rewrite._

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
skills/refactoring-safety/          Skill 8 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a fourth time), per-target risk tier + independent test-coverage signal (ADR-014)
skills/regression-hunter/           Skill 9 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a fifth time), three-axis non-blended regression-risk scoring (ADR-015)
skills/release-readiness/           Skill 10 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a sixth time), Release Readiness Scorecard (ADR-016), first skill also composing OPTIONALLY with two other skills' own reports
skills/dependency-supply-chain/     Skill 11 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a seventh time), pin/known-risk-name/duplicate-declaration signals (ADR-017) (Phase 11, 2026-08-26)
skills/engineering-knowledge-capture/  Skill 12 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused an eighth time), first skill whose deterministic layer targets a documentation artifact rather than a code-risk judgment (ADR-018) (Phase 12, 2026-08-26)
skills/context-optimizer/          Skill 13 — SKILL.md + Python engine + agent workflow, required composition (ADR-010, reused a ninth time), fail-OPEN-toward-inclusion inversion (ADR-019) (Phase 13, 2026-08-26)
skills/workflow-composer/          Skill 14 — SKILL.md + Python engine + agent workflow, first skill executing other skills' real code, required composition (ADR-010, reused a tenth time), fails CLOSED on execution uncertainty (ADR-020) (Phase 14, 2026-08-26)
skills/engineering-memory/         Skill 15 — SKILL.md + Python engine + agent workflow, first skill retrieving against this project's own memory bank (self-referential composition), required composition (ADR-010, reused an eleventh time) (ADR-021) (Phase 15, 2026-08-26, final skill in the originally-scoped portfolio)
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
evaluations/dependency-supply-chain/     Evaluation harness + 8 fixtures + RESULTS.md
evaluations/engineering-knowledge-capture/  Evaluation harness + 8 fixtures + RESULTS.md
evaluations/context-optimizer/           Evaluation harness + 8 fixtures + RESULTS.md
evaluations/workflow-composer/           Evaluation harness + 8 fixtures + RESULTS.md
evaluations/engineering-memory/          Evaluation harness + 8 fixtures + RESULTS.md
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
examples/dependency-supply-chain/        Dogfood run against this repo's own root manifest; confirmed the inherited L2 root-level-only scope gap, disclosed L25/L26
examples/engineering-knowledge-capture/  Dogfood run against a real narrative built from this project's own engineering history; disclosed L28
examples/context-optimizer/              Dogfood run: fresh codebase-intelligence report + a real task from this session; disclosed L29
examples/workflow-composer/              Dogfood run: a real, non-dry-run execution of understand-then-plan against this repo's own current state; disclosed L30
examples/engineering-memory/             Dogfood run: retrieval against this project's own actual 50-record memory bank + a fresh codebase-intelligence report; disclosed L31
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
03-architecture.md              updated through Phase 15 (Pattern 2 reused a fourteenth time, ADR-021 note)
04-skill-contract.md
05-evaluation-framework.md      updated through Phase 15 (Engineering Memory Retrieval Checklist, fourteenth checklist)
06-security-model.md
07-current-state.md             (this file — fully refreshed this pass, Phase 15)
08-roadmap.md                   updated through Phase 15 (Phase 15 COMPLETE; originally-scoped 15-skill portfolio now fully built, no Phase 16 in the list)
operating-charter.md            NEW 2026-08-26 — the previously-referenced-
                                 but-missing source document ADR-001 adopts
11-decisions.md                 updated through ADR-022 (Java/Kotlin support, 2026-08-29, not a new phase)
12-known-limitations.md         updated through L33 (ADR-022 follow-on, 2026-08-29)
16-assumptions-and-validation.md   updated through Phase 15 (A2, A5, A8, A10)
17-experiment-viability-check.md
implementation-status.md        updated through ADR-022 (733 total tests, all fifteen skills)
active-context.md               updated through ADR-022 (2026-08-29)
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
sprint-history/SPRINT-10.md
sprint-history/SPRINT-11.md
sprint-history/SPRINT-12.md
sprint-history/SPRINT-13.md
sprint-history/SPRINT-14.md
sprint-history/SPRINT-15.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no reusable
composed workflows yet), `10-ui-ux-principles.md` (no UI yet),
`13-lessons-learned.md`, `14-community-feedback.md`, `15-metrics.md` (no
external usage yet).

## What exists in practice

- **Fifteen skills implemented**, all Level 2 (Evaluated) per
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
  - `dependency-supply-chain` — deterministic pin-status/known-risk-name/
    duplicate-declaration/surface-area engine + agent-driven Dependency
    Risk Checklist workflow (Pattern 2, reused a tenth time), plus
    ADR-017: reuses `security-context-guard`'s advisory/fail-closed
    discipline, explicitly declines a live-vulnerability-DB feature (L25)
    and a per-dependency-license feature (L26, dropped mid-build once the
    data needed for it was confirmed not to exist). Reuses the
    mandatory-composition rule (ADR-010) a seventh time.
  - `engineering-knowledge-capture` — deterministic narrative-scanning
    engine (decision/lesson/limitation/workaround candidate detection) +
    agent-driven Knowledge Capture Checklist workflow (Pattern 2, reused
    an eleventh time), plus ADR-018: the first skill whose deterministic
    layer targets a documentation artifact rather than a code-risk
    judgment, and the first word-boundary-aware module resolver built
    correct from day one rather than shipped with the L23/L24 bug first.
    Reuses the mandatory-composition rule (ADR-010) an eighth time.
  - `context-optimizer` — deterministic task-relevance scoring engine
    (tokenized whole-token keyword match against path/docstring/
    functions/classes/imports, fan_in/hotspot-boosted) + agent-driven
    Context Optimization Checklist workflow (Pattern 2, reused a twelfth
    time), plus ADR-019: the headline decision is an explicit
    **inversion** of the fail-closed-toward-caution convention — this
    skill fails OPEN toward inclusion under uncertainty, because silently
    excluding a needed file is the worse failure for a context-
    recommendation tool. Reuses the mandatory-composition rule (ADR-010)
    a ninth time.
  - `workflow-composer` — the first skill whose deliverable is composed
    **execution**, not analysis: a small hardcoded registry of 3 workflow
    templates that subprocess-invokes other skills' real `engine/cli.py`
    entry points, with a compatibility-drift guard gating each step
    (Pattern 2, reused a thirteenth time), plus ADR-020: fails CLOSED on
    any step failure or compatibility issue — the opposite default from
    ADR-019 one phase earlier, both framed as the same underlying
    principle applied in opposite directions depending on which failure
    is cheaper to recover from. Reuses the mandatory-composition rule
    (ADR-010) a tenth time.
  - `engineering-memory` — the first skill whose primary retrieval corpus
    is this project's own `project-memory-bank/` markdown rather than a
    target repo's external artifacts (self-referential composition):
    deterministic parser/resolver/scorer engine over `11-decisions.md`/
    `12-known-limitations.md` + agent-driven Engineering Memory Retrieval
    Checklist workflow (Pattern 2, reused a fourteenth time), plus
    ADR-021: word-boundary/whole-token matching applied from day one
    (an accumulated lesson from six prior disclosed limitations, not a
    new discovery), and every match always carries an explicit staleness
    flag rather than silently trusting or silently dropping a stale
    record. Reuses the mandatory-composition rule (ADR-010) an eleventh
    time — the final skill in the originally-scoped 15-skill portfolio.
  Full detail in [[implementation-status.md]].
- **Fifteen evaluation harnesses**: codebase-intelligence (4 fixtures, all
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
  100%, judgment 100% precision/recall on all 8), dependency-supply-chain,
  engineering-knowledge-capture, context-optimizer, workflow-composer, and
  engineering-memory (8 fixtures each, same deterministic-100%/judgment-
  100% pattern). All fourteen judgment-layer evaluations carry the L8
  self-authored/single-rater caveat — now applying a fourteenth time.
- **733 total unit/integration tests** across fifteen skills (42 + 29 +
  24 + 21 + 58 + 32 + 34 + 65 + 70 + 84 + 55 + 47 + 64 + 51 + 57), all
  passing — up from 420 as of Phase 10, after a 2026-08-26 mentor-review
  follow-up (+8 tests fixing L23/L24), Phases 11-15's five new skills
  (+46, +47, +64, +51, +57 tests respectively), and a 2026-08-29
  cross-cutting change (ADR-022, NOT a new phase) adding Java/Kotlin
  support to `codebase-intelligence` and 5 downstream skills (+40 tests).
  See [[active-context.md]] for the current, authoritative breakdown.
- **Nine real bugs/gaps found and fixed via dogfooding**, not hypothetical:
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
  from 23 to 24. The 2026-08-26 mentor-review follow-up (before Phase 11)
  fixed a ninth: L23 in full, by replacing the bare substring check in
  `target_resolver.py` (shared across `refactoring-safety`/`regression-
  hunter`/`release-readiness`) with a word-boundary-aware match, and
  mitigated (not fully closed) L24 the same way in
  `test_coverage_scanner.py`. No dogfood run across Phases 11-15 found and
  fixed a new bug — each of those phases' real findings (L25/L26/L28/L29/
  L30/L31, below) was disclosed and deliberately left unfixed, the same
  "disclose, don't guess a fix from one data point" discipline applied
  consistently since L14. See [[12-known-limitations]].
- **Six real limitations found via dogfooding and deliberately left
  unfixed** (plus L24, mitigated but not fully closed — above), the same
  coincidental-keyword/substring-collision mechanism class recurring across
  independent skills and corpora: L14 — `feature-planner`'s relevance
  scorer ranked the true target file 13th (not 1st) in a real dogfood run;
  the agent's Step 3 judgment correctly identified the right file anyway.
  L21 (Phase 7) — the same mechanism at full-repo scale. L23 (Phase 9,
  later fixed — above) — `target_resolver.py`'s substring-based caller
  identification inflated the caller list for a short, common module stem.
  L24 (Phase 10, mitigated not fixed) — the same pattern corrupting test-
  coverage matching, not just caller-list display. L28 (Phase 12) —
  `engineering-knowledge-capture`'s location resolver only checks the
  matched line, not the surrounding paragraph, missing a real module
  mention named four times in the prior sentence. L29 (Phase 13) —
  `context-optimizer`'s tokenized scorer still floods with false-positive
  CORE recommendations at full-repository scale when the task description
  uses this project's own recurring vocabulary. L30 (Phase 14) —
  `workflow-composer` composing with `feature-planner` inherits the same
  scorer's flooding unfiltered, confirming the mechanism lives in the
  oldest relevance engine in the portfolio, not just newer copies. L31
  (Phase 15) — a genuinely different ambiguity from the same resolver
  family: `engineering-memory`'s basename-exact module resolution (built
  correct from day one specifically to defeat the substring-collision
  class) collapses multiple real, distinct same-basename files across the
  portfolio into one arbitrarily-chosen match — a "multiple TRUE matches"
  ambiguity, not a "FALSE match via containment."
- **A fifth judgment-based skill evaluated the same way as the first
  four — and the first to break the perfect-score pattern**:
  root-cause-analyzer scored 7/8 fixtures perfect and 1/8 (case-03) at
  0.67/0.67 precision/recall against self-authored ground truth (L19 in
  [[12-known-limitations]]), disclosed as-is rather than adjusted.
  architecture-decision (the sixth), refactoring-safety (the seventh),
  regression-hunter (the eighth), release-readiness (the ninth),
  dependency-supply-chain (the tenth), engineering-knowledge-capture (the
  eleventh), context-optimizer (the twelfth), workflow-composer (the
  thirteenth), and engineering-memory (the fourteenth) all returned to a
  perfect 8/8 score — stated plainly as *not* evidence of higher judgment
  quality, since a single self-authored evaluation cannot support that
  comparison. Neither a perfect score nor an imperfect one, on
  self-authored single-rater fixtures, is evidence of real-world quality.
  Disclosed explicitly in all fourteen skills' `RESULTS.md` and `SKILL.md`.
- **First skill with mandatory (not optional) composition**: `feature-
  planner` (ADR-010, Phase 4) — now joined by `root-cause-analyzer` (Phase
  6), `architecture-decision` (Phase 7), `refactoring-safety` (Phase 8),
  `regression-hunter` (Phase 9), `release-readiness` (Phase 10),
  `dependency-supply-chain` (Phase 11), `engineering-knowledge-capture`
  (Phase 12), `context-optimizer` (Phase 13), `workflow-composer` (Phase
  14), and `engineering-memory` (Phase 15), the eleventh skill to adopt
  the same rule.
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
- **First skill whose deterministic layer targets a documentation
  artifact rather than a code-risk judgment**: `engineering-knowledge-
  capture` (ADR-018, Phase 12) — scans a free-text engineering narrative
  for decision/lesson/limitation/workaround candidates, the first word-
  boundary-aware module resolver in this portfolio built correct from day
  one rather than shipped with the substring-collision bug first.
- **First skill to invert the fail-closed-toward-caution convention**:
  `context-optimizer` (ADR-019, Phase 13) — fails OPEN toward inclusion
  under uncertainty instead, because for a context-recommendation tool,
  silently excluding a needed file is the worse failure, not silently
  including an unimportant one.
- **First skill whose deliverable is composed execution, not analysis**:
  `workflow-composer` (ADR-020, Phase 14) — subprocess-invokes other
  skills' real `engine/cli.py` entry points via a small hardcoded registry
  of 3 workflow templates, gated by a compatibility-drift guard, failing
  CLOSED on any step failure — the opposite default from ADR-019 one
  phase earlier, both the same underlying "fail toward the cheaper-to-
  recover-from error" principle pointing in opposite directions.
- **First skill whose primary corpus is this project's own memory bank,
  not a target repo's artifacts**: `engineering-memory` (ADR-021, Phase
  15) — retrieves against `11-decisions.md`/`12-known-limitations.md`
  directly, applying word-boundary matching from day one as an
  accumulated lesson from six prior disclosed limitations, and always
  attaches an explicit staleness flag rather than silently trusting or
  silently dropping a stale record — the final skill in the originally-
  scoped 15-skill portfolio.
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
  any of the fifteen skills (as of Phase 15, the originally-scoped
  portfolio's completion). Assumptions A2/A3/A5/A7/A8/A10 have partial
  (synthetic, self-authored, or single-pilot/single-architecture) evidence
  only — not real-world validation, not independent-rater validation.
- **One reusable multi-skill composed-workflow registry now exists**
  (`workflow-composer`, Phase 14) — 3 hardcoded templates that really
  execute other skills' own `engine/cli.py` code, still no general-purpose
  or user-authored composed-workflow infrastructure beyond that fixed
  registry. Zero UI, zero product code beyond these fifteen skills and
  that one composition layer.

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

## What Phase 11 established

Reused Pattern 2 (ADR-007) for a tenth judgment-based skill and the
mandatory-composition rule (ADR-010) a seventh time — both stated
explicitly as *reuses*. Added a reusable Dependency Risk Checklist (10
categories) to [[05-evaluation-framework]], a tenth checklist,
decision-gate shaped like the Security checklist. Established a new
architectural decision (ADR-017): `dependency-supply-chain` reuses
`security-context-guard`'s advisory/fail-closed discipline and explicitly
declines two features — a live-vulnerability-DB lookup (L25, a permanent
scope decision) and per-dependency license-risk detection (L26, dropped
*mid-build* once it became clear a manifest's `license` field describes
the project's own license, not each dependency's, and no such data is
actually available from what `codebase-intelligence` parses — naming the
gap explicitly rather than shipping a fabricated-looking flag). Ran a real
dogfood run against this repo's own root manifest, found only one real
dependency (`pytest`), concretely confirming the inherited L2
root-level-only scope gap (the platform's real per-skill dependencies live
in `skills/*/pyproject.toml`, one level below repo root). 46 tests.
Platform test count rose from 428 to 474.

## What Phase 12 established

Reused Pattern 2 (ADR-007) for an eleventh judgment-based skill and
ADR-010 an eighth time — both stated explicitly as *reuses*. Added a
reusable Knowledge Capture Checklist (11th checklist). Established a new
architectural decision (ADR-018): `engineering-knowledge-capture` is the
first skill in the portfolio whose deterministic layer targets a
documentation artifact (a decision/lesson/limitation/workaround
candidate) rather than a code-risk judgment, and the fourth independent
copy of the word-boundary-aware resolution fix first applied after
L23/L24 — this one built correct from day one rather than shipped with
the bug first. Ran a real dogfood run against a narrative built from
genuine excerpts of this project's own engineering history (the L23/L24
fix, Phase 11's dropped license-detection decision) and found L28:
`location_resolver.py` only checks the exact matched line for a module
mention, not the surrounding paragraph, so every candidate in that real
run resolved to no location at all despite `target_resolver.py` being
named four times in the sentence immediately above — the first dogfood
finding in this project's history about a gap between synthetic-fixture
behavior and real-prose behavior specifically. 47 tests. Platform test
count rose from 474 to 521.

## What Phase 13 established

Reused Pattern 2 (ADR-007) for a twelfth judgment-based skill and ADR-010
a ninth time — both stated explicitly as *reuses*. Added a reusable
Context Optimization Checklist (12th checklist). Established a new
architectural decision (ADR-019): `context-optimizer`'s relevance scorer
is the fifth independent copy of the containment-check lineage and the
second built correct from day one, using tokenization rather than
`location_resolver.py`'s `\b`-regex (a deliberate, disclosed
precision/recall tradeoff); the headline decision is an explicit
**inversion** of the fail-closed-toward-caution convention — this skill
fails **OPEN** toward inclusion under uncertainty instead, because for a
context-recommendation tool, silently excluding a needed file is the
worse failure. Ran a real dogfood run against this repo's own current
state with a real task description from this session's own work and
found L29: at full-repository scale, keyword relevance still floods with
false-positive CORE recommendations when the task description is phrased
in this project's own recurring vocabulary — the second time the
coincidental-keyword-collision mechanism class was hit on a real dogfood
run without either project acting on it. 64 tests. Platform test count
rose from 521 to 585.

## What Phase 14 established

Reused Pattern 2 (ADR-007) for a thirteenth judgment-based skill and
ADR-010 a tenth time — both stated explicitly as *reuses*. Added a
reusable Workflow Composition Checklist (13th checklist). Established a
new architectural decision (ADR-020): `workflow-composer` is the first
skill in the portfolio whose deliverable is composed **execution**, not
analysis — a small, hardcoded registry of exactly 3 workflow templates
that subprocess-invokes other skills' real `engine/cli.py` entry points,
gated by a compatibility-drift guard confirming each step's declared
upstream marker still appears in the downstream skill's real `SKILL.md`;
fails **CLOSED** on any step failure or compatibility issue — the
opposite default from ADR-019 one phase earlier, both framed as the same
underlying "fail toward the cheaper-to-recover-from error" principle
pointing in opposite directions depending on which failure is expensive.
51 tests, including one genuinely real subprocess-based integration test
— no prior skill's test suite invokes another skill's real code. Ran a
real, non-dry-run execution of `understand-then-plan` against this
repo's own current state; both steps succeeded, and found L30:
`feature-planner`'s own relevance scorer (composed, not computed by
`workflow-composer` itself) ranked a test file as the single
highest-scoring file in the entire repository — confirming the
coincidental-keyword-collision mechanism class lives inside
`feature-planner` itself, the oldest relevance engine in this portfolio,
not just newer copies. Platform test count rose from 585 to 636.

## What Phase 15 established

Reused Pattern 2 (ADR-007) for a fourteenth judgment-based skill and
ADR-010 an eleventh time — the final skill in the originally-scoped
15-skill portfolio. Added a reusable Engineering Memory Retrieval
Checklist (14th checklist). Established a new architectural decision
(ADR-021): `engineering-memory` is the first skill whose primary
retrieval corpus is this project's own `project-memory-bank/` markdown
rather than a target repo's external artifacts — a new "self-referential
composition" category. Parses real `## ADR-NNN:`/`## LNN:` section
headers out of `11-decisions.md`/`12-known-limitations.md` (explicitly
skipping `## L8 update:` sub-entries), resolves any module mentioned in a
record's body against a required `codebase-intelligence` report via
basename-EQUALITY, scores each record against a task description's
whole-token keyword overlap, and always attaches a staleness flag derived
from a record's own `(FIXED...)`/`(SUPERSEDED...)` title suffix or a
mentioned module no longer resolving — the direct, operational answer to
A8's own named risk about stale memory being treated as authoritative.
Word-boundary/whole-token matching was applied from day one specifically
because six prior disclosed limitations (L14/L19/L21/L23/L24/L28/L29/L30)
already proved the substring-containment alternative fails — applying an
accumulated lesson, not discovering a new one. 57 tests, including a real
end-to-end integration test. Ran a real, non-fixture retrieval run against
this project's own actual 50-record memory bank and a freshly-generated
real `codebase-intelligence` report; 8/8 top matches were substantively
on-topic and both real staleness signals fired correctly, but found L31:
`module_resolver.py`'s basename-exact resolution, built correct from day
one specifically to defeat the substring-collision class, has a
different, real ambiguity once the corpus is this project's actual
many-skill memory bank — `ci_report_loader.py` (a real, distinct file in
most composing skills) caused five different records about five
different skills to all resolve their mention to the same single
arbitrarily-chosen path. A genuinely different failure mode than the
substring class this resolver already defeats, not a sign that defeat
was incomplete. Platform test count rose from 636 to **693**, zero
regressions. **This completes the originally-scoped 15-skill portfolio
named in [[08-roadmap]] — there is no Phase 16 in that list.**

## Immediate next decision point

**Superseded** — Phase 11 (`Dependency / Supply Chain`), Phase 12
(`Engineering Knowledge Capture`), Phase 13 (`Context Optimizer`), Phase
14 (`Workflow Composer`), and Phase 15 (`Engineering Memory`) all shipped
2026-08-26 at the user's explicit direction (see [[active-context.md]]
for the full account), not because the independent-evidence gap (L8/A5)
closed — Phase 14 also directly overrode a named, phase-specific decision
(A10) rather than only the general freeze; Phase 15's own gating decision
(A8) was satisfied simply by being reached in order, so it did not need
that same kind of override. **Phase 15 completes the originally-scoped
15-skill portfolio — there is no Phase 16 in [[08-roadmap]]'s list.** Any
further skill work is a newly-proposed scope under the same rule this
section originally described: re-justify against real external
validation evidence before starting, not "the next portfolio item" by
default, since there no longer is one. The case for investing a phase in
L8/A5 instead of building further remains at least as strong as it was at
the Phase 11 through Phase 15 boundaries.
