# Case 03 — removed-conditional-guard-covered-medium

- **Input**: `fixtures/case-03-removed-conditional-guard-covered-medium/diff.txt`
  (an `if user is None: return` guard removed with no replacement from
  `engine/session.py`) + a synthetic `ci_report.json` with a real covering
  test module and one real caller.
- **Context**: a structurally moderate (fan_in=1, not a hotspot), genuinely
  covered module with a removed guard.
- **Expected Behavior**: `removed-conditional-guard` fires; structural tier
  is `medium`; the file is genuinely covered; `overall_risk_tier == "medium"`
  per the rule table (medium tier + flag + coverage -> stays medium, does not
  escalate to high the way an uncovered medium-tier flagged file would).
- **Acceptance Criteria**: `flag_ids == ["removed-conditional-guard"]`;
  `file_risk_tiers["engine/session.py"] == "medium"`; the actual derivation
  distinguishes this from case-04's escalation to HIGH by naming the real
  coverage as the reason it doesn't escalate.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating "flag fired" and "structurally risky"
  as automatically HIGH regardless of coverage; missing real coverage.
