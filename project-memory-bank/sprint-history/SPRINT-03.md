# Sprint 03 — Phase 3: Acceptance Test Engineer

## Goal
Build a second judgment-based skill by reusing Phase 2's architectural
pattern (rather than inventing a new one), and run a first honest viability
check on whether Experiment A and Experiment B are runnable now that 3
skills exist.

## Hypothesis
A judgment-based skill pattern (deterministic anti-pattern flagging +
agent-driven derivation against a fixed checklist) generalizes beyond its
original domain (diff review) to a different judgment domain (requirement
testability) without needing a new base pattern. Separately: once the core
thesis loop's three skills exist, it should be possible to at least assess —
even if not yet fully run — whether the product thesis's validation
experiments are viable.

## Success Criteria
Engine modules <300 lines each; tests pass; evaluation harness runs against 8
seeded fixtures with real scores for both layers; `SKILL.md` meets the
canonical template; memory bank updated per the user's "save state"
requirement; at least one dogfood run against real (non-synthetic) input;
a written Experiment A/B viability assessment with at least one bounded,
honestly-labeled pilot per experiment.

## Completed Work
`skills/acceptance-test-engineer/` (SKILL.md, engine, tests), an 8-fixture
evaluation harness scoring deterministic testability-flags + judgment-layer
Precision/Recall, a dogfood run against a real, already-shipped requirement
that found and fixed a real gap in a *different* skill's code (L10),
`project-memory-bank/05-evaluation-framework.md` (acceptance-coverage
checklist added), `03-architecture.md` (Pattern 2 reuse documented),
`12-known-limitations.md` (L10-L12), `11-decisions.md` (ADR-009),
`17-experiment-viability-check.md` (new), updated `07-current-state.md`,
`08-roadmap.md`, `16-assumptions-and-validation.md` (A2, A5, A10),
`implementation-status.md`, `active-context.md`, `CHANGELOG.md`, `README.md`,
`ROADMAP.md`.

## Evidence
20/20 new tests passing; 66/66 across all three skills. 8/8 evaluation
fixtures: deterministic testability-flag layer 100% correct (automated);
judgment layer 100% precision/recall — same self-authored, single-rater
caveat as Phase 2 (L8), disclosed up front this time rather than discovered
after the fact. One real gap found and fixed via dogfooding: L10
(`adversarial-diff-reviewer`'s CLI had zero test coverage) — the first
cross-skill dogfood finding in this project. Two explicitly-labeled N=1
pilots run for Experiment A/B viability, each finding a real, bounded signal
without claiming experiment-level validity.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-2. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as Phase 2's first exercise of the "Agent Runtime" step.
Safety/Explainability left for human review, same discipline as before.

## Failures
None shipped. L10 (found via dogfooding, fixed within this sprint) is the
only defect-shaped finding — see [[12-known-limitations]].

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass rates
above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-009 (internal viability pilots must never be presented as the validated
experiment) — see `11-decisions.md`. Pattern 2 (ADR-007) reused without a new
ADR — itself a decision, logged in `03-architecture.md`.

## Lessons Learned
Reusing an existing architectural pattern for a second, different judgment
domain worked cleanly with zero friction — real evidence the Pattern 2 split
(deterministic leads + agent-driven checklist reasoning) is not diff-review-
specific. Separately: dogfooding a *new* skill against a *previous* phase's
shipped code found a real gap in that previous phase's work — a stronger
form of the "always dogfood" lesson from Sprint 02, since it shows dogfooding
value compounds across phases, not just within one. Also: getting a second
100%/100% self-graded judgment-layer score confirms (rather than just
suspects) that this evaluation design has a real ceiling problem — it cannot
yet tell a good derivation from a mediocre one, and that gap is now the most
important unresolved methodology question in the project.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against real (not just synthetic) input
  before closing a phase — and prefer targets from *other* phases' shipped
  code when available, since Phase 3 showed that surfaces cross-cutting gaps.
- **Continue**: reuse an existing architectural pattern before inventing a
  new one; only add a new ADR when the reuse genuinely doesn't fit.
- **Change**: stop treating "ran a viability pilot" as separate from "ran the
  experiment" in casual language anywhere in the repo — ADR-009 exists
  specifically because this distinction is easy to blur under time pressure.
- **Change (carried over from Sprint 02, still not done)**: the next
  judgment-based skill, or a return pass on these two, should get a
  genuinely independent review before any further precision/recall claim is
  made — two consecutive perfect self-graded scores is now itself the
  argument for doing this, not just a nice-to-have.

## Next Sprint Recommendation
Phase 4 (Feature Planner), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule. Alternative
worth flagging to the user: investing a sprint in the independent-rater
evaluation (L8) or a real Experiment A/B (with an actual second party) before
adding a fourth skill, since the evidence gap there is now larger than the
skill-count gap.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular, tested, pattern reuse worked cleanly |
| Usefulness | 2 | Not yet used on real engineering work by anyone else |
| Evaluation Quality | 2 | Deterministic layer solid; judgment layer is self-authored/single-rater for the second time running (L8) — the ceiling problem is now confirmed, not just suspected |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and a new dedicated viability-check file all recorded |
| Focus | 4 | One skill plus the explicitly-requested viability check; no scope creep into Phase 4 |
| Learning | 5 | Cross-skill dogfood finding (L10), pattern-reuse evidence, and the ADR-009 pilot-vs-experiment distinction are all genuinely new |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
