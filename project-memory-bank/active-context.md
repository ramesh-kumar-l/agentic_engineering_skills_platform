# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 9 (regression-hunter) — COMPLETE. Phase 10 (Release Readiness, per
[[08-roadmap]]'s portfolio list) not started, still waiting on explicit user
instruction per [[08-roadmap]]'s phase protocol.

## What Phase 9 built

Built `regression-hunter`, the ninth skill: `SKILL.md` contract reusing
Pattern 2 (ADR-007) an eighth time — a deterministic engine (11 modules,
each under 300 lines, max 181) that parses a unified git diff (independent
copy of `adversarial-diff-reviewer`'s parsing conventions) into structured
per-file hunks, scans those hunks directly for five mechanically-detectable
diff-pattern shapes (removed exception handling, a removed conditional
guard with no replacement, a large unreplaced deletion, decreased test
assertions in a changed test file, a modified function signature with no
corresponding test-file change in the same diff), resolves each changed
file against a real `codebase-intelligence` report (exact-path or
module-stem match, independent copy of `refactoring-safety`'s
`target_resolver.py`), finds its real callers via an independent import-
list scan, checks an independently-computed test-coverage signal
(independent copy of `refactoring-safety`'s `test_coverage_scanner.py`),
and combines all three axes into one `overall_risk_tier` per file via a
documented rule table. 64 passing tests, including a CLI test file written
from the start (same discipline Phases 5-8 established). Combined with an
agent-driven Regression Risk Checklist workflow — a new, eighth checklist
in [[05-evaluation-framework]] (10 categories: existing-behavior-at-risk
stated precisely, diff-pattern flags reviewed as leads not proof,
structural blast radius grounded in real data, test coverage distinguished
from diff-level silence, overall risk tier explained via the rule table,
false-positive check, missing-coverage files named explicitly, security
implications, evidence cited, assumption flag).

**Architecture**: reuses `feature-planner`'s/`root-cause-analyzer`'s/
`architecture-decision`'s/`refactoring-safety`'s mandatory-composition rule
(ADR-010) a fifth time — a missing/malformed `codebase-intelligence` report
is a hard failure, not a degraded path, stated explicitly as a *reuse*. New
this phase: **ADR-015** — three explicitly separate, non-blended regression
signals per changed file (diff-pattern flags scanned directly against the
diff's own hunks, structural blast radius, test coverage) are combined into
one `overall_risk_tier` via a documented rule table, while all three fields
stay visible and separately inspectable, so a flagged-but-covered file is
never confused with an unflagged-but-uncovered hotspot. The diff-pattern
scanning (Axis 1) is the genuinely new deterministic-layer contribution
this phase — no prior skill scans a diff's own hunks for regression shapes;
`adversarial-diff-reviewer`'s `risk_scanner.py` scans *added* lines for new
defects, while this skill scans *removed and modified* lines for existing
behavior at risk, making the two skills complementary rather than
overlapping.

**Evaluation**: an 8-fixture harness (`evaluations/regression-hunter/`),
same two-layer scoring (deterministic + judgment) as Phases 2-8. This is
the **eighth** judgment-based skill evaluated with self-authored,
single-rater fixtures. All 8 fixtures scored perfect precision/recall on
both layers — stated plainly as *not* evidence of higher judgment quality
than Phase 6's non-perfect score (`root-cause-analyzer`'s case-03,
0.67/0.67); a single self-authored evaluation cannot support that
comparison either way. Two fixtures (case-06, case-07) deliberately
exercise the three-axis divergence: a diff-level "no test file changed in
THIS diff" flag fires at the same time the composed report shows the file
genuinely has real test coverage — independent signals that can and do
disagree.

**Dogfood run** (`examples/regression-hunter/example-run.md`):
regenerated a fresh `codebase-intelligence` report against this repo's
current (9-skill) state, then ran a real `git diff` this phase's own build
actually produced — a genuine, already-tested `codebase-intelligence`
scanner fix (excluding `*.egg-info` directories from repo scans, with a new
test, `codebase-intelligence`'s suite growing from 23 to 24). The run
correctly scored both changed files LOW overall risk (zero diff-pattern
flags, no structural escalation for a purely additive, already-tested
change) — the correct, honest outcome. One real, disclosed finding: **L23**
— `target_resolver.py`'s substring-based caller-identification heuristic,
shared as an independent copy between `refactoring-safety` and
`regression-hunter`, inflated `scanner.py`'s caller list to 22 modules,
most of them false positives from other skills' own `*_scanner.py` modules
sharing the substring `"scanner"`. This is a new category of finding: not a
gap in the *composed upstream data* (like Phase 8's L22), but a gap in a
*resolution pattern shared across two skills' independent copies* of the
same heuristic.

**Memory-bank updates this phase**: `05-evaluation-framework.md`
(Regression Risk Checklist), `11-decisions.md` (ADR-015),
`12-known-limitations.md` (L23, L8 update), `16-assumptions-and-
validation.md` (A5, A10 updated), `08-roadmap.md` (Phase 9 marked complete,
Phase 10 proposed next), `implementation-status.md`, `07-current-state.md`,
`03-architecture.md`, `sprint-history/SPRINT-09.md`, root `README.md`/
`ROADMAP.md`/`QuickStarterGuide.md`/`DEPENDENCIES.md`/`CHANGELOG.md`.

## Open threads / not yet decided

- Phase 10 (Release Readiness) is next on the portfolio list per
  [[08-roadmap]] but not started and not re-justified against evidence yet
  — that re-justification happens at the start of Phase 10, not now.
- **L8 remains the most important open thread, now applying eight times**:
  seven of eight judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard,
  architecture-decision, refactoring-safety, regression-hunter) scored
  100% precision/recall against self-authored ground truth; the eighth
  (root-cause-analyzer) scored 7/8 perfect and 1/8 at 0.67/0.67 (L19). All
  outcomes are equally inconclusive about real-world quality —
  self-authored, single-rater evidence either way. The inter-rater-
  agreement experiment (A5) still has not been run for any of the eight.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, C) found
  plausible-but-narrow signal on N=1 each; Phase 9's dogfood run is
  additional real-usage evidence for A10, sharpening Phase 8's finding —
  composition executed correctly and was genuinely used, and this time
  surfaced a gap shared across two skills' independent copies of the same
  composition-consuming resolution pattern (L23), not just a gap in the
  composed data itself (L22). None upgrades its assumption's status beyond
  UNKNOWN — the missing ingredient in every case is the same: a real second
  party this session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5), L18 (Phase 6, scope boundary), L21 (Phase 7,
  keyword-collision-at-scale), L22 (Phase 8, fan_in undercounting), L23
  (Phase 9, substring-collision caller identification) remain deliberately
  deferred — revisit only if real usage shows they matter.
- No real (non-agent) engineer has used any of the nine skills yet — Trust
  Status stays EXPERIMENTAL on all nine, and assumptions
  A2/A3/A5/A7/A10 in [[16-assumptions-and-validation]] remain only
  partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `README.md` (root) — primary public-facing entry point
5. `skills/regression-hunter/SKILL.md`,
   `skills/refactoring-safety/SKILL.md`,
   `skills/architecture-decision/SKILL.md`,
   `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
6. `examples/regression-hunter/example-run.md` (the real diff run that
   disclosed L23)
7. [[17-experiment-viability-check.md]]
8. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with Phase 6, 7, 8, or 9 posts)

## Last updated

2026-08-23 — end of Phase 9.
