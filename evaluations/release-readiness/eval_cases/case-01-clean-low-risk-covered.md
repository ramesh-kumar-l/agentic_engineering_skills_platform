# Case 01 — clean-low-risk-covered

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-clean-low-risk-covered/diff.txt` (a
  type-annotation-only edit to `engine/util.py`) + a synthetic
  `ci_report.json` with 2 modules including a real covering test module.
- **Context**: a trivial, low-risk change to a low-fan-in, non-hotspot,
  genuinely test-covered module — no optional regression/security reports
  supplied.
- **Expected Behavior**: no hygiene flags fire; the file resolves with
  `structural_tier == "low"` (fan_in=0, not a hotspot); the file is
  genuinely covered by `tests/test_util.py`; `readiness_tier == "clear"`;
  `overall_verdict == "READY"`.
- **Acceptance Criteria**: `flag_ids == []`;
  `file_readiness_tiers["engine/util.py"] == "clear"`;
  `overall_verdict == "READY"`; the actual derivation explicitly notes both
  the absence of flags and the real coverage as positive evidence, not
  silence, and explains the verdict via the rule table rather than asserting it.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating a clean diff as automatically
  release-ready without checking the axes explicitly; missing real test
  coverage that is present.
