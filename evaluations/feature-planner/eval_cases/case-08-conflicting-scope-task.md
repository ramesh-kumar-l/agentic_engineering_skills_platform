# Case 08 — conflicting-scope-task

- **Input**: `fixtures/case-08-conflicting-scope-task/task.txt` + a
  synthetic `ci_report.json` with a CLI module and a formatter module.
- **Context**: "only support JSON output" directly contradicts "keeps
  supporting the legacy plain-text output format" in the next sentence —
  mirrors acceptance-test-engineer's case-08 conflicting-requirement
  fixture; tests the same deterministic-layer blind spot (L11-shaped) for
  this skill.
- **Expected Behavior**: only `no-verification-signal` fires
  deterministically (the word "only" satisfies the scope-boundary check in
  isolation, masking the actual contradiction) — the agent's Step 3
  reasoning is the only layer that can catch the contradiction, and must
  disclose its resolution as an explicit assumption rather than silently
  picking one sentence over the other.
- **Acceptance Criteria**: matches
  `expected/case-08-conflicting-scope-task.expected.json`; the
  `scope-statement` case's `assumptions` field is non-null and names the
  contradiction explicitly.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently resolving the contradiction (picking
  JSON-only or plain-text-forever) without disclosing that a choice was
  made — the same false-confidence failure mode as case-01/case-04, applied
  to scope rather than verification.
