# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 5 (security-context-guard) — COMPLETE, at a hard STOP per
[[08-roadmap]]'s phase protocol. Waiting for explicit user instruction
before starting Phase 6.

## What just happened

Built the security-context-guard skill end-to-end, reusing Pattern 2
(ADR-007) a fourth time rather than inventing a new base pattern: a
deterministic classify/minimize/sanitize engine (secret/PII/sensitive-path/
action-category pattern tables, in-place redaction — every occurrence, not
just the first) + a deterministic sensitivity/`suggested_verdict` rollup
that fails closed on inconclusive input + an agent-driven Security Decision
Checklist workflow (7 categories, added to [[05-evaluation-framework]] as a
fourth checklist — shaped differently from the other three, a decision-gate
workflow rather than a coverage-enumeration list) + SKILL.md contract + 58
unit/integration tests (all passing, including a CLI test file written from
the start rather than discovered missing later) + an 8-fixture evaluation
harness scoring two layers separately (same self-authored/single-rater
caveat as Phases 2-4, now applying a fourth time).

The exit criteria's core new requirement — "first real test of A7" — was
addressed as honestly as currently possible without a real external user:
**Pilot C**, logged in [[17-experiment-viability-check.md]] under the same
ADR-009 governance as Pilot A/B. The real, in-session pending decision
("commit and push these Phase 5 files to the shared origin repository") was
run through the skill for real, and compared against an honest unstructured
baseline written before re-reading the structured output. The two
conclusions matched (this session already treats a git push as needing
confirmation, independent of this skill), so the pilot did not demonstrate
a changed decision — but it did produce a concrete, auditable evidence
trail an unstructured pass wouldn't spontaneously produce, and the dogfood
process itself caught a real bug. A7 stays UNKNOWN in
[[16-assumptions-and-validation]] — real qualitative feedback from an
actual user remains the missing ingredient, same shape as A2/A10's gap.

**New architectural decision — ADR-011**, logged in [[11-decisions]]:
extends ADR-008's redact-not-exclude discipline from diff-content secrets
specifically to a general classify/minimize/sanitize engine covering
secrets, PII, and high-risk actions, and establishes as a hard rule that
`classification.suggested_verdict` is always advisory — the engine never
authorizes anything itself, per [[06-security-model]]'s Human Approval
principle. Unlike `feature-planner`'s ADR-010, composition with
`codebase-intelligence` stays **optional** here (a `--ci-report` only adds a
hotspot-touch note).

Dogfooded against this phase's own real source file and a real pending
decision this session actually faced (not a synthetic fixture). One genuine
finding came out of that real run:
- **L16** (found and fixed same-session): the action classifier's
  `publishing` pattern used a fixed-distance proximity window between a
  verb ("push") and its target ("origin") — real phrasing put a
  parenthetical file list between them, 150+ characters apart. Widening the
  window (the first attempted fix) still wasn't enough at any reasonable
  size. **Real fix**: replaced the fixed window with same-sentence
  co-occurrence matching (`ActionPattern.matches()` in
  `action_patterns.py`) — a better-justified design, not a bigger magic
  number. This is the third "real dogfood run on real phrasing found a gap"
  finding (after L1, L13), and the first one found in the very skill being
  dogfooded rather than a different one.

## Open threads / not yet decided

- Phase 6 (Root Cause Analyzer) is proposed next per [[08-roadmap]] but
  not started and not re-justified against evidence yet — that
  re-justification happens at the start of Phase 6, not now.
- **L8 remains the most important open thread, now applying four times**:
  all four judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard) score
  100% precision/recall against self-authored ground truth. Four-for-four
  is the established pattern now, not a new surprise — it continues to show
  this evaluation design can't discriminate good derivation from mediocre.
  The real inter-rater-agreement experiment still has not been run for any
  of the four.
- **Experiment A/B and now A7's real experiment are all still not viable
  to run for real** — [[17-experiment-viability-check.md]]'s pilots (A, B,
  and now C) found plausible-but-narrow signal on N=1 each. None upgrades
  its assumption's status beyond UNKNOWN — the missing ingredient in every
  case is the same: a real second party (external engineer, independent
  rater, or real user) that this session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5) scope boundaries remain deliberately deferred — revisit
  only if real usage shows they matter.
- No real (non-agent) engineer has used any of the five skills yet — Trust
  Status stays EXPERIMENTAL on all five, and assumptions A2/A3/A5/A7/A10 in
  [[16-assumptions-and-validation]] remain only partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
5. `examples/security-context-guard/example-run.md` (the L16 finding + Pilot C)
6. [[17-experiment-viability-check.md]]

## Last updated

2026-08-23 — end of Phase 5.
