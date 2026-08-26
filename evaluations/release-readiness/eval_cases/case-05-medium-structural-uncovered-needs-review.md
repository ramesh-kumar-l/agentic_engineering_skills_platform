# Case 05 — medium-structural-uncovered-needs-review

- **Input**: a small behavioral change (added `ttl` argument) to
  `engine/session.py`, which has one real caller (`engine/auth.py`,
  fan_in=1) and no covering test module.
- **Context**: exercises the medium structural tier branch of the rule
  table, distinct from case-03's high/hotspot branch and case-04's
  high/covered branch.
- **Expected Behavior**: `readiness_tier == "needs-review"` (medium
  structural, no coverage); `overall_verdict == "READY_WITH_CONDITIONS"`.
- **Acceptance Criteria**: the actual derivation names both the real caller
  and the missing coverage explicitly, not just asserting the tier.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating a "not a hotspot" file as
  automatically low-risk, ignoring genuine fan_in=1 blast radius.
