# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 10 (release-readiness) — COMPLETE. Phase 11 (Dependency / Supply
Chain, per [[08-roadmap]]'s portfolio list) not started, still waiting on
explicit user instruction per [[08-roadmap]]'s phase protocol.

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

- Phase 11 (Dependency / Supply Chain) is next on the portfolio list per
  [[08-roadmap]] but not started and not re-justified against evidence yet
  — that re-justification happens at the start of Phase 11, not now.
- **L8 remains the most important open thread, now applying nine times**:
  eight of nine judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard,
  architecture-decision, refactoring-safety, regression-hunter,
  release-readiness) scored 100% precision/recall against self-authored
  ground truth; the ninth (root-cause-analyzer) scored 7/8 perfect and 1/8
  at 0.67/0.67 (L19). All outcomes are equally inconclusive about
  real-world quality — self-authored, single-rater evidence either way.
  The inter-rater-agreement experiment (A5) still has not been run for any
  of the nine.
- **The L14/L19/L21/L23/L24 substring-collision limitation class is now
  the second most important open thread**, and arguably the strongest case
  yet for a dedicated fix-it phase rather than a tenth (now eleventh)
  skill copying the pattern again: L24 demonstrated the SAME shared
  `target_resolver.py` pattern, reused a THIRD time, corrupts test-coverage
  matching (not just a displayed caller list) — a more consequential
  failure mode than any prior occurrence, since it feeds directly into a
  downstream rule table's decision. Sprint 09 already flagged this
  concern; Sprint 10 sharpens it further (see `sprint-history/SPRINT-10.md`).
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
- No real (non-agent) engineer has used any of the ten skills yet — Trust
  Status stays EXPERIMENTAL on all ten, and assumptions
  A2/A3/A5/A7/A10 in [[16-assumptions-and-validation]] remain only
  partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `README.md` (root) — primary public-facing entry point
5. `skills/release-readiness/SKILL.md`,
   `skills/regression-hunter/SKILL.md`,
   `skills/refactoring-safety/SKILL.md`,
   `skills/architecture-decision/SKILL.md`,
   `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
6. `examples/release-readiness/example-run.md` (the real diff run that
   disclosed L24)
7. [[17-experiment-viability-check.md]]
8. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with Phase 6, 7, 8, 9, or 10 posts)

## Last updated

2026-08-24 — end of Phase 10.
