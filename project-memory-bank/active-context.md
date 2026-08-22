# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 3 (acceptance-test-engineer) — COMPLETE, at a hard STOP per
[[08-roadmap]]'s phase protocol. Waiting for explicit user instruction before
starting Phase 4.

## What just happened

Built the acceptance-test-engineer skill end-to-end, reusing Pattern 2
(ADR-007) as-is rather than inventing a new base pattern: a deterministic
testability-anti-pattern engine (vague terms, weak modal verbs, error/
boundary-signal absence checks) + an agent-driven acceptance-case-derivation
workflow against a new 10-category coverage checklist (added to
[[05-evaluation-framework]]) + SKILL.md contract + 20 unit/integration tests
(all passing) + an 8-fixture evaluation harness scoring two layers separately
(same self-authored/single-rater caveat as Phase 2, disclosed up front this
time). Dogfooded against a real, already-shipped requirement — the actual
`--format`/`--out`/stdin behavior of `adversarial-diff-reviewer`'s CLI — which
surfaced a real, previously-undiscovered gap: that CLI had zero test
coverage. Fixed immediately (`tests/test_cli.py`, 4 new tests; that skill's
suite is now 23/23). See L10 in [[12-known-limitations]].

Also delivered the exit criteria's second half: a first Experiment A/B
viability check ([[17-experiment-viability-check.md]], new this phase). Ran
two explicitly-labeled internal pilots (N=1, self-run, un-blinded — NOT the
real experiments, per new ADR-009): Pilot A found the skill's "never guess
silently" discipline surfaced a real, checkable design question about
`argparse` behavior that direct reasoning likely would have skipped; Pilot B
found composing `codebase-intelligence`'s real Phase 1 output into
`acceptance-test-engineer` resolved a specific gap (which directories need
READMEs) the individual skill alone could only flag as an assumption.

## Open threads / not yet decided

- Phase 4 (Feature Planner) is proposed next per [[08-roadmap]] but not
  started and not re-justified against evidence yet — that re-justification
  happens at the start of Phase 4, not now.
- **L8 remains the most important open thread, now doubled**: both
  judgment-based skills (adversarial-diff-reviewer, acceptance-test-engineer)
  score 100% precision/recall against self-authored ground truth. Two-for-two
  perfect scores from self-grading is itself evidence this evaluation design
  can't discriminate good derivation from mediocre — not evidence either
  skill is actually good. The real inter-rater-agreement experiment still has
  not been run.
- **Experiment A/B are still not viable to run for real** — both pilots in
  [[17-experiment-viability-check.md]] found plausible signal on N=1, but per
  ADR-009 neither may be cited as validating A2 or A10. Both remain blocked
  on the same missing ingredient: an independent party.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3) scope boundaries
  remain deliberately deferred — revisit only if real usage shows they matter.
- No real (non-agent) engineer has used any of the three skills yet — Trust
  Status stays EXPERIMENTAL on all three, and assumptions A2/A3/A5/A10 in
  [[16-assumptions-and-validation]] remain only partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`,
   `skills/codebase-intelligence/SKILL.md`
5. [[17-experiment-viability-check.md]]

## Last updated

2026-08-23 — end of Phase 3.
