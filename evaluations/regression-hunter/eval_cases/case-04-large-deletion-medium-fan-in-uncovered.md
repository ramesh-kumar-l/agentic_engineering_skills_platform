# Case 04 — large-deletion-medium-fan-in-uncovered

- **Input**: `fixtures/case-04-large-deletion-medium-fan-in-uncovered/diff.txt`
  (14 lines of `build_summary`'s real aggregation logic deleted with zero
  lines added in the same hunk) + a synthetic `ci_report.json` where
  `engine/report_builder.py` has fan_in=2, is not a hotspot, and has zero
  test coverage.
- **Context**: a structurally moderate, genuinely uncovered module with a
  large, unreplaced deletion.
- **Expected Behavior**: `large-deletion-no-addition` fires (14 removed, 0
  added lines, past the 10-line threshold); structural tier is `medium`; no
  coverage; `overall_risk_tier == "high"` per the rule table (medium tier +
  flag + no coverage -> escalates to HIGH).
- **Acceptance Criteria**: `flag_ids == ["large-deletion-no-addition"]`;
  `file_risk_tiers["engine/report_builder.py"] == "high"`; the actual
  derivation explains the escalation via the rule table, not just asserts it.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: the flag not firing because a small stub
  addition (e.g. `return {}`) is present in the same hunk, which would
  incorrectly cancel a genuinely large, unreplaced deletion — this fixture
  deliberately has ZERO additions in the hunk to trigger it correctly.
