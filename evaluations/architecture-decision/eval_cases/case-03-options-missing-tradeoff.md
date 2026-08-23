# Case 03 — options-missing-tradeoff

- **Input**: `fixtures/case-03-options-missing-tradeoff/decision.txt` (two
  options + explicit reversibility, but no stated tradeoff or security
  consideration) + a 1-module `ci_report.json`.
- **Context**: rewrite a reporting module in Go vs. add caching in Python.
- **Expected Behavior**: `no-tradeoff-signal` and `no-security-signal` fire;
  reversibility is correctly recognized as present (not flagged).
- **Acceptance Criteria**: `flags == ["no-tradeoff-signal",
  "no-security-signal"]`; the actual derivation states the missing downside
  explicitly rather than treating Option A's framing as balanced.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: missing that reversibility IS present while
  correctly catching that tradeoffs are NOT.
