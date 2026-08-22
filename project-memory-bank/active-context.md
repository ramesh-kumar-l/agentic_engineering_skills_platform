# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 4 (feature-planner) — COMPLETE, at a hard STOP per [[08-roadmap]]'s
phase protocol. Waiting for explicit user instruction before starting
Phase 5.

## What just happened

Built the feature-planner skill end-to-end, reusing Pattern 2 (ADR-007) a
third time rather than inventing a new base pattern: a deterministic
relevance-scoring engine (keyword-overlap against a codebase-intelligence
report, annotated with fan-in/fan-out/hotspot blast-radius signal) +
planning-anti-pattern flags (vague scope, weak goal modals, scope-boundary/
verification absence checks, mirroring acceptance-test-engineer's scanner)
+ an agent-driven structured-plan-derivation workflow against a new
10-category Plan Quality checklist (added to [[05-evaluation-framework]]) +
SKILL.md contract + 21 unit/integration tests (all passing) + an 8-fixture
evaluation harness scoring two layers separately (same self-authored/
single-rater caveat as Phases 2-3, now applying a third time).

The exit criteria's core new requirement — "first skill composing on top of
Codebase Intelligence's output" — was implemented as a genuine architectural
decision, not just documentation: **ADR-010**, logged in
[[11-decisions]]. Unlike every prior skill's optional composition,
feature-planner's engine requires a valid `codebase-intelligence`
`report.json` and refuses to run without one (`CiReportError`, actionable
exit-1 message).

Dogfooded against this platform's own current (4-skill) repository state —
regenerated a *fresh* `codebase-intelligence` report (the Phase-1-era one
predates 3 of the 4 skills now in the repo) and ran a real task against it.
Two genuine findings came out of that one real run:
- **L13** (fixed): `acceptance-test-engineer`'s own CLI had zero test
  coverage — the second cross-skill dogfood finding in this project (after
  L10), found purely as a side effect of grounding "affected files" in real
  structure, not from deliberately auditing coverage. Fixed same-session
  (`tests/test_cli.py`, 4 new tests; suite now 24/24).
- **L14** (documented, not fixed): the relevance scorer's path-weighting
  floods when a task's keywords collide with a shared directory name — the
  real target file ranked 13th of 65, not 1st. Left unfixed deliberately:
  this is the documented boundary between the deterministic lead-generator
  and the agent's Step 3 judgment (ADR-007), and in this same real run the
  agent's judgment correctly identified the right file anyway — the
  strongest concrete evidence yet that the two-layer split earns its
  complexity, not just a theoretical justification.

## Open threads / not yet decided

- Phase 5 (Security Context Guard) is proposed next per [[08-roadmap]] but
  not started and not re-justified against evidence yet — that
  re-justification happens at the start of Phase 5, not now.
- **L8 remains the most important open thread, now applying three times**:
  all three judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner) score 100% precision/recall
  against self-authored ground truth. Three-for-three is the established
  pattern now, not a new surprise — it continues to show this evaluation
  design can't discriminate good derivation from mediocre. The real
  inter-rater-agreement experiment still has not been run for any of the
  three.
- **Experiment A/B are still not viable to run for real** —
  [[17-experiment-viability-check.md]]'s pilots (Phase 3) found plausible
  signal on N=1; feature-planner's ADR-010 (Phase 4) is stronger evidence
  that required composition *executes correctly and is genuinely used*, but
  that is a narrower claim than Experiment B requires (composition
  *outperforms* the alternative, against an independent baseline). A10
  remains UNKNOWN per ADR-009's discipline.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4)
  scope boundaries remain deliberately deferred — revisit only if real
  usage shows they matter.
- No real (non-agent) engineer has used any of the four skills yet — Trust
  Status stays EXPERIMENTAL on all four, and assumptions A2/A3/A5/A10 in
  [[16-assumptions-and-validation]] remain only partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `skills/feature-planner/SKILL.md`, `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
5. `examples/feature-planner/example-run.md` (the L13/L14 findings)
6. [[17-experiment-viability-check.md]]

## Last updated

2026-08-23 — end of Phase 4.
