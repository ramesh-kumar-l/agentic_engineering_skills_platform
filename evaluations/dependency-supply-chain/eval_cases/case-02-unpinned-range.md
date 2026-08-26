# Case 02 — unpinned-range

- **Input**: `fixtures/case-02-unpinned-range/ci_report.json` — one
  dependency (`gamma>=1.0,<2.0`), a range specifier.
- **Context**: tests pin-status detection for a range (not wildcard, not
  missing) specifier.
- **Expected Behavior**: one `unpinned-range` flag (low severity, category
  `unpinned-version`); `suggested_risk_level == "NEEDS_REVIEW"`.
- **Acceptance Criteria**: flag present; risk level `NEEDS_REVIEW`; the
  derivation explains the reproducibility risk in its own words, not just
  echoes the flag's `description` field verbatim.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: misclassifying a range specifier as "pinned"
  because it contains a valid-looking version number.
