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

**Phase 8 — Refactoring Safety** (complete): eighth skill —
`skills/refactoring-safety/` — reusing the same pattern a seventh time to
turn a refactoring description into a per-target risk assessment against a
real dependency graph plus an independently-computed test-coverage signal,
evaluated on 8 fixtures (all 8 scored perfect on both layers) plus a real
dogfood run against a genuine refactor this phase's own build produced
(extracting a duplicated helper). New this phase: **ADR-014** — a target's
structural risk tier is kept as a field distinct from its test-coverage
status, rather than blended into one score — and this skill reuses Phase
4's mandatory-composition rule (ADR-010) a fourth time. The real dogfood
run disclosed — without fixing — a new cross-skill limitation: `codebase-
intelligence`'s own `fan_in` metric undercounted a real caller that this
skill's own independent caller scan found correctly. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Phase 9 — Regression Hunter** (complete): ninth skill —
`skills/regression-hunter/` — reusing the same pattern an eighth time to
turn a unified git diff into a per-file regression-risk assessment,
evaluated on 8 fixtures (all 8 scored perfect on both layers) plus a real
dogfood run against a genuine diff this phase's own build produced. New
this phase: **ADR-015** — regression risk is scored from three explicit,
non-blended signals per changed file (diff-pattern flags like removed
exception handling or a removed conditional guard; structural blast radius
from real fan-in/hotspot data, ADR-013-style; and an independently-computed
test-coverage signal, ADR-014-style) combined into an overall tier via a
documented rule table, with all three axes still visible separately in the
report — and this skill reuses Phase 4's mandatory-composition rule
(ADR-010) a fifth time. The real diff dogfooded was a genuine `codebase-intelligence` fix from this
phase's own build (excluding `*.egg-info` directories from repo scans), and
running it through the skill disclosed — without fixing — a new limitation
(L23): `target_resolver.py`'s substring-based caller matching produces a
wildly inflated caller list for short, common module stems like `scanner`,
the same limitation class as L14/L19/L21 now shown to affect two skills'
independent copies of the same heuristic at once. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Phase 10 — Release Readiness** (complete): tenth skill, the final skill
in the Engineering Lifecycle group — `skills/release-readiness/` — reusing
the same pattern a ninth time to turn a git diff into a per-file Release
Readiness Scorecard, evaluated on 8 fixtures (all 8 scored perfect on both
layers) plus a real dogfood run against this phase's own actual body of
work (a real, staged-then-unstaged, never-committed diff of all 78 new
files). New this phase: **ADR-016** — three always-available, non-blended
per-file signals (diff-hygiene flags, structural blast radius, test
coverage) combine into a `readiness_tier` via a documented rule table,
rolling up into one advisory-only `overall_verdict`; two further, OPTIONAL
signals — surfaced (never re-derived) from a supplied `regression-hunter`
or `security-context-guard` report — are the first cross-skill-report
composition in this platform, deliberately excluded from the rule table.
This skill also reuses Phase 4's mandatory-composition rule (ADR-010) a
sixth time. The real dogfood run confirmed an already-documented
false-positive shape concretely (a legitimate CLI `print()` flagged as a
debug leftover) and disclosed — without fixing — a sharper, more
consequential version of the L14/L19/L21/L23 limitation class: the same
substring-based `target_resolver.py` pattern, reused a third time, was
shown to produce false-positive test coverage, not just an inflated caller
list (L24). See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md).

**Phase 11 — Dependency / Supply Chain** (complete): eleventh skill —
`skills/dependency-supply-chain/` — reusing the same pattern a tenth time
to scan a repo's declared dependencies for pin status, known-risk names,
duplicate/conflicting version declarations, and surface area, evaluated on
8 fixtures (all 8 scored perfect on both layers) plus a real dogfood run
against this repo's own root manifest. New this phase: **ADR-017** —
composing on `codebase-intelligence`'s output a seventh time (ADR-010), and
two explicit scope decisions rather than silent gaps: no live CVE/
vulnerability-database lookup (this project makes no network calls,
ADR-006), and no per-dependency license-risk detection (dropped
mid-implementation once it became clear the data needed doesn't exist in
what's parsed — a manifest's `license` field describes the *project's*
license, not each dependency's). The real dogfood run against this repo's
own root manifest concretely confirmed a pre-known scope limitation: only 1
of the platform's actual dependencies (`pytest`) was visible, because the
platform's own real per-skill dependencies live one level below repo root.
**Process note**: earlier the same day, a mentor-style review of this
project's own progress (zero real external users after ten phases) froze
the roadmap pending real validation evidence; Phase 11 started anyway at
the user's explicit direction — a one-time exception, not new evidence.

**Phase 12 — Engineering Knowledge Capture** (complete): twelfth skill —
`skills/engineering-knowledge-capture/` — reusing the same pattern an
eleventh time to scan a free-text engineering narrative for decision/
lesson/limitation/workaround candidates, resolving any mentioned module
against real structural data (fan_in/hotspot), evaluated on 8 fixtures
(all 8 scored perfect on both layers) plus a real dogfood run against a
narrative built from genuine excerpts of this project's own engineering
history. New this phase: **ADR-018** — composing on
`codebase-intelligence`'s output an eighth time (ADR-010); the location
resolver is the fourth independent copy of the word-boundary-aware fix
first applied after L23/L24, and the first one built correct from the
start; and this is the first skill in the portfolio whose deterministic
layer targets a documentation artifact (an ADR/known-limitation/
lessons-learned candidate) rather than a code-risk judgment. The real
dogfood run found a new, disclosed-not-fixed limitation (L28): the
resolver only checks the exact matched line for a module mention, not the
surrounding paragraph, so every candidate in that real run resolved to no
location despite the relevant module being named four times nearby.
**Process note**: this is a SECOND same-day reopening of the same
mentor-review freeze, at the user's explicit direction — again a one-time
exception, not new evidence, and not precedent that the freeze auto-lifts
generally. Phase 13 onward remains frozen. See
[`project-memory-bank/active-context.md`](project-memory-bank/active-context.md).

**Phase 13 — Context Optimizer** (complete): thirteenth skill —
`skills/context-optimizer/` — reusing the same pattern a twelfth time to
score every file in a required `codebase-intelligence` report against a
free-text task description's keywords (a tokenized, not `\b`-regex,
whole-token match — a deliberate, disclosed different technique than
Phase 12's resolver), boosted by real fan_in/hotspot data, tiered
CORE/SUPPORTING/EXCLUDED against an optional line budget, evaluated on 8
fixtures (all 8 scored perfect on both layers) plus a real dogfood run
against a task description drawn from this actual session. New **ADR-019**
— composing on `codebase-intelligence`'s output a ninth time (ADR-010),
and an explicit inversion of the fail-closed-toward-caution convention
ADR-011/017/018 established into a fail-OPEN-toward-inclusion default,
since silently excluding a needed file is this skill's worse failure
mode. The real dogfood run found a new, disclosed-not-fixed limitation
(L29): at full-repository scale, keyword relevance floods with
false-positive CORE recommendations when the task description shares
this project's own recurring documentation/evaluation-harness vocabulary
— a new manifestation of the same mechanism class `architecture-
decision`'s L14/L19/L21 already disclosed.
**Process note**: this is a THIRD same-day reopening of the same
mentor-review freeze, at the user's explicit direction — again a one-time
exception, not new evidence, and not precedent that the freeze auto-lifts
generally, now deferred across three consecutive phase boundaries. Phase
14 onward remains frozen. See
[`project-memory-bank/active-context.md`](project-memory-bank/active-context.md).

**Phase 14 — Workflow Composer** (complete): fourteenth skill —
`skills/workflow-composer/` — reusing the same pattern a thirteenth time,
but the first skill whose deliverable is composed **execution**, not
analysis: subprocess-runs a small, hardcoded registry of exactly 3
workflow templates (each reusing a composition this project already ran
for real in an earlier phase's dogfood — Phase 4's, Phase 3's real Pilot
B, and Phase 13's), every one rooted in a required
`codebase-intelligence` report (ADR-010, tenth reuse), evaluated on 8
fixtures (all 8 scored perfect on both layers) plus a real, non-dry-run
execution against this repo's own current state. New **ADR-020** —
composing on `codebase-intelligence`'s output a tenth time, and an
explicit fail-**CLOSED** default on execution uncertainty (a
compatibility-check drift blocks all real execution outright; any step's
failure stops the chain) — the opposite default from Phase 13's ADR-019,
reconciled explicitly as the same underlying principle landing on the
normal side because the cheaper error points the other way in this
domain. The real run found a new, disclosed-not-fixed limitation (L30):
the composed `feature-planner` step's own relevance scorer ranked a test
file above every real implementation file relevant to the task — the
same mechanism class `architecture-decision`'s L14/L19/L21 and
`context-optimizer`'s L29 already disclosed, now confirmed present inside
`feature-planner` itself.
**Process note**: this is a FOURTH same-day reopening of the same
mentor-review freeze, at the user's explicit direction, and the FIRST to
also directly override a named, phase-specific decision on record
(`16-assumptions-and-validation.md` A10's "do not build Workflow Composer
until Experiment B can be run") — again a one-time exception, not new
evidence, and not precedent that the freeze or a named decision
auto-lifts generally, now deferred across four consecutive phase
boundaries. Phase 15 onward remains frozen. See
[`project-memory-bank/active-context.md`](project-memory-bank/active-context.md).

**Phase 15 — Engineering Memory** (complete): fifteenth and **final**
skill in the originally-scoped portfolio — `skills/engineering-memory/`
— reusing the same pattern a fourteenth time, and the first skill whose
primary retrieval corpus is this project's own memory bank
(`11-decisions.md`, `12-known-limitations.md`), not a target repo's
external artifacts: parses real ADR/limitation section headers, resolves
mentioned modules against a required `codebase-intelligence` report
(ADR-010, eleventh reuse) via basename equality, scores whole-token
keyword overlap against a task description, and always attaches a
staleness flag rather than presenting a FIXED or module-gone record as
current guidance, evaluated on 8 fixtures (all 8 scored perfect on both
layers) plus a real, non-fixture retrieval run against this project's own
actual 50-record memory bank. New **ADR-021** — composing on
`codebase-intelligence`'s output an eleventh time, and the first
"self-referential composition"; word-boundary/whole-token matching
applied from day one because six prior disclosed limitations already
proved the substring-containment alternative fails. The real run found a
new, disclosed-not-fixed limitation (L31): basename-exact module
resolution collapses distinct real files sharing a common basename
(`ci_report_loader.py`, real in most composing skills) into the same
single, arbitrarily-chosen resolved path — a different failure mode from
the substring-collision class this resolver was already built to defeat.
**Process note**: this is a FIFTH same-day reopening of the same
mentor-review freeze, at the user's explicit direction — unlike Phase 14,
this one does not override a named, phase-specific decision
(`16-assumptions-and-validation.md` A8's "design only when reached" gate
was satisfied by reaching Phase 15 in order) — again a one-time exception
to the general freeze, not new evidence, now deferred across five
consecutive phase boundaries. **This completes the originally-scoped
15-skill portfolio — there is no Phase 16 on this list.** Any further
skill work is a newly-proposed scope, still requiring re-justification
against real external validation evidence. See
[`project-memory-bank/active-context.md`](project-memory-bank/active-context.md).

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
