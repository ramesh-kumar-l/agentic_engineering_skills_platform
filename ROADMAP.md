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
Phase 12 onward remains frozen. See
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
