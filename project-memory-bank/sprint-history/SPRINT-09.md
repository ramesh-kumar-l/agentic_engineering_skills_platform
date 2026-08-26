# Sprint 09 — Phase 9: Regression Hunter

## Goal
Build a ninth skill by reusing Pattern 2's judgment-based architectural
pattern an eighth time and the mandatory-composition rule (ADR-010,
already reused four times: `feature-planner`, `root-cause-analyzer`,
`architecture-decision`, `refactoring-safety`) a fifth time, turning a
unified git diff into a per-file regression-risk assessment grounded in a
real structural map of the repo plus an independent test-coverage signal,
per the user's exit criteria ("same bar, first skill composing on top of
Codebase Intelligence's output, production-level stable system" — the
"first" framing is a fifth reuse of an already-established pattern, stated
honestly as such, same as every phase since Phase 6).

## Hypothesis
Pattern 2 generalizes to an eighth judgment domain (weighing whether a
*diff*, not just a description, risks regressing existing behavior) without
needing a new base pattern. Separately: a diff's regression risk has three
genuinely independent axes — what the diff itself mechanically looks like
(removed guards, removed exception handling, fewer test assertions), how
structurally consequential the changed file already is (real fan-in/hotspot
data), and whether the change is actually test-covered — and blending them
into one score would hide exactly the divergence a reviewer most needs to
see (e.g. a diff with zero pattern flags touching a real hotspot with no
tests).

## Success Criteria
Engine modules <300 lines each (strict modularity, explicit user
requirement, carried forward from every prior phase — met, max 181 lines);
tests pass, including a CLI test file written from the start; evaluation
harness runs against 8 seeded fixtures with real scores for both layers;
`SKILL.md` meets the canonical template; memory bank updated per the user's
"save state" requirement; a real dogfood run against a genuine diff this
phase's own build actually produced, not a purely synthetic stand-in.

## Completed Work
`skills/regression-hunter/` (SKILL.md, engine — 11 modules, tests — 64
passing including CLI), an 8-fixture evaluation harness scoring
deterministic diff-pattern-flag/risk-tier correctness plus judgment-layer
Precision/Recall, a dogfood run (`examples/regression-hunter/`) regenerating
a fresh `codebase-intelligence` report against the repo's current 9-skill
state and assessing a real, already-fixed-and-tested `codebase-intelligence`
bug this phase's own build produced (a missing `*.egg-info` directory
exclusion), `project-memory-bank/05-evaluation-framework.md` (Regression
Risk Checklist added, eighth checklist), `03-architecture.md` (Pattern 2
reused an eighth time, ADR-015 note), `11-decisions.md` (ADR-015),
`12-known-limitations.md` (L23, L8 update to eight), `16-assumptions-and-
validation.md` (A5, A10), `08-roadmap.md` (Phase 9 complete, Phase 10
proposed next), `implementation-status.md`, `07-current-state.md`,
`active-context.md`, root `README.md`/`ROADMAP.md`/`CHANGELOG.md`/
`QuickStarterGuide.md`/`DEPENDENCIES.md` (skill-count refreshes).

## Evidence
64/64 new tests passing; 342/342 across all nine skills
(24+23+24+21+58+32+34+62+64 — `codebase-intelligence` itself gained one
test this phase, from a real fix its own dogfood target surfaced). 8/8
evaluation fixtures: deterministic layer 100% correct (automated); judgment
layer 8/8 perfect precision/recall — same caveat as every prior phase, not
read as evidence of higher judgment quality than Phase 6's non-perfect
case. One real dogfood finding, disclosed-not-fixed: `regression-hunter`'s
`target_resolver.py` (an independent copy of `refactoring-safety`'s
identical caller-matching pattern) resolves callers via bare substring
match, producing a wildly inflated caller list for short, common module
stems like `scanner` (L23) — the first time this limitation class
(L14/L19/L21) has been shown to affect two skills' independent copies of
the same heuristic at once. Separately, the dogfooded diff itself was a
genuine, already-tested `codebase-intelligence` fix (excluding `*.egg-info`
directories from repo scans) — a real bug this phase's own build found and
fixed outside `regression-hunter`'s own code, raising `codebase-
intelligence`'s test count from 23 to 24.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-8. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as every prior phase. Safety/Explainability left for human
review, same discipline as before. All 8 fixtures' expected categories were
authored before any actual derivation was scored against them, same
protocol as every prior phase. Case-06 and case-07 deliberately exercise a
real divergence between the diff-pattern axis and the composed-report
test-coverage axis (a "no test file touched in this diff" flag firing even
when the report shows real, pre-existing coverage) — confirming by design
that the three axes are independent signals, not redundant ones.

## Failures
None shipped as an undisclosed defect. L23 (inflated caller lists for
short module stems) is a disclosed, deliberately-unfixed limitation — the
same design tradeoff already accepted for L14/L19/L21, not re-litigated
here without new evidence of need across every skill using this pattern.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-015 (per-changed-file regression risk from three explicit, non-blended
signals — diff-pattern flags, structural blast radius, test-coverage
status — combined via a documented rule table into an overall tier, all
three still visible separately) — see `11-decisions.md`. `feature-planner`'s
ADR-010 (mandatory composition with `codebase-intelligence`) reused a fifth
time, explicitly stated as a reuse. Pattern 2 (ADR-007) reused an eighth
time without a new base-pattern ADR.

## Lessons Learned
Reusing an existing architectural pattern for an eighth, different judgment
domain — this time diff-driven rather than description-driven — worked
cleanly again, and the three-axis, non-blended design translated directly
from Phase 8's two-axis version without needing a new base pattern, only a
third field. The real dogfood run again earned its keep more than the
synthetic fixtures: all 8 scored perfectly (confirming the harness works,
nothing new learned from them beyond that), while the real diff dogfood run
surfaced L23 — a limitation now shown to affect *two independently-copied*
implementations of the same heuristic, which is stronger evidence that the
underlying design tradeoff deserves a real look before a tenth skill copies
it a third time, rather than evidence specific to this one skill.

## What We Should Stop / Continue / Change
- **Continue**: dogfooding every skill against something real whenever
  possible — this phase's dogfood target was itself a real bug found and
  fixed in a *different* skill (`codebase-intelligence`) during this
  phase's own build, then used as the diff under test.
- **Continue**: surfacing cross-skill limitations plainly the moment they
  recur, rather than treating each skill's disclosure in isolation — L23 is
  explicitly framed as the second occurrence of a shared heuristic's
  weakness, not a new, unrelated finding.
- **Change (carried over from Sprints 05-08, now eight skills deep)**: the
  independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was explicitly instructed to build a ninth skill instead. That is a
  legitimate user call, but the gap itself has not gotten smaller, and now
  two skills share an unfixed, unverified structural-matching heuristic
  (L23) that only real, non-self-authored use would meaningfully stress.

## Next Sprint Recommendation
Phase 10 (Release Readiness, per the roadmap's portfolio list), pending
explicit user approval and re-justification against evidence per the
adaptive-roadmap rule. The case for investing a sprint in the
independent-evidence gap (L8/A5) before a tenth skill is now stronger than
it was after Sprint 08: L23 demonstrated the substring-matching weakness is
not a one-off, and a tenth skill copying the same `target_resolver.py`
pattern a third time without addressing it would compound a known,
disclosed risk rather than discover a new one.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file, max 181), tested, pattern reuse worked cleanly, ADR-015's three-axis split is a real scoring-design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run diff |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the eighth time; perfect fixture scores are less informative than the real dogfood finding this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, including the honest cross-skill-limitation disclosure |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep |
| Learning | 4 | ADR-015's three-axis scoring and L23's cross-skill recurrence are both genuinely new, non-trivial findings |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
