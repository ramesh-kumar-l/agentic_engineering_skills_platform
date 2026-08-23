# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 6 (root-cause-analyzer) — COMPLETE. Phase 7 (Refactoring Safety) not
started, still waiting on explicit user instruction per [[08-roadmap]]'s
phase protocol.

## What Phase 6 built

Built `root-cause-analyzer`, the sixth skill: `SKILL.md` contract reusing
Pattern 2 (ADR-007) a fifth time — a deterministic engine (11 modules, each
under 300 lines) that parses a symptom description, optionally extracts
stack-trace frames from it (Python tracebacks + generic `path:line`), and
scores `codebase-intelligence` modules as candidate root-cause locations in
two explicit evidence tiers (`stack-trace` — a dominant flat bonus when a
frame's path matches a real module — vs. `keyword` — the fallback
overlap-scoring tier, reusing `feature-planner`'s weighting scheme). 32
passing tests, including a CLI test file written from the start (same
discipline Phase 5 established). Combined with an agent-driven Root Cause
Investigation Checklist workflow — a new, fifth checklist in
[[05-evaluation-framework]] (10 categories: symptom restated, repro
context, candidate locations, evidence tier, blast radius, recent-change
correlation, ruled-out candidates, confirmation step, fix-risk note,
assumption flag).

**Architecture**: reuses `feature-planner`'s mandatory-composition rule
(ADR-010) a second time — a missing/malformed `codebase-intelligence`
report is a hard failure, not a degraded path. This is stated explicitly as
a *reuse*, not a new decision on that specific point. New this phase:
**ADR-012** — candidate locations are scored in two non-blended evidence
tiers rather than one blended score, so a stack-trace-confirmed location
is never presented with the same confidence as a coincidental keyword
match.

**Evaluation**: an 8-fixture harness (`evaluations/root-cause-analyzer/`),
same two-layer scoring (deterministic + judgment) as Phases 2-5. This is
the **fifth** judgment-based skill evaluated with self-authored,
single-rater fixtures, and the **first** whose judgment layer did **not**
score perfect precision/recall on every fixture: 7/8 perfect, case-03 at
0.67/0.67 (a genuine keyword-wording mismatch between the hand-authored
expected categories and the actual derivation, not a fabricated or
"corrected" result). Logged as L19 in [[12-known-limitations]] — the first
break in the "four-for-four perfect scores" pattern the L8 updates had been
tracking, itself a useful data point that this evaluation design *can*
diverge, not evidence this skill's diagnostic judgment is worse than the
other four's.

**Dogfood run** (`examples/root-cause-analyzer/example-run.md`):
regenerated a fresh `codebase-intelligence` report against this repo's
current (6-skill) state, then fed a natural-language description of Phase
5's own L16 defect (written without naming the file or the fix) into the
engine. The candidate scorer — keyword-tier evidence only, since L16 was a
silent misclassification with no stack trace — ranked `action_patterns.py`
(the file that actually contained that bug) first out of 122 scored
modules. Explicitly disclosed as a **retrospective validation**, not a new
bug find: L16 was already fixed in Phase 5. A prospective run against a
genuinely new, not-yet-diagnosed symptom remains the real, still-unrun
test.

**Memory-bank updates this phase**: `03-architecture.md` (Pattern 2 reused
a fifth time, "Pattern 2, reused for Phase 6" section), `05-evaluation-
framework.md` (Root Cause Investigation Checklist), `11-decisions.md`
(ADR-012), `12-known-limitations.md` (L18, L19, L8 update), `16-
assumptions-and-validation.md` (A5, A10 updated), `08-roadmap.md` (Phase 6
marked complete, Phase 7 proposed next), `implementation-status.md`,
`07-current-state.md`, `CHANGELOG.md`, `sprint-history/SPRINT-06.md`, root
`README.md` (skills table + architecture note), `skills/root-cause-
analyzer/README.md` (Status line).

## Open threads / not yet decided

- Phase 7 (Refactoring Safety) is proposed next per [[08-roadmap]] but not
  started and not re-justified against evidence yet — that re-justification
  happens at the start of Phase 7, not now.
- **L8 remains the most important open thread, now applying five times, and
  no longer a clean "four-for-four perfect scores" pattern**: four
  judgment-based skills (adversarial-diff-reviewer, acceptance-test-
  engineer, feature-planner, security-context-guard) scored 100% precision/
  recall against self-authored ground truth; the fifth (root-cause-
  analyzer) scored 7/8 perfect and 1/8 at 0.67/0.67 (L19). Both outcomes are
  equally inconclusive about real-world quality — self-authored,
  single-rater evidence either way. The inter-rater-agreement experiment
  (A5) still has not been run for any of the five.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, C) found
  plausible-but-narrow signal on N=1 each; Phase 6's dogfood run is
  additional real-usage evidence for A10 in the same shape as Phase 4's
  (composition genuinely required and used, correctly ranking a real
  historical root cause first), but still not the independently-baselined
  comparison Experiment B requires. None upgrades its assumption's status
  beyond UNKNOWN — the missing ingredient in every case is the same: a real
  second party this session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5), L18 (Phase 6, scope boundary) remain deliberately deferred
  — revisit only if real usage shows they matter.
- No real (non-agent) engineer has used any of the six skills yet — Trust
  Status stays EXPERIMENTAL on all six, and assumptions A2/A3/A5/A7/A10 in
  [[16-assumptions-and-validation]] remain only partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `README.md` (root) — primary public-facing entry point
5. `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
6. `examples/root-cause-analyzer/example-run.md` (the retrospective L16
   validation run)
7. [[17-experiment-viability-check.md]]
8. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with a Phase 6 post)

## Last updated

2026-08-23 — end of Phase 6.
