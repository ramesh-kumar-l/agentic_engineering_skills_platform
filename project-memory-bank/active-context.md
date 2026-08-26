# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 12 (`engineering-knowledge-capture`) — COMPLETE. **Phase 13 onward
remains frozen.** 2026-08-26 (same day, four sub-events): (1) the user
requested a mentor-style critique of the whole project, which found ten
phases shipped, zero real external users, A2/A5 still UNKNOWN, and the
L23/L24 substring bug disclosed four times without being fixed — the user
approved pausing new-skill work to fix that bug and scaffold a measurement
harness instead (see "Mentor-review follow-up" below); (2) the user then
explicitly directed starting Phase 11 anyway, with their own exit criteria
("same bar," first skill composing on `codebase-intelligence`'s output,
"production-level stable") — **this reopened the freeze at the user's
explicit direction, not because A2/A5 moved off UNKNOWN**; (3) Phase 11
shipped, and the operating charter was checked in as a documentation-only
pass (see "Documentation check-in" below); (4) the user then explicitly
directed starting Phase 12, with the same shape of exit criteria — **a
second, one-time reopening of the same freeze**, and Phase 12 shipped (see
"What Phase 12 built" below). The freeze remains in force for any phase
beyond 12 — starting Phase 11 and Phase 12 were each one-time, explicit
exceptions, not a general unfreezing.

## Documentation check-in (2026-08-26, after Phase 11 — not a new phase)

The user pasted the full "operating charter" (north-star vision, thesis,
principles, target users, skill portfolio, canonical skill contract,
assumption-tracking methodology) that ADR-001 has adopted since Phase 0 but
that had never actually been checked into the repo. Confirmed by the user as
complete. Filed at [[operating-charter]], cross-linked from ADR-001,
`00-project-vision.md`, `01-product-thesis.md`, and every file that already
cited "the operating charter" by name. One honest gap surfaced and disclosed
rather than papered over: several existing files cite charter sections
(39–40, 43, "First Activation") that don't exist in this version, which only
runs through Section 11 — see [[12-known-limitations|L27]]. No code, tests,
or roadmap changed; Phase 12+ freeze is untouched by this.

## What Phase 12 built

Built `engineering-knowledge-capture`, the twelfth skill: `SKILL.md`
contract reusing Pattern 2 (ADR-007) an eleventh time — a deterministic
engine (9 modules, each under 130 lines) that scans a free-text
engineering narrative for four candidate categories (decision, lesson,
limitation, workaround; 16 patterns total, non-exhaustive), resolves any
module mentioned on the matched line against a required `codebase-
intelligence` report (ADR-010, reused an eighth time), and rolls a
resolved candidate's real fan_in/hotspot data into an advisory
`suggested_capture_priority` (HIGH/MEDIUM — LOW is defined but never
assigned this version, a deliberate fail-upward choice under uncertainty).
New **ADR-018** documents the required-composition reuse, the fourth
independent copy of the word-boundary-aware resolution fix first applied
after L23/L24 — this one built correct from day one rather than shipped
with the bug first — and this skill's status as the first in the
portfolio whose deterministic layer targets a documentation artifact (an
ADR/known-limitation/lessons-learned candidate) rather than a code-risk
judgment. New **Knowledge Capture Checklist** (eleventh checklist,
[[05-evaluation-framework]], decision-gate shaped like the Security and
Dependency Risk checklists). 47 passing tests (CLI test file from the
start). 8-fixture evaluation harness, both layers scored perfect —
eleventh judgment-based skill scored this way, same self-authored caveat
(L8). Real dogfood (`examples/engineering-knowledge-capture/example-run.md`)
against a narrative built from genuine excerpts of this project's own
engineering history (the L23/L24 fix, Phase 11's dropped license-detection
decision) found a new, disclosed-not-fixed limitation: **L28** —
`location_resolver.py` only checks the exact matched line for a module
mention, not the surrounding paragraph, so every candidate in that real
run resolved to no location at all despite `target_resolver.py` being
named four times in the sentence immediately above the flagged markers.
This is the first dogfood run in this project's history whose finding is
about a gap between synthetic-fixture behavior and real-prose behavior
specifically (every evaluation fixture deliberately puts the module
mention in the same sentence as the marker; real retrospective writing
often doesn't). Platform test count rose from 474 to **521**, zero
regressions. `.github/workflows/tests.yml`'s matrix updated to include the
new skill.

## What Phase 11 built

Built `dependency-supply-chain`, the eleventh skill: `SKILL.md` contract
reusing Pattern 2 (ADR-007) a tenth time — a deterministic engine (11
modules, each under 100 lines) that reuses a required `codebase-
intelligence` report's `external_dependencies` field (ADR-010, reused a
seventh time) and produces four explicit signals — pin status (missing/
wildcard/range/pinned, covering both pip- and npm-style specifiers), a
5-entry curated known-risk-name table (each citing a real public incident,
exact-name matched, not substring), duplicate/conflicting version
declarations across manifests, and surface-area stats — rolled into one
advisory, fail-closed `suggested_risk_level` (CLEAR/NEEDS_REVIEW/
REQUIRES_REVIEW), reusing `security-context-guard`'s ADR-011 discipline.
**Corrected mid-implementation**: the original plan included a
`license_patterns.py` module for per-dependency license-risk detection;
this was dropped once it became clear a manifest's `license` field
describes the *project's* license, not each dependency's, and no such data
is actually available from what `codebase-intelligence` parses — shipping
a fabricated-looking license flag was rejected in favor of naming the gap
explicitly (L26). 46 passing tests (CLI test file from the start). New
**ADR-017** documents both the required-composition reuse and the two
explicit scope decisions (no live CVE lookup, no license-risk detection).
New **Dependency Risk Checklist** (tenth checklist,
[[05-evaluation-framework]], decision-gate shaped like the Security
checklist). 8-fixture evaluation harness, both layers scored perfect —
tenth judgment-based skill scored this way, same self-authored caveat (L8).
Real dogfood (`examples/dependency-supply-chain/example-run.md`) against
this repo's own root manifest found only 1 real dependency (`pytest`),
concretely confirming the inherited L2 root-level-only scope gap (the
platform's real per-skill dependencies live in `skills/*/pyproject.toml`,
one level below repo root). New known limitations L25 (no live CVE
database, permanent scope decision) and L26 (no per-dependency license
data, corrected-during-build scope decision). Platform test count rose
from 428 to **474**, zero regressions. `.github/workflows/tests.yml`'s
matrix updated to include the new skill.

## Mentor-review follow-up (2026-08-26, before Phase 11)

1. **Fixed L23 fully, L24 partially** — replaced the bare substring check
   (`target_stem in imports_text`) with a word-boundary-aware match
   (`\b<stem>\b`) in `refactoring-safety/engine/target_resolver.py`,
   `regression-hunter/engine/target_resolver.py`,
   `release-readiness/engine/target_resolver.py`, and
   `release-readiness/engine/test_coverage_scanner.py`. This closes the
   embedded-substring collision class (e.g. "scanner" inside
   "testability_scanner") that L23 fully described. It does **not** close
   L24's headline example — two different skills each legitimately
   importing their own identically-stemmed `models.py` still produces a
   real, boundary-respecting match, since the resolver has no notion of
   "same skill" path scoping. See `12-known-limitations.md`'s updated L23
   (FIXED) and L24 (PARTIALLY fixed, narrowed scope) entries for the exact
   distinction — do not read this as L24 being closed. 8 new regression
   tests added (2 refactoring-safety, 2 regression-hunter, 4
   release-readiness); platform test count rose from 420 to **428**, all
   passing, zero regressions.
2. **Scaffolded `evaluations/usage-comparison/`** — a before/after
   token/turns/time measurement harness, the first artifact in this project
   that can log a real task run both with a skill and with plain prompting.
   Ships empty (no fabricated numbers); see its README for the same
   self-run-pilot honesty caveat every other harness here carries.

Both items were the "purely technical" half of a broader checklist the
mentor critique produced (see the session's chat history / plan file for
the full checklist) — the remaining items (get one real external user, run
an independent/blind eval pass, actually log real usage-comparison runs)
require the user's own action outside this session and were explicitly
left to them.

## Prior phase summary (historical)

## What Phase 10 built

Built `release-readiness`, the tenth skill and the final skill in the
Engineering Lifecycle group: `SKILL.md` contract reusing Pattern 2
(ADR-007) a ninth time — a deterministic engine (16 modules, each under
300 lines, max 211) that parses a unified git diff (independent copy of
`regression-hunter`'s/`adversarial-diff-reviewer`'s parsing conventions)
into structured per-file hunks, scans those hunks directly for four
mechanically-detectable, release-blocking diff-hygiene shapes (debug
leftovers, merge-conflict markers, hardcoded-secret-shaped literals,
TODO-blocking markers), resolves each changed file against a real
`codebase-intelligence` report (a THIRD independent copy of
`refactoring-safety`'s/`regression-hunter`'s `target_resolver.py`
pattern), checks an independently-computed test-coverage signal, and
combines these three ALWAYS-AVAILABLE axes into one `readiness_tier` per
file via a documented rule table. Two FURTHER axes — a supplied
`regression-hunter` report's `overall_risk_tier` and a supplied
`security-context-guard` report's `suggested_verdict` — are OPTIONAL,
loaded via `--regression-report`/`--security-report`, surfaced verbatim,
and deliberately excluded from the rule table. Per-file tiers roll up into
one report-level `overall_verdict`
(`NOT_READY`/`READY_WITH_CONDITIONS`/`READY`), explicitly and repeatedly
framed everywhere as a recommendation for a human to review, never an
autonomous release gate. 78 passing tests, including a CLI test file
written from the start (same discipline Phases 5-9 established). Combined
with an agent-driven Release Readiness Checklist workflow — a new, ninth
checklist in [[05-evaluation-framework]] (10 categories: scope stated
precisely, diff-hygiene blockers reviewed as absolute, structural blast
radius grounded in real data, test coverage distinguished per file,
regression/security evidence surfaced-not-re-derived when present and
explicitly marked absent when not, overall verdict explained via the rule
table, false-positive check, evidence cited, assumption flag, and a
non-negotiable tenth category — verdict framed as advisory/human-
checkpoint, never an auto-gate — unique to this checklist because this
skill's output is this portfolio's single highest-stakes recommendation).

**Architecture**: reuses `feature-planner`'s/`root-cause-analyzer`'s/
`architecture-decision`'s/`refactoring-safety`'s/`regression-hunter`'s
mandatory-composition rule (ADR-010) a sixth time — a missing/malformed
`codebase-intelligence` report is a hard failure, not a degraded path,
stated explicitly as a *reuse*. New this phase: **ADR-016** — the Release
Readiness Scorecard combines three always-available, non-blended per-file
signals into a `readiness_tier` via a documented rule table (any hygiene
flag -> blocked; high structural tier with no coverage -> blocked; high or
medium structural tier, or no coverage -> needs-review; otherwise clear),
and is the FIRST skill in this platform to also compose OPTIONALLY with
TWO OTHER skills' own real outputs (not just `codebase-intelligence`'s) —
reusing `security-context-guard`'s ADR-011 optional-composition precedent
for those two specifically, rather than ADR-010's mandatory rule. The
optional evidence is surfaced but deliberately never blended into the rule
table, since each is already a rolled-up verdict from a DIFFERENT skill's
own rule table, and re-blending it would hide which skill produced which
judgment.

**Evaluation**: an 8-fixture harness (`evaluations/release-readiness/`),
same two-layer scoring (deterministic + judgment) as Phases 2-9. This is
the **ninth** judgment-based skill evaluated with self-authored,
single-rater fixtures. All 8 fixtures scored perfect precision/recall on
both layers — stated plainly as *not* evidence of higher judgment quality
than Phase 6's non-perfect score (`root-cause-analyzer`'s case-03,
0.67/0.67); a single self-authored evaluation cannot support that
comparison either way. Two fixtures deliberately exercise real divergence:
case-03 has ZERO diff-hygiene flags but is still `readiness_tier=blocked`
because a real hotspot with no test coverage is an absolute blocker on its
own (Axis 2/3 alone can block, hygiene is not the only path); case-07 has
a CLEAR `readiness_tier` from Axes 1-3 while a composed regression-hunter
report shows `overall_risk_tier=high` for the same file — independent
signals that can and do disagree, by design.

**Dogfood run** (`examples/release-readiness/example-run.md`):
regenerated a fresh `codebase-intelligence` report against this repo's
current (10-skill) state, then ran a real `git diff` of this phase's own
actual body of work — 78 new files, staged (never committed) with `git
add`, diffed with `git diff --cached`, then immediately unstaged with
`git reset`. The run confirmed, concretely, a limitation `SKILL.md`'s
Known Limitations had already predicted before the run: the
`debug-print-leftover` hygiene pattern fired 5 times on this skill's own
`engine/cli.py` and `run_evaluation.py`, every one a legitimate CLI
stdout/stderr `print()` call, not a debug leftover — left unfixed by
design (the documented boundary between the hygiene table and the agent's
Step 4 false-positive-check judgment). It also surfaced, and deliberately
did **not** fix, a new, materially more consequential finding: **L24** —
`target_resolver.py`'s substring-based resolution, a THIRD independent
copy of the exact heuristic already disclosed as L23, was shown for the
first time to produce **false-positive test coverage** (not just an
inflated caller list) when a module's stem (e.g. `models`, `stats`,
`report`) collides with an identically-named module in an unrelated
skill — `skills/release-readiness/engine/models.py` resolved as "covered"
by `architecture-decision`'s test files despite having no
`tests/test_models.py` of its own. This is a more consequential category
of finding than L23: L23 inflated a displayed field without changing that
run's outcome; L24 corrupts the exact signal (`test_coverage.has_coverage`)
the readiness rule table uses to decide whether a structurally
consequential file needs closer review.

**Memory-bank updates this phase**: `05-evaluation-framework.md`
(Release Readiness Checklist), `11-decisions.md` (ADR-016),
`12-known-limitations.md` (L24, L8 update), `16-assumptions-
validation.md` (A5, A10 updated), `08-roadmap.md` (Phase 10 marked
complete, Phase 11 proposed next), `implementation-status.md`,
`07-current-state.md`, `03-architecture.md`, `sprint-history/SPRINT-10.md`,
root `README.md`/`ROADMAP.md`/`QuickStarterGuide.md`/`DEPENDENCIES.md`/
`CHANGELOG.md`.

## Open threads / not yet decided

- **2026-08-26 update: Phase 11 AND Phase 12 both shipped at the user's
  explicit direction; Phase 13 onward is still frozen.** The mentor-review
  critique concluded velocity of building had outpaced velocity of
  validating (A2/A5 both UNKNOWN after ten phases, zero real external
  users), and the user then explicitly directed starting Phase 11, and
  later the same day Phase 12, anyway. Each is a one-time, explicit
  exception, not new evidence and not a general unfreezing —
  re-justifying Phase 13+ still requires real external validation evidence
  first (a real user, an independent/blind eval pass, or a real
  usage-comparison run via `evaluations/usage-comparison/`), not just a
  pre-written roadmap proposal.
- **L8 remains the most important open thread, now applying eleven
  times**: ten of eleven judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard,
  architecture-decision, refactoring-safety, regression-hunter,
  release-readiness, dependency-supply-chain, engineering-knowledge-capture)
  scored 100% precision/recall against self-authored ground truth; the
  eleventh (root-cause-analyzer) scored 7/8 perfect and 1/8 at 0.67/0.67
  (L19). All outcomes are equally inconclusive about real-world quality —
  self-authored, single-rater evidence either way. The inter-rater-
  agreement experiment (A5) still has not been run for any of the eleven.
- **L25/L26 (Phase 11)**: `dependency-supply-chain` has no live
  CVE/vulnerability-database lookup (L25, permanent scope decision — this
  project makes no network calls, ADR-006) and no per-dependency
  license-risk detection (L26, corrected mid-implementation — the data
  needed doesn't exist in what `codebase-intelligence` parses; dropped from
  scope rather than fabricated). Both named explicitly in `SKILL.md`, not
  silently omitted.
- **L28 (new, Phase 12)**: `engineering-knowledge-capture`'s
  `location_resolver.py` only checks the exact matched line for a module
  mention, not the surrounding paragraph — found via a real dogfood run
  where every candidate resolved to no location despite the relevant
  module being named four times nearby. Disclosed, not fixed — widening
  the window risks a new false-positive class this project has no evidence
  is rarer than the false negative just found.
- **The L14/L19/L21/L23/L24 substring-collision limitation class — status
  as of 2026-08-26: L23 FIXED, L24 PARTIALLY fixed, L14/L19/L21 still
  open.** `target_resolver.py`'s caller-identification bug (L23, shared
  across `refactoring-safety`/`regression-hunter`) and its embedded-
  substring subclass in `release-readiness`'s `test_coverage_scanner.py`
  (part of L24) are fixed via a word-boundary-aware match — see
  `12-known-limitations.md`. L24's headline example (two skills'
  identically-stemmed modules producing a real, boundary-respecting
  false-positive coverage match) remains open — closing it needs
  repo-layout-aware path scoping, deliberately not implemented this pass.
  L14 (`feature-planner/relevance_scorer.py`), L19
  (`root-cause-analyzer/candidate_scorer.py`), and L21
  (`architecture-decision/impact_scorer.py`) are a related but distinct
  keyword-relevance-scoring limitation class in different files — NOT
  touched by this fix, still open.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, C) found
  plausible-but-narrow signal on N=1 each; Phase 10's dogfood run is
  additional real-usage evidence for A10, sharpening Phase 9's finding —
  composition executed correctly and was genuinely used (including, for the
  first time, the two OPTIONAL cross-skill compositions), and this time
  surfaced a more consequential gap in a shared resolution pattern (L24),
  not just a gap in the composed data itself (L22) or a displayed-field-only
  gap (L23). None upgrades its assumption's status beyond UNKNOWN — the
  missing ingredient in every case is the same: a real second party this
  session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5), L18 (Phase 6, scope boundary), L21 (Phase 7,
  keyword-collision-at-scale), L22 (Phase 8, fan_in undercounting), L23
  (Phase 9, substring-collision caller identification) remain deliberately
  deferred — revisit only if real usage shows they matter. L24 (Phase 10)
  is deferred for the same reason but flagged, above, as the strongest
  candidate yet to revisit soon.
- No real (non-agent) engineer has used any of the twelve skills yet —
  Trust Status stays EXPERIMENTAL on all twelve, and assumptions
  A2/A3/A5/A7/A10 in [[16-assumptions-and-validation]] remain only
  partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[operating-charter]] — the source document everything else in this
   memory bank distills (only needed for deep context; skip on a quick
   resume)
3. [[implementation-status.md]]
4. [[07-current-state]]
5. `README.md` (root) — primary public-facing entry point
6. `skills/engineering-knowledge-capture/SKILL.md`,
   `skills/dependency-supply-chain/SKILL.md`,
   `skills/release-readiness/SKILL.md`,
   `skills/regression-hunter/SKILL.md`,
   `skills/refactoring-safety/SKILL.md`,
   `skills/architecture-decision/SKILL.md`,
   `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
7. `examples/engineering-knowledge-capture/example-run.md` (real dogfood,
   surfaced the new L28 line-vs-paragraph resolution gap),
   `examples/dependency-supply-chain/example-run.md` (real dogfood, confirms
   the inherited L2 scope gap concretely) and `examples/release-readiness/
   example-run.md` (the real diff run that disclosed L24)
8. [[17-experiment-viability-check.md]]
9. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with Phase 6-11 posts)

## Last updated

2026-08-26 — Phase 12 (`engineering-knowledge-capture`) shipped at the
user's explicit direction, a second one-time reopening of the same-day
mentor-review freeze (after Phase 11, `dependency-supply-chain`); Phase 13
onward remains frozen. Test count: 521 (up from 474). Earlier the same
day, between Phase 11 and Phase 12: the operating charter checked in at
[[operating-charter]] (documentation only, no code/roadmap change; see
[[12-known-limitations|L27]] for the disclosed section-numbering gap).
