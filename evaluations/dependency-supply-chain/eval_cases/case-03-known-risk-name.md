# Case 03 — known-risk-name

- **Input**: `fixtures/case-03-known-risk-name/ci_report.json` — one
  dependency, `request@2.88.0` from `package.json`.
- **Context**: `request` matches `risk_patterns.py`'s curated table
  (deprecated by its maintainer in 2020).
- **Expected Behavior**: one `known-risk-name` flag (medium severity);
  `suggested_risk_level == "NEEDS_REVIEW"`.
- **Acceptance Criteria**: flag present; the derivation verifies the cited
  incident (deprecation notice) rather than repeating it uncritically, and
  distinguishes `request` from the real, actively-maintained `requests`
  package (exact-name match, not substring).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: substring-matching `request` against
  `requests` and producing a false positive on an unrelated, healthy
  package — the same precision discipline as the project's L23 fix.
