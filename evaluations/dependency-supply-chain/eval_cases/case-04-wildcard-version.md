# Case 04 — wildcard-version

- **Input**: `fixtures/case-04-wildcard-version/ci_report.json` — one
  dependency, `delta@*`.
- **Context**: a wildcard specifier — the most severe pin-status category,
  since literally any published version (including a future, compromised
  one) resolves.
- **Expected Behavior**: one `unpinned-wildcard` flag, **high** severity
  (unlike a plain range, which is low); `suggested_risk_level ==
  "REQUIRES_REVIEW"`.
- **Acceptance Criteria**: flag present with `severity == "high"`; risk
  level escalates to `REQUIRES_REVIEW` on this single flag alone (the
  rollup rule: any high-severity flag forces `REQUIRES_REVIEW`); the
  derivation explains why a wildcard is materially worse than a range, not
  just louder.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating "unpinned" as a single undifferentiated
  bucket instead of recognizing wildcard as categorically riskier.
