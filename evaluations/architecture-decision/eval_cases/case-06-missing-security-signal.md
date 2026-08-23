# Case 06 — missing-security-signal

- **Input**: `fixtures/case-06-missing-security-signal/decision.txt` (two
  well-specified options with stated reversibility and tradeoffs, but no
  security mention) + a 2-module `ci_report.json`.
- **Context**: move user photos to S3 vs. keep local disk with a cron
  cleanup job.
- **Expected Behavior**: only `no-security-signal` fires; this is a real
  gap, not a false alarm — an S3 migration plausibly needs new credentials.
- **Acceptance Criteria**: `flags == ["no-security-signal"]`; the actual
  derivation names the concrete missing consideration (credentials/IAM)
  rather than treating the flag as boilerplate.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: dismissing the security flag as noise on a
  decision that otherwise reads as well-specified.
