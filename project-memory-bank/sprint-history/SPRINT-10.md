# Sprint 10 — Phase 10: Release Readiness

## Goal
Build a tenth skill — the final skill in the Engineering Lifecycle group —
by reusing Pattern 2's judgment-based architectural pattern a ninth time
and the mandatory-composition rule (ADR-010, already reused five times:
`feature-planner`, `root-cause-analyzer`, `architecture-decision`,
`refactoring-safety`, `regression-hunter`) a sixth time, turning a git diff
plus a required `codebase-intelligence` report — and optionally,
pre-computed `regression-hunter`/`security-context-guard` reports — into a
Release Readiness Scorecard: a per-file readiness tier and one advisory
overall verdict, per the user's exit criteria ("same bar, first skill
composing on top of Codebase Intelligence's output, production-level
stable system" — the "first" framing is a sixth reuse of an already-
established pattern, stated honestly as such, same as every phase since
Phase 6).

## Hypothesis
Pattern 2 generalizes to a ninth judgment domain (assessing whether a body
of work, not just one diff, is ready to ship) without needing a new base
pattern. Separately: a release-readiness judgment has (at least) three
genuinely independent, always-available axes — mechanical diff-hygiene
issues, real structural blast radius, and real test coverage — plus two
further, OPTIONAL axes this platform's own prior skills already compute
better than this skill could re-derive them. Blending all five into one
score would both hide real divergence between the always-available axes
AND silently override a different skill's own, already-validated
judgment. Keeping the optional axes visible-but-not-blended tests whether
that discipline (already proven for within-skill axes by ADR-012/013/014/
015) also holds across skill boundaries.

## Success Criteria
Engine modules <300 lines each (strict modularity, explicit user
requirement, carried forward from every prior phase — met, max 211 lines);
tests pass, including a CLI test file written from the start; evaluation
harness runs against 8 seeded fixtures with real scores for both layers,
including at least 2 fixtures exercising real axis divergence; `SKILL.md`
meets the canonical template with explicit, repeated advisory-only framing
for the overall verdict; memory bank updated per the user's "save state"
requirement; a real dogfood run against a genuine body of work this
phase's own build actually produced, not a purely synthetic stand-in.

## Completed Work
`skills/release-readiness/` (SKILL.md, engine — 16 modules, tests — 78
passing including CLI), an 8-fixture evaluation harness scoring
deterministic hygiene-flag/readiness-tier/overall-verdict correctness plus
judgment-layer Precision/Recall, a dogfood run (`examples/release-
readiness/`) regenerating a fresh `codebase-intelligence` report against
the repo's current 10-skill state and assessing a real, staged-then-
unstaged (never committed) `git diff` of this phase's own 78 new files,
`project-memory-bank/05-evaluation-framework.md` (Release Readiness
Checklist added, ninth checklist), `03-architecture.md` (Pattern 2 reused
a ninth time, ADR-016 note), `11-decisions.md` (ADR-016),
`12-known-limitations.md` (L24, L8 update to nine), `16-assumptions-and-
validation.md` (A5, A10), `08-roadmap.md` (Phase 10 complete, Phase 11
proposed next), `implementation-status.md`, `07-current-state.md`,
`active-context.md`, root `README.md`/`ROADMAP.md`/`CHANGELOG.md`/
`QuickStarterGuide.md`/`DEPENDENCIES.md` (skill-count refreshes).

## Evidence
78/78 new tests passing; 420/420 across all ten skills
(24+23+24+21+58+32+34+62+64+78 — `codebase-intelligence` itself unchanged
this phase, having already gained a test in Phase 9). 8/8 evaluation
fixtures: deterministic layer 100% correct (automated); judgment layer 8/8
perfect precision/recall — same caveat as every prior phase, not read as
evidence of higher judgment quality than Phase 6's non-perfect case. Two
real dogfood findings: (1) a predicted false-positive shape (legitimate CLI
`print()` calls flagged as debug leftovers) confirmed concretely on this
skill's own real `engine/cli.py` and `run_evaluation.py`, left unfixed by
design; (2) a real, disclosed-not-fixed limitation (L24) — `target_
resolver.py`, reused a THIRD time (after `refactoring-safety`'s and
`regression-hunter`'s), was shown for the first time to produce
false-positive TEST COVERAGE, not just an inflated caller list, when a
module's stem collides with an identically-named module in an unrelated
skill — a materially more consequential manifestation of the L14/L19/L21/
L23 limitation class than any prior occurrence.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-9. Judgment-layer Precision/Recall/False Positives/False
Negatives computed automatically from real agent-produced
`actual/*.json`, same methodology as every prior phase. Safety/
Explainability left for human review, same discipline as before. All 8
fixtures' expected categories were authored before any actual derivation
was scored against them, same protocol as every prior phase. Case-03 and
case-07 deliberately exercise real divergence: case-03 shows a completely
clean diff (zero hygiene flags) can still be `blocked` from structural
tier + missing coverage alone; case-07 shows a `clear` readiness_tier from
Axes 1-3 coexisting with a composed regression-hunter report's `high`
overall_risk_tier for the same file — confirming by design that the
always-available axes and the optional cross-skill axes are independent
signals, not redundant ones.

## Failures
None shipped as an undisclosed defect. L24 (false-positive test coverage
from stem-collision, a sharper manifestation of L14/L19/L21/L23) is a
disclosed, deliberately-unfixed limitation — the same design tradeoff
already accepted for its predecessors, not re-litigated here without new
evidence of need across every skill using this pattern, though this
sprint's write-up explicitly states the case for revisiting it is now
stronger than at any prior phase boundary.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-016 (the Release Readiness Scorecard — three always-available,
non-blended per-file signals combined via a documented rule table into a
readiness tier, plus two OPTIONAL, cross-skill-composed signals surfaced
but never blended in, rolled up into one advisory overall verdict) — see
`11-decisions.md`. `feature-planner`'s ADR-010 (mandatory composition with
`codebase-intelligence`) reused a sixth time, explicitly stated as a reuse.
`security-context-guard`'s ADR-011 (optional composition, advisory-only
output) reused for the two new optional axes specifically. Pattern 2
(ADR-007) reused a ninth time without a new base-pattern ADR.

## Lessons Learned
Composing OPTIONALLY with two OTHER skills' own real outputs — not just
`codebase-intelligence`'s — worked cleanly and validated the "surface,
don't re-blend" discipline generalizes across skill boundaries, not just
within one skill's own axes (which ADR-012/013/014/015 had already
established). The real dogfood run again earned its keep more than the
synthetic fixtures: all 8 scored perfectly (confirming the harness works,
nothing new learned from them beyond that), while assessing this phase's
own real body of work surfaced L24 — a materially more consequential
version of a limitation class this project has now seen four times before
in three skills' independent copies of the same pattern. That recurrence,
at increasing severity, is itself the most important finding of this
sprint: the underlying design tradeoff (bare substring matching over a
word-boundary or scoped match) has now been given four separate,
independent chances to prove itself safe enough to leave alone, and each
one has instead sharpened the case against it.

## What We Should Stop / Continue / Change
- **Continue**: dogfooding every skill against something real whenever
  possible — this phase's dogfood target was the phase's own actual body
  of work, assessed via a real, staged-then-unstaged, never-committed
  `git diff`, a genuinely fitting choice for the skill whose entire
  purpose is judging release readiness.
- **Continue**: surfacing cross-skill limitations plainly the moment they
  recur, rather than treating each skill's disclosure in isolation — L24 is
  explicitly framed as a sharper, third occurrence of a known mechanism,
  not a new, unrelated finding.
- **Change (carried over from Sprints 05-09, now nine skills deep, and
  raised with more urgency this sprint)**: the independent-rater evaluation
  (L8) and the inter-rater-agreement experiment (A5) remain unrun. This
  sprint did not close that gap — it was explicitly instructed to build a
  tenth skill instead. That is a legitimate user call, but L24 has now
  demonstrated the shared substring-matching pattern can corrupt a
  downstream decision signal (test coverage), not just a displayed field —
  the strongest evidence yet that the L14/L19/L21/L23/L24 limitation class
  deserves a dedicated look before an eleventh skill copies the pattern
  again, rather than being deferred a fifth time.

## Next Sprint Recommendation
Phase 11 (Dependency / Supply Chain, per the roadmap's portfolio list),
pending explicit user approval and re-justification against evidence per
the adaptive-roadmap rule. Given L24's severity, a future session should
explicitly weigh whether to invest a sprint fixing the shared
`target_resolver.py`-family substring-matching pattern (now present in
three skills as independent copies) before building an eleventh skill that
might copy it a fourth time — this recommendation is stated more strongly
here than in any prior sprint's equivalent note.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file, max 211), tested, pattern reuse worked cleanly, ADR-016's always-available/optional axis split is a real scoring-design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run diff |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the ninth time; perfect fixture scores are less informative than the real dogfood finding this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, including the honest cross-skill-limitation disclosure at a sharper severity than before |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep |
| Learning | 4 | ADR-016's always-available/optional axis split and L24's sharper cross-skill recurrence are both genuinely new, non-trivial findings |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
