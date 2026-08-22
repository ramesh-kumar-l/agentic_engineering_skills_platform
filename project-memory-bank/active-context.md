# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 2 (adversarial-diff-reviewer) — COMPLETE, at a hard STOP per
[[08-roadmap]]'s phase protocol. Waiting for explicit user instruction before
starting Phase 3.

## What just happened

Built the adversarial-diff-reviewer skill end-to-end: a new architectural
pattern (deterministic risk-flagging engine + agent-driven adversarial review
workflow, ADR-007/008 — the judgment-based counterpart to Phase 1's fully-
deterministic pattern) + SKILL.md contract + 19 unit/integration tests (all
passing) + an 8-fixture evaluation harness scoring two layers separately
(deterministic risk flags, automated; judgment findings, this session's agent
actually performing the review) + a dogfood run against a real diff from
earlier in this same session. Dogfooding surfaced and fixed two real bugs in
sequence: L5 (secret redaction didn't cover raw diff content, only the risk
flag) and L6 (found by adversarially re-reviewing the L5 fix itself — the fix
only redacted the first occurrence of a secret pattern per line, not all of
them). See [[12-known-limitations]].

## Open threads / not yet decided

- Phase 3 (Acceptance Test Engineer) is proposed next per [[08-roadmap]] but
  not started and not re-justified against evidence yet — that
  re-justification happens at the start of Phase 3, not now.
- **L8 is the most important open thread**: the Phase 2 evaluation's 100%
  precision/recall is self-authored, single-rater evidence — this session's
  agent wrote the fixtures, the ground truth, AND performed the review. The
  actual inter-rater-agreement experiment A5 has called for since Phase 1
  still has not been run. Do not let this score be cited as proof the skill
  reviews code well.
- L2/L3/L4 (Phase 1) and L7/L9 (Phase 2 scope boundaries) remain deliberately
  deferred — revisit only if real usage shows they matter.
- No real (non-agent) engineer has used either skill yet — Trust Status stays
  EXPERIMENTAL on both, and assumptions A2/A3/A5 in
  [[16-assumptions-and-validation]] remain only partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `skills/adversarial-diff-reviewer/SKILL.md` and
   `skills/codebase-intelligence/SKILL.md`

## Last updated

2026-08-23 — end of Phase 2.
