# Case 04 — no-verification-task

- **Input**: `fixtures/case-04-no-verification-task/task.txt` + a synthetic
  `ci_report.json` with a payment worker and a backoff helper.
- **Context**: scope is stated ("Only touch...") but no test/verification
  language appears anywhere — isolates the `no-verification-signal`
  absence check from the scope-boundary check.
- **Expected Behavior**: only `no-verification-signal` fires (scope
  boundary is satisfied by "Only"); the agent must flag the verification
  approach itself as an assumption rather than silently inventing one
  without disclosure.
- **Acceptance Criteria**: matches
  `expected/case-04-no-verification-task.expected.json`; the `test-hook`
  case's `assumptions` field is non-null.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: presenting an invented test strategy as if it
  were derived from the task, rather than disclosed as an assumption.
