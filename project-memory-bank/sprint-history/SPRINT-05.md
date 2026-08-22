# Sprint 05 — Phase 5: Security Context Guard

## Goal
Build a fifth skill by reusing Phase 2's judgment-based architectural
pattern a fourth time, implementing
[[06-security-model]]'s `Classify → Minimize → Sanitize → Authorize →
Execute → Audit` workflow as a runnable skill, and running a first honest
test toward A7 (does security handling increase trust) — the exit
criteria's core new requirement.

## Hypothesis
Pattern 2 (deterministic anti-pattern flagging + agent-driven derivation
against a fixed checklist) generalizes to a fourth judgment domain (security
classification, after diff review, requirement testability, and task
planning) without needing a new base pattern. Separately: a skill whose job
is a safety recommendation must make "the engine never authorizes" an
explicit, hard rule rather than an implicit convention — the stakes of
getting this wrong are categorically different from the prior three skills.

## Success Criteria
Engine modules <300 lines each; tests pass; evaluation harness runs against
8 seeded fixtures with real scores for both layers; `SKILL.md` meets the
canonical template with explicit advisory-only language; memory bank
updated per the user's "save state" requirement; a real dogfood run against
this phase's own real source and a real pending decision this session
actually faced, not a synthetic stand-in.

## Completed Work
`skills/security-context-guard/` (SKILL.md, engine, tests), an 8-fixture
evaluation harness scoring deterministic classification + judgment-layer
Precision/Recall, a dogfood run against a real git-push decision that found
and fixed a real bug in this skill's own action classifier (L16) and served
as Pilot C toward A7, `project-memory-bank/05-evaluation-framework.md`
(Security Decision Checklist added), `03-architecture.md` (Pattern 2 reused
a fourth time, ADR-011 note), `11-decisions.md` (ADR-011),
`12-known-limitations.md` (L16-L17), `16-assumptions-and-validation.md` (A5,
A7), `17-experiment-viability-check.md` (Pilot C), updated
`07-current-state.md`, `08-roadmap.md`, `implementation-status.md`,
`active-context.md`.

## Evidence
58/58 new tests passing; 149/149 across all five skills
(23+23+24+21+58). 8/8 evaluation fixtures: deterministic layer 100% correct
(automated); judgment layer 100% precision/recall — fourth judgment-based
skill scored this way, same self-authored, single-rater caveat as Phases
2-4, disclosed up front. One real finding from dogfooding: L16 (a genuine
action-classifier bug — fixed-distance window vs. real phrasing — found and
fixed same-session, the first dogfood finding located in the skill being
dogfooded rather than a different one).

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-4. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically from real agent-produced `actual/*.json`, same
methodology as Phase 2's first exercise of the "Agent Runtime" step.
Safety/Explainability left for human review, same discipline as before.

## Failures
None shipped. L16 (found via dogfooding, fixed within this sprint) is a
defect-shaped finding in this same skill — the first time that's happened
(L10/L13 were both cross-skill findings) — see [[12-known-limitations]].

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 2ms for the deterministic layer) and test/fixture pass rates
above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-011 (security-context-guard's engine classifies and recommends, never
authorizes) — see `11-decisions.md`. Pattern 2 (ADR-007) reused a fourth
time without a new base-pattern ADR — itself now stated as the project's
default architecture for judgment-based skills, logged in
`03-architecture.md`.

## Lessons Learned
Reusing an existing architectural pattern for a fourth, different judgment
domain worked cleanly again — four-for-four is now enough repetition that
Pattern 2 no longer needs re-justifying per skill, only per genuinely new
architectural fork (as ADR-010 and ADR-011 both were). The L16 finding
reinforced the standing lesson from L1/L13: real dogfooding against real
phrasing finds gaps synthetic fixtures don't, and this time the discipline
paid off inside the very skill being dogfooded, not just cross-skill —
proof the "dogfood everything for real" habit isn't just catching other
skills' gaps by luck. Pilot C's honest result (matched conclusion, not a
demonstrated decision change) is itself a useful, non-inflated data point:
it shows this project resists the temptation to round a null/neutral pilot
result up into a positive one.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against real, in-session, self-referential
  decisions wherever possible (this phase's git-push decision was real, not
  invented for the pilot) — it keeps pilots honest and has now found bugs
  in three different skills across three phases (L1, L13, L16).
- **Continue**: reuse an existing architectural pattern before inventing a
  new one; only add a new ADR when the reuse genuinely doesn't fit (ADR-011
  was necessary here — advisory-only-by-hard-rule is a real fork from the
  implicit "leads not verdicts" convention, not cosmetic).
- **Change (carried over from Sprints 02-04, still not done, now the
  loudest item on this list)**: the independent-rater evaluation (L8) is
  now four-for-four overdue, and A7's Pilot C makes the same point for
  Experiment-shaped assumptions generally — every "first test" this project
  runs on its own is structurally unable to move a status past UNKNOWN. A
  sixth skill should not be built before this gap is closed, or at minimum
  before the user explicitly re-affirms building more skills over closing
  it.

## Next Sprint Recommendation
Phase 6 (Root Cause Analyzer), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule. Same
alternative flagged in Sprints 03-04, now with the most weight behind it
yet: four consecutive perfect self-graded judgment scores, plus three
pilots (A/B/C) that all hit the same "N=1 self-run ceiling" wall, is a
strong case for investing a sprint in closing the independent-evidence gap
before adding a sixth skill.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular, tested, pattern reuse worked cleanly, new ADR-011 is a real hard-rule fork, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else |
| Evaluation Quality | 2 | Deterministic layer solid; judgment layer is self-authored/single-rater for the fourth time running (L8) — four-for-four is now the loudest unaddressed item in this project |
| Real-world Validation | 0 | Zero external usage; Pilot C is N=1/self-rated, not real user feedback |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations, and the dogfood example all recorded with concrete evidence, not just claims |
| Focus | 4 | One skill plus the explicitly-requested A7 pilot; no scope creep into Phase 6 |
| Learning | 4 | L16 is a genuinely new, non-trivial finding; Pilot C's honest null-ish result is itself a useful (if modest) piece of self-knowledge for the project |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
