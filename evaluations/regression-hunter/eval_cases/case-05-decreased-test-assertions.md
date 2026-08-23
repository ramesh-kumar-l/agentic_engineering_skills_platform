# Case 05 — decreased-test-assertions

- **Input**: `fixtures/case-05-decreased-test-assertions/diff.txt` (2 of 3
  `assert` lines removed from `test_add`, only 1 kept) + a synthetic
  `ci_report.json` where `tests/test_mathlib.py` itself is a listed module.
- **Context**: the changed file IS the test file — real verification
  coverage for `add()` decreased within the same commit.
- **Expected Behavior**: `decreased-test-assertions` fires (test-shaped path,
  more removed assert lines than added); structural tier is `low` (the test
  file itself has fan_in=0); no coverage (no OTHER test covers a test file);
  `overall_risk_tier == "medium"` per the rule table (low tier + flag + no
  coverage -> escalates from low to medium).
- **Acceptance Criteria**: `flag_ids == ["decreased-test-assertions"]`;
  `file_risk_tiers["tests/test_mathlib.py"] == "medium"`; the actual
  derivation correctly identifies the changed file as a test file itself,
  not production code losing test coverage.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: applying the assertion-count check to a
  non-test file; miscounting assertions across multiple hunks.
