# Sprint 04 — Phase 4: Feature Planner

## Goal
Build a fourth skill by reusing Phase 2's judgment-based architectural
pattern a third time, and make composition with `codebase-intelligence`
architecturally mandatory rather than optional — the exit criteria's "first
skill composing on top of Codebase Intelligence's output."

## Hypothesis
Pattern 2 (deterministic anti-pattern flagging + agent-driven derivation
against a fixed checklist) generalizes to a third judgment domain (task
planning, after diff review and requirement testability) without needing a
new base pattern. Separately: making an upstream skill's output a hard
precondition (rather than optional context) is buildable, testable, and
will surface real value/limitations of composition that an optional-context
stance would never force into the open.

## Success Criteria
Engine modules <300 lines each; tests pass; evaluation harness runs against
8 seeded fixtures (each pairing a task with a synthetic codebase-
intelligence report) with real scores for both layers; `SKILL.md` meets the
canonical template; memory bank updated per the user's "save state"
requirement; a real dogfood run against this repo's own current state,
using a freshly regenerated codebase-intelligence report (not the stale
Phase-1-era one).

## Completed Work
`skills/feature-planner/` (SKILL.md, engine, tests), an 8-fixture evaluation
harness scoring deterministic planning-flags/relevance + judgment-layer
Precision/Recall, a dogfood run against a real task using a freshly
regenerated codebase-intelligence report that found and fixed a real gap in
a *different* skill (L13) and documented a real, deliberately-unfixed
limitation in this skill's own relevance ranking (L14),
`project-memory-bank/05-evaluation-framework.md` (Plan Quality checklist
added), `03-architecture.md` (Pattern 2 reused a third time, ADR-010 note),
`11-decisions.md` (ADR-010), `12-known-limitations.md` (L13-L15),
`16-assumptions-and-validation.md` (A5, A10), updated `07-current-state.md`,
`08-roadmap.md`, `implementation-status.md`, `active-context.md`.

## Evidence
21/21 new tests passing; 91/91 across all four skills (23+23+24+21, +4 of
the 24 in acceptance-test-engineer added this phase as the L13 fix). 8/8
evaluation fixtures: deterministic layer 100% correct (automated); judgment
layer 100% precision/recall — third judgment-based skill scored this way,
same self-authored, single-rater caveat as Phases 2-3, disclosed up front.
Two real findings from dogfooding: L13 (a genuine cross-skill test-coverage
gap, fixed) and L14 (a genuine relevance-ranking limitation, documented,
left unfixed with real evidence the agent's judgment compensates for it in
the same run).

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-3. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as Phase 2's first exercise of the "Agent Runtime" step.
Safety/Explainability left for human review, same discipline as before.

## Failures
None shipped. L13 (found via dogfooding, fixed within this sprint) is a
defect-shaped finding in a different skill; L14 is a documented, deliberate
non-fix — see [[12-known-limitations]].

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass rates
above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-010 (feature-planner requires codebase-intelligence's report as a hard
precondition) — see `11-decisions.md`. Pattern 2 (ADR-007) reused a third
time without a new base-pattern ADR — itself a decision, logged in
`03-architecture.md`.

## Lessons Learned
Reusing an existing architectural pattern for a third, different judgment
domain worked cleanly again — three-for-three is now real evidence the
Pattern 2 split isn't specific to any one domain. Making composition
mandatory (rather than optional, as in Phases 2-3) forced a genuinely useful
real-world test: regenerating a fresh codebase-intelligence report against
the repo's *current* state (rather than reusing the stale Phase-1 one) was
necessary to get an honest dogfood result, and doing so surfaced two real
things a synthetic fixture never would have: a genuine cross-skill test gap
(L13) and a genuine ranking weakness in the new engine itself (L14). The L14
finding is the most valuable single piece of evidence produced so far for
why the two-layer architecture (ADR-007) is worth its complexity — not
because the deterministic layer is perfect, but because it doesn't need to
be, and this phase caught that difference happening in a real run rather
than asserting it in the abstract.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against real (not just synthetic) input,
  and regenerate any composed upstream artifact fresh rather than reusing a
  stale one — reusing the stale Phase-1 report here would have hidden both
  L13 and L14.
- **Continue**: reuse an existing architectural pattern before inventing a
  new one; only add a new ADR when the reuse genuinely doesn't fit (ADR-010
  was necessary here — required-vs-optional composition is a real
  architectural fork, not a cosmetic difference).
- **Change (carried over from Sprints 02-03, still not done)**: the
  independent-rater evaluation (L8) is now three-for-three overdue. A fifth
  skill should not be built before this gap is closed, or at minimum before
  the user explicitly re-affirms building more skills over closing it.

## Next Sprint Recommendation
Phase 5 (Security Context Guard), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule. Same
alternative flagged in Sprint 03, now with more weight behind it: investing
a sprint in the independent-rater evaluation (L8) or a real Experiment A/B
(with an actual second party) before adding a fifth skill — three
consecutive perfect self-graded judgment scores is a stronger argument for
this than two was.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular, tested, pattern reuse worked cleanly, new ADR-010 is a real architectural fork, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else |
| Evaluation Quality | 2 | Deterministic layer solid; judgment layer is self-authored/single-rater for the third time running (L8) — three-for-three is now the established pattern, not new news |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, not just claims |
| Focus | 4 | One skill plus the explicitly-requested composition requirement; no scope creep into Phase 5 |
| Learning | 5 | L13 (cross-skill gap) and L14 (real evidence the two-layer split works) are both genuinely new and non-trivial findings |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
