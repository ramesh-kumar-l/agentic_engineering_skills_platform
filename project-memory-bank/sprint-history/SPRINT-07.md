# Sprint 07 — Phase 7: Architecture Decision

## Goal
Build a seventh skill by reusing Phase 2's judgment-based architectural
pattern a sixth time and the mandatory-composition rule (ADR-010, already
reused once by `root-cause-analyzer` as ADR-012) a third time, turning a
free-text architecture-decision description into a per-option blast-radius
assessment grounded in a real structural map of the repo, per the user's
explicit exit criteria ("same bar, first skill composing on top of
Codebase Intelligence's output").

## Hypothesis
Pattern 2 (deterministic pre-processing + agent-driven derivation against a
fixed checklist) generalizes to a sixth judgment domain (weighing a
decision between alternatives, after diff review, requirement testability,
task planning, security classification, and root-cause diagnosis) without
needing a new base pattern. Separately: an option's blast radius should be
expressed as a real structural-risk tier (driven by fan-in/hotspot data),
not a bare keyword-relevance number, so a decision option touching a real
hotspot is never presented with the same confidence as one touching
nothing real.

## Note on the exit criteria's phrasing
As with Phase 6, the user's stated exit criteria — "first skill composing
on top of Codebase Intelligence's output" — was, factually, already true
of `feature-planner` (Phase 4, ADR-010) and reused once already by
`root-cause-analyzer` (Phase 6, ADR-012). This sprint reused ADR-010's rule
a third time rather than re-claiming a "first," and named the genuinely new
element separately (ADR-013's per-option blast-radius tiering). This is
also the second time within this same instruction that a phase-ordering
discrepancy needed correcting: the roadmap had proposed "Refactoring
Safety" for Phase 7 (with "Architecture Decision" slotted at Phase 8), but
the user's actual instruction named Architecture Decision for Phase 7. Both
discrepancies are stated plainly in `project-memory-bank/08-roadmap.md`
rather than silently absorbed.

## Success Criteria
Engine modules <300 lines each (strict modularity, explicit user
requirement, carried forward from Phase 6); tests pass, including a CLI
test file written from the start; evaluation harness runs against 8 seeded
fixtures with real scores for both layers; `SKILL.md` meets the canonical
template; memory bank updated per the user's "save state" requirement; a
real dogfood run against a genuine in-flight decision, not a purely
synthetic stand-in.

## Completed Work
`skills/architecture-decision/` (SKILL.md, engine — 11 modules, tests — 34
passing including CLI), an 8-fixture evaluation harness scoring
deterministic decision-flag/option-impact correctness + judgment-layer
Precision/Recall, a dogfood run (`examples/architecture-decision/`)
regenerating a fresh `codebase-intelligence` report against the repo's
current 7-skill state and assessing a real, in-flight decision (required
vs. optional composition for this very skill), `project-memory-bank/
05-evaluation-framework.md` (Architecture Decision Record Checklist added),
`03-architecture.md` (Pattern 2 reused a sixth time, ADR-013 note),
`11-decisions.md` (ADR-013), `12-known-limitations.md` (L20-L21),
`16-assumptions-and-validation.md` (A5, A10), `08-roadmap.md` (Phase 7
complete + reordering note, Phase 8 now Refactoring Safety),
`implementation-status.md`, `07-current-state.md`, `active-context.md`,
root `README.md`/`ROADMAP.md`/`QuickStarterGuide.md`/`DEPENDENCIES.md`
(skill-count refreshes).

## Evidence
34/34 new tests passing; 215/215 across all seven skills
(23+23+24+21+58+32+34). 8/8 evaluation fixtures: deterministic layer 100%
correct (automated); judgment layer 8/8 perfect precision/recall — unlike
Phase 6 (one non-perfect case), this is not read as evidence of higher
judgment quality, since a single self-authored evaluation cannot support
that comparison. Two real dogfood findings: (1) found-and-fixed — the
tradeoff-detection regex missed the verb phrasing "trades X for Y" (L20),
fixed same-session, all tests/fixtures re-verified passing after the fix;
(2) disclosed-not-fixed — at full-repository scale, a decision about the
platform's own architecture produced a blast-radius score of 240+ touching
all 10 hotspots for both options, a real but not useful signal caused by
the decision text's vocabulary overlapping the repo's own recurring
vocabulary (L21).

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-6. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as every prior phase. Safety/Explainability left for human
review, same discipline as before. Unlike Phase 6, no fixture scored
imperfectly this time — this was not engineered by adjusting expected
categories after the fact; all 8 fixtures' expected categories were
authored before any actual derivation was scored against them, same
protocol as every prior phase.

## Failures
None shipped as an undisclosed defect. L20 (tradeoff-regex verb-form gap)
is a real bug the dogfood run found and fixed same-session, not a shipped
failure. L21 (blast-radius signal degrading at full-repo scale) is a
disclosed, deliberately-unfixed limitation, not a shipped failure —
documented in `SKILL.md`'s "When NOT to Use" section so a future user
knows not to trust the blast-radius number for a decision about the
platform's own architecture at large.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-013 (per-option blast-radius scored in a three-tier structural-risk
band from real fan-in/hotspot data, rather than a bare relevance number) —
see `11-decisions.md`. `feature-planner`'s ADR-010 (mandatory composition
with `codebase-intelligence`) reused a third time, explicitly stated as a
reuse. Pattern 2 (ADR-007) reused a sixth time without a new base-pattern
ADR.

## Lessons Learned
Reusing an existing architectural pattern for a sixth, different judgment
domain worked cleanly again — the marginal cost of adding a judgment-based
skill to this platform continues to be dominated by the domain-specific
pattern table and checklist design, not by re-deriving the base
architecture. The real dogfood run, once again, earned its keep more than
the synthetic fixtures did: all 8 fixtures scored perfectly (nothing new
learned from them beyond confirming the harness works), while the single
real-decision dogfood run found one real bug and one real, more interesting
limitation the fixtures never would have surfaced, because they were
authored by the same session that would have to notice a gap to write a
fixture testing for it — the full-repo-scale vocabulary-collision problem
(L21) only exists at a scale no hand-authored 1-3-module fixture can
recreate. This reinforces a pattern visible since Phase 4 (L13/L14) and
Phase 5 (L16): real dogfooding on real text finds things synthetic
fixtures, written by the same author who wrote the tool, structurally
cannot.

## What We Should Stop / Continue / Change
- **Continue**: dogfooding every skill against something real whenever
  possible, and preferring the real-use finding over the fixture-only
  score as the more informative evidence — this phase's real bug (L20) and
  real limitation (L21) were both found this way, neither by the fixtures.
- **Continue**: correcting phase-ordering and exit-criteria phrasing
  discrepancies plainly in the roadmap rather than silently absorbing
  them — this is the second phase in a row where the instruction's
  framing didn't quite match the roadmap's prior state, and both times
  the discrepancy is now a matter of record, not a quiet drift.
- **Change (carried over from Sprints 05-06, now six skills deep)**: the
  independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was explicitly instructed to build a seventh skill instead. That is a
  legitimate user call, but the gap itself has not gotten smaller, and an
  eighth skill should not be built without either closing it or another
  explicit re-affirmation.

## Next Sprint Recommendation
Phase 8 (Refactoring Safety, per the roadmap's reordering this phase),
pending explicit user approval and re-justification against evidence per
the adaptive-roadmap rule. The same alternative flagged in Sprints 03-06
carries forward with even more weight: six consecutive skills evaluated
only by their own author is a strong case for investing a sprint in
closing the independent-evidence gap before adding an eighth skill,
especially since this phase's own dogfood run demonstrated exactly the
kind of finding (L21) that only surfaces through real, non-self-authored
use at scale — the same category of gap the inter-rater experiment would
help close for the judgment layer.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file), tested, pattern reuse worked cleanly, ADR-013 is a real scoring-design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run decision |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the sixth time; perfect fixture scores are less informative than the real dogfood findings this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, including the honest found-bug/disclosed-limitation split |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep |
| Learning | 4 | ADR-013's blast-radius tiering and L21's full-repo-scale limitation are both genuinely new, non-trivial findings |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
