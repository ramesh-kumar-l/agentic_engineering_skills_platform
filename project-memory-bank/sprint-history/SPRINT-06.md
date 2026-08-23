# Sprint 06 — Phase 6: Root Cause Analyzer

## Goal
Build a sixth skill by reusing Phase 2's judgment-based architectural
pattern a fifth time and Phase 4's mandatory-composition rule (ADR-010) a
second time, turning a bug report (with or without a stack trace) into a
ranked, evidence-tiered set of candidate root-cause locations grounded in a
real structural map of the repo, per the user's explicit exit criteria
("same bar, first skill composing on top of Codebase Intelligence's
output").

## Hypothesis
Pattern 2 (deterministic pre-processing + agent-driven derivation against a
fixed checklist) generalizes to a fifth judgment domain (root-cause
diagnosis, after diff review, requirement testability, task planning, and
security classification) without needing a new base pattern. Separately: a
stack-trace-confirmed candidate location is categorically stronger evidence
than a keyword-overlap guess, and that difference should be encoded as an
explicit, non-blended tier in the engine's output — not left for the agent
to infer from a numeric score alone.

## Note on the exit criteria's phrasing
The user's stated exit criteria — "first skill composing on top of Codebase
Intelligence's output" — was, factually, already true of `feature-planner`
(Phase 4, ADR-010). Rather than silently re-claim that "first" for this
phase, this sprint reused ADR-010's rule explicitly (a second skill now
requires the same precondition) and named the genuinely new element
separately (ADR-012's tiered evidence scoring). Flagging this discrepancy
rather than quietly overclaiming novelty is itself the honesty discipline
this project has followed since Sprint 01.

## Success Criteria
Engine modules <300 lines each (strict modularity, explicit user
requirement this sprint); tests pass, including a CLI test file written
from the start (per Sprint 05's established discipline); evaluation harness
runs against 8 seeded fixtures with real scores for both layers; `SKILL.md`
meets the canonical template; memory bank updated per the user's "save
state" requirement; a real dogfood run against a genuine symptom, not a
purely synthetic stand-in.

## Completed Work
`skills/root-cause-analyzer/` (SKILL.md, engine — 11 modules, tests — 32
passing including CLI), an 8-fixture evaluation harness scoring
deterministic candidate/symptom-flag correctness + judgment-layer
Precision/Recall, a dogfood run (`examples/root-cause-analyzer/`)
regenerating a fresh `codebase-intelligence` report against the repo's
current 6-skill state and diagnosing a real, retrospective symptom (Phase
5's own L16 defect, described in natural language without naming the file),
`project-memory-bank/05-evaluation-framework.md` (Root Cause Investigation
Checklist added), `03-architecture.md` (Pattern 2 reused a fifth time,
ADR-012 note), `11-decisions.md` (ADR-012), `12-known-limitations.md`
(L18-L19), `16-assumptions-and-validation.md` (A5, A10), `08-roadmap.md`
(Phase 6 complete, Phase 7 proposed), `implementation-status.md`,
`07-current-state.md`, `active-context.md`, root `README.md` (skills table
+ test count).

## Evidence
32/32 new tests passing; 181/181 across all six skills
(23+23+24+21+58+32). 8/8 evaluation fixtures: deterministic layer 100%
correct (automated); judgment layer 7/8 fixtures perfect precision/recall,
1/8 (case-03) at 0.67/0.67 — the first non-perfect judgment score across
five judgment-based skills, disclosed as-is (L19). One real (if
retrospective) dogfood finding: the candidate scorer, using keyword-tier
evidence alone, ranked the true historical root-cause file
(`action_patterns.py`) first out of 122 scored modules from a
natural-language description of L16 that never named the file.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-5. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as every prior phase. Safety/Explainability left for human
review, same discipline as before. Case-03's 0.67/0.67 score was left as
computed — the expected-category keywords were not rewritten after seeing
the mismatch, since doing so would have been gaming the evaluation rather
than reporting it honestly.

## Failures
None shipped as a defect. The one below-perfect evaluation score (case-03)
is not a shipped failure — it's a disclosed evaluation-design artifact (a
keyword-wording mismatch between hand-authored expected categories and the
actual derivation's phrasing), logged as L19 rather than silently corrected.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass rates
above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-012 (tiered evidence scoring: stack-trace-confirmed candidates always
outrank keyword-overlap ones via a dominant, non-blended bonus) — see
`11-decisions.md`. `feature-planner`'s ADR-010 (mandatory composition with
`codebase-intelligence`) reused a second time, explicitly stated as a reuse
rather than a new decision. Pattern 2 (ADR-007) reused a fifth time without
a new base-pattern ADR.

## Lessons Learned
Reusing an existing architectural pattern for a fifth, different judgment
domain worked cleanly again, and reusing an already-established mandatory-
composition rule (rather than re-deriving whether this skill needed one)
saved real design time — the "ungrounded output is actively harmful" test
from ADR-010 applied cleanly to candidate-location diagnosis without
needing new justification. Sprint 05 explicitly flagged that a sixth skill
"should not be built before [the independent-rater evaluation] gap is
closed, or at minimum before the user explicitly re-affirms building more
skills over closing it" — the user's own Phase 6 instruction is exactly
that re-affirmation, so this sprint proceeded, but the gap itself remains
open and is now five skills deep, not four. The retrospective dogfood
run's honest framing (explicitly "not a new bug find") mattered: it would
have been easy to overstate a correct retrospective ranking as equivalent
to prospective diagnostic skill, and the write-up deliberately did not.
The first non-perfect judgment-layer score (case-03) is a genuinely useful
data point precisely because it was left alone rather than "fixed" —
proof this project's evaluation harness can and does produce results that
don't flatter the skill being evaluated.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against something real whenever
  possible, and state plainly when a dogfood run is retrospective
  validation rather than a live discovery — this phase's run would have
  been easy to overstate and wasn't.
- **Continue**: reuse an existing architectural decision explicitly (ADR-010
  here) rather than re-deriving or re-claiming novelty that isn't there —
  this phase corrected the user's own exit-criteria phrasing rather than
  quietly going along with an inaccurate "first."
- **Change (carried over from Sprint 05, now five skills deep)**: the
  independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was explicitly instructed to build a sixth skill instead. That is a
  legitimate user call, but the gap itself has not gotten smaller, and a
  seventh skill should not be built without either closing it or another
  explicit re-affirmation.

## Next Sprint Recommendation
Phase 7 (Refactoring Safety), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule. The same
alternative flagged in Sprints 03-05 carries forward with even more weight:
five consecutive skills evaluated only by their own author, plus a first
non-perfect score that — while honestly disclosed — still cannot by itself
distinguish genuinely-good diagnostic judgment from a fixture-wording
mismatch, is a strong case for investing a sprint in closing the
independent-evidence gap before adding a seventh skill.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file), tested, pattern reuse worked cleanly, ADR-012 is a real scoring-design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is retrospective |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the fifth time, but this time honestly produced a non-perfect score instead of extending an increasingly suspicious four-for-four streak |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, including the honest "retrospective, not a new find" framing |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep |
| Learning | 4 | ADR-012's tiered-evidence design and L19's honest imperfect score are both genuinely new, non-trivial findings |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
