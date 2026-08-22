# Case 03 — missing-error-handling

- **Input**: `fixtures/case-03-missing-error-handling/requirement.txt` — a
  login requirement that never mentions incorrect credentials.
- **Context**: no-error-handling-signal should fire (whole-document absence
  check); tests whether the agent notices the gap the requirement leaves.
- **Expected Behavior**: agent derives an invalid-input-error-handling case
  and explicitly labels the reject-behavior as an assumption, not a fact.
- **Acceptance Criteria**: `no-error-handling-signal` present in testability
  flags; actual derivation includes an assumption-flag case referencing the
  missing incorrect-credentials behavior.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: presenting an invented reject-behavior as if the
  requirement stated it (false confidence, category 10 violation).
