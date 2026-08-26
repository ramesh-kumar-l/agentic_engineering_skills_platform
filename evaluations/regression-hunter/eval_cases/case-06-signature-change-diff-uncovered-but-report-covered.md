# Case 06 — signature-change-diff-uncovered-but-report-covered

- **Input**: `fixtures/case-06-signature-change-diff-uncovered-but-report-covered/diff.txt`
  (`def handle(request):` changed to `def handle(request, ctx):`, no other
  file changed in this diff) + a synthetic `ci_report.json` where
  `tests/test_api.py` genuinely imports `engine.api`.
- **Context**: deliberately exercises the divergence between Axis 1's
  diff-level "no test file changed in THIS diff" signal and Axis 3's
  report-level "does a real test module import this file" signal — the two
  are independent and can disagree.
- **Expected Behavior**: `modified-signature-no-test-change` fires (no
  test-shaped file among the diff's OTHER changed files); structural tier is
  `medium` (fan_in=2); `test_coverage.has_coverage == True` (the composed
  report shows real coverage); `overall_risk_tier == "medium"` per the rule
  table.
- **Acceptance Criteria**: both the flag AND `has_coverage=True` appear in
  the report simultaneously — the actual derivation must explicitly state
  this is a real, deliberate divergence, not a contradiction or a bug.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "no test file touched in this diff"
  with "this file has no real test coverage" — the exact conflation
  `refactoring-safety`'s case-03 (L-numbered precedent) already tested for
  a different skill's analogous divergence.
