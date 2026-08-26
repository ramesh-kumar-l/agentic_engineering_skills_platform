# Sprint 12 — Phase 12: Engineering Knowledge Capture

## Goal
Build a twelfth skill by reusing Pattern 2's judgment-based architectural
pattern an eleventh time and the mandatory-composition rule (ADR-010,
already reused seven times) an eighth time, turning a free-text
engineering narrative and a required `codebase-intelligence` report into a
Knowledge Capture Report — candidate decisions/lessons/limitations/
workarounds, each resolved against real structural data where a module is
named — per the user's exit criteria ("same bar, first skill composing on
top of Codebase Intelligence's output, implementation make sure final
developed product is a scalable and production level stable system" — the
"first" framing is an eighth reuse of an already-established pattern,
stated honestly as such, same as every phase since Phase 6). The user also
directed strict per-file modularity (<300 lines) and a memory-bank
save-state update before ending — both already this project's standing
discipline, restated explicitly this sprint.

**Process context, unique to this sprint**: this is the SECOND same-day
reopening of the mentor-review freeze. Phase 11 (`dependency-supply-chain`)
had already reopened it once earlier the same day at the user's explicit
direction; the freeze itself (A2/A5 both UNKNOWN, zero real external
users) had not lifted in between. The user then explicitly directed
starting Phase 12 anyway. This sprint proceeded on that explicit
instruction — recorded here as a second, one-time exception, not as the
freeze's conditions having been met, and not as Phase 11 shipping being
read as precedent that asking unfreezes the roadmap generally.

## Hypothesis
Pattern 2 generalizes to an eleventh judgment domain (deciding what
engineering knowledge is worth durably capturing) without needing a new
base pattern. Separately: this project's own practice of writing ADRs,
known-limitations, and lessons-learned every phase is itself a repeatable
signal-extraction task — a fixed marker table over free text, resolved
against real structural data, can flag genuine candidates without
fabricating judgment about which candidates are actually worth writing up.

## Success Criteria
Engine modules <300 lines each (met, max 121 lines — well under budget);
tests pass, including a CLI test file written from the start; evaluation
harness runs against 8 seeded fixtures with real scores for both layers;
`SKILL.md` meets the canonical template with explicit scope boundaries (no
commit-history parsing, no automatic memory-bank writes) stated up front;
memory bank updated per the user's explicit "save state" directive; a real
dogfood run against this project's own actual engineering history, not a
purely synthetic stand-in.

## Completed Work
`skills/engineering-knowledge-capture/` (SKILL.md, engine — 9 modules,
tests — 47 passing including CLI), an 8-fixture evaluation harness scoring
deterministic candidate-set/priority correctness plus judgment-layer
Precision/Recall, a dogfood run (`examples/engineering-knowledge-capture/`)
against a narrative built from genuine excerpts of this project's own
engineering history, `project-memory-bank/05-evaluation-framework.md`
(Knowledge Capture Checklist added, eleventh checklist), `11-decisions.md`
(ADR-018), `12-known-limitations.md` (L28), `16-assumptions-and-
validation.md` (A2, A5 notes), `03-architecture.md` (Pattern 2 reuse count
updated), `08-roadmap.md` (Phase 12 marked complete with the freeze/
exception context), `implementation-status.md`, `07-current-state.md`,
`active-context.md`, root `README.md`/`ROADMAP.md`/`CHANGELOG.md`,
`.github/workflows/tests.yml` (matrix updated).

## Evidence
47/47 new tests passing; 521/521 across all twelve skills
(24+23+24+21+58+32+34+64+66+82+46+47). 8/8 evaluation fixtures:
deterministic layer 100% correct (automated); judgment layer 8/8 perfect
precision/recall — same caveat as every prior phase, eleventh time now,
not read as evidence of higher judgment quality than Phase 6's
non-perfect case. Real dogfood finding: every candidate in the real run
resolved to no location at all, despite the narrative naming
`target_resolver.py` four times by full path — a concrete, live
demonstration that this skill's own synthetic fixtures (which put the
module mention in the same sentence as the marker) don't match how real
retrospective narratives are actually written (module named in one
sentence, decision/lesson stated in the next) — logged as L28.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-11. Judgment-layer Precision/Recall computed automatically from
real agent-produced `actual/*.json`, same methodology as every prior
phase. Safety/Explainability left for human review, same discipline as
before. All 8 fixtures' expected categories were authored before any
actual derivation was scored against them, same protocol as every prior
phase. Case-05 deliberately exercises multi-candidate composition (a
decision and its direct-consequence limitation, kept as two distinct
candidates, not collapsed), and case-08 exercises the fail-closed rule
(zero modules in the CI report triggers MEDIUM, never a silent LOW).

## Failures
None shipped as an undisclosed defect. One gap was found via real dogfood,
after fixtures already passed, and disclosed rather than silently
patched around: `location_resolver.py`'s single-line evidence window
(L28, above). Left unfixed by design — the same "disclose, don't guess a
fix from one data point" discipline this project applied to L14, L18,
L21, and L22 on their first discovery.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures well under 5ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-018 (required composition reused an eighth time; location resolver
built word-boundary-correct from day one, the fourth independent copy of
the L23/L24 fix and the first not shipped with the bug first; fail-closed
priority discipline reused a third time, extended to deliberately never
assign LOW; first skill whose deterministic layer targets a documentation
artifact rather than a code-risk judgment) — see `11-decisions.md`.
Pattern 2 (ADR-007) reused an eleventh time without a new base-pattern ADR.

## Lessons Learned
Building the location resolver correct from day one (word-boundary-aware,
not a bare substring check) avoided reintroducing the L23/L24 bug class —
but a *different*, previously-unseen gap (single-line vs. paragraph-scoped
evidence windows) was still only found by running against real prose, not
by writing correct code or passing synthetic fixtures. This sharpens L8's
existing caveat with a concrete mechanism: self-authored fixtures encode
the fixture-writer's own assumptions about how input is shaped (one
sentence per candidate), and a real dogfood run is what actually tests
whether that assumption holds outside the fixtures that were built to
confirm it.

## What We Should Stop / Continue / Change
- **Continue**: building each new independent-copy pattern (like the
  word-boundary resolver here) correct from the start when the correct
  version is already known from a prior phase's disclosed bug, rather than
  reintroducing a known defect and waiting for a fourth disclosure to fix
  it.
- **Continue**: real dogfood runs against genuine project material (this
  sprint's own history, not synthetic text) even when — especially when —
  the result contradicts every evaluation fixture's assumption.
- **Change (carried over from Sprints 05-11, now twelve skills deep)**:
  the independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was started at explicit user direction that reopened, for a second
  time, rather than resolved, the same-day freeze on new-skill work. The
  case for investing a sprint in L8/A5 before a thirteenth skill remains
  at least as strong as it was going into this sprint, arguably stronger
  now that it has been deferred twice in one day.

## Next Sprint Recommendation
No Phase 13 by default. The freeze from before Sprint 11 remains in force,
now deferred across two consecutive phase boundaries: re-justify against
real external validation evidence (a real user, an independent/blind eval
pass, or a real usage-comparison run) before starting any further skill
phase, per the adaptive-roadmap rule — this sprint's own existence is not
that evidence, and should not be read as precedent that asking unfreezes
the roadmap generally.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file, max 121), tested, pattern reuse worked cleanly, the word-boundary-correct-from-day-one resolver is a real design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run result that mostly surfaced a limitation rather than delivering usable candidates |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the eleventh time; perfect fixture scores are less informative than the real dogfood finding this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, ADR-018, known limitations, and the dogfood example all recorded with concrete evidence, including the honest single-line-resolution-window disclosure |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep |
| Learning | 4 | The line-vs-paragraph resolution gap is a genuinely new finding with a clear mechanism (fixture assumption vs. real prose shape), not just a confirmation of already-known patterns |
