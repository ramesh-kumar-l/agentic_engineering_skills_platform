# Case 04 — hotspot-covered-needs-review

- **Input**: a comment-text edit to `engine/payment.py`, same hotspot as
  case-03 but this time WITH a real covering test module
  (`tests/test_payment.py`).
- **Context**: contrasts directly with case-03 — same structural profile,
  but coverage exists this time.
- **Expected Behavior**: `readiness_tier == "needs-review"` (not `clear`,
  because a high structural tier never drops all the way to clear per the
  rule table; not `blocked`, because coverage is real and no hygiene flag
  fired); `overall_verdict == "READY_WITH_CONDITIONS"`.
- **Acceptance Criteria**: the actual derivation must distinguish this from
  both case-03 (blocked, uncovered) and case-01 (clear, low structural).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "covered" with "clear" for a real
  hotspot; conflating this with case-03's blocked outcome.
