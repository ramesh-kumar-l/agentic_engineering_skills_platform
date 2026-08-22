# Sprint 02 — Phase 2: Adversarial Diff Reviewer

## Goal
Build the first judgment-based skill end-to-end (contract + deterministic
pre-processing engine + agent-driven adversarial workflow + evaluation),
establishing the counterpart architectural pattern to Phase 1's fully-
deterministic one.

## Hypothesis
A skill whose core task is judgment (not structure extraction) can still be
built with the same production discipline as Phase 1 — modular, tested,
evaluated — by splitting it into a deterministic pre-processing layer and an
agent-driven reasoning layer, each evaluated on its own terms.

## Success Criteria
Engine modules <300 lines each; tests pass; evaluation harness runs against 8
seeded-defect fixtures with real scores for both layers; SKILL.md meets the
canonical template; memory bank updated per the user's "save state"
requirement; at least one real (non-synthetic) diff reviewed.

## Completed Work
`skills/adversarial-diff-reviewer/` (SKILL.md, engine, tests), an 8-fixture
evaluation harness scoring deterministic risk-flags + judgment-layer
Precision/Recall, a dogfood run against a real in-session diff + 2 bug fixes,
`project-memory-bank/03-architecture.md` (Pattern 2 added),
`12-known-limitations.md` (L5-L9), ADR-007/008, updated `07-current-state.md`,
`08-roadmap.md`, `16-assumptions-and-validation.md` (A2, A5),
`implementation-status.md`, `active-context.md`, `CHANGELOG.md`, `README.md`,
`ROADMAP.md`.

## Evidence
19/19 tests passing. 8/8 evaluation fixtures: deterministic risk-flag layer
100% correct (automated); judgment layer 100% precision/recall — but this is
self-authored, single-rater evidence (same agent wrote fixtures, ground
truth, and review; see L8). Two real bugs found and fixed via dogfooding in
sequence: L5 (secret redaction missed raw diff content) and L6 (found by
adversarially re-reviewing the L5 fix itself — it only redacted the first
occurrence per line).

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phase 1. Judgment-layer Precision/Recall/False Positives/False Negatives
computed automatically, but from an input (`actual/*.json`) that required a
real agent turn to produce — the first real exercise of the "Agent Runtime"
step in `05-evaluation-framework.md`'s pipeline. Safety/Explainability left
for human review, same discipline as Phase 1.

## Failures
L5 (secret redaction gap in raw diff content) and L6 (incomplete
multi-occurrence redaction) — both found and fixed within this sprint, not
shipped. See `12-known-limitations.md`.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 1ms for the deterministic layer) and test/fixture pass rates
above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-007 (deterministic pre-processor + agent-driven adversarial workflow),
ADR-008 (redact-not-exclude for secrets in diff content) — see
`11-decisions.md`.

## Lessons Learned
Dogfooding a judgment-based skill against a real diff caught not one but two
sequential real bugs — the second only surfaced by applying the skill's own
adversarial-review discipline to its own prior fix. This is stronger evidence
for "always dogfood before closing a phase" than Phase 1 alone was. Separately:
building the evaluation fixtures, ground truth, AND performing the actual
review all within one agent session produces evaluation scores that look
excellent but are much weaker evidence than they appear — this is now
explicitly logged (L8) rather than left implicit.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against real (not just synthetic) input
  before closing a phase.
- **Continue**: keep engine modules single-responsibility and under 300 lines,
  regardless of whether the skill is deterministic or judgment-based.
- **Change**: for the next judgment-based skill, seriously consider getting a
  genuinely independent review (a second agent session with no visibility
  into the ground truth, or a human) before claiming any judgment-layer score
  — self-authored evaluation should not be repeated uncritically.

## Next Sprint Recommendation
Phase 3 (Acceptance Test Engineer), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular, tested, caught & fixed two of its own bugs |
| Usefulness | 2 | Not yet used on real engineering work by anyone else |
| Evaluation Quality | 2 | Deterministic layer solid; judgment layer is self-authored/single-rater (L8) — weaker than it looks |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations all recorded, including the L8 caveat |
| Focus | 5 | One skill, no scope creep into Phase 3+ |
| Learning | 5 | Two sequential real bugs caught via dogfooding; the self-evaluation-bias lesson is genuinely new |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
