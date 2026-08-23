# Case 02 — removed-exception-handling-hotspot-uncovered

- **Input**: `fixtures/case-02-removed-exception-handling-hotspot-uncovered/diff.txt`
  (a `try`/`except GatewayTimeout` block removed with no replacement from
  `engine/payment.py`) + a synthetic `ci_report.json` where `engine/payment.py`
  is a real hotspot with 3 real callers and zero test coverage.
- **Context**: a change to a genuinely high-blast-radius, genuinely uncovered
  module, removing its only error handling.
- **Expected Behavior**: `removed-exception-handling` fires; structural tier
  is `high` (hotspot); no test coverage; `overall_risk_tier == "high"` per the
  rule table (high structural tier + a flag -> HIGH regardless of coverage,
  and here coverage is absent too).
- **Acceptance Criteria**: `flag_ids == ["removed-exception-handling"]`;
  `file_risk_tiers["engine/payment.py"] == "high"`; the actual derivation
  names all three real callers and the absence of coverage explicitly.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: missing the removed exception handler because
  the surrounding hunk also contains an unrelated addition; failing to
  ground blast radius in the report's real caller list.
