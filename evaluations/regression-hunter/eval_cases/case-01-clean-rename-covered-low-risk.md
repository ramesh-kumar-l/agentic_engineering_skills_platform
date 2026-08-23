# Case 01 — clean-rename-covered-low-risk

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-clean-rename-covered-low-risk/diff.txt` (a
  single-line comment edit to `engine/util.py`) + a synthetic `ci_report.json`
  with 2 modules including a real covering test module.
- **Context**: a trivial, low-risk change to a low-fan-in, non-hotspot,
  genuinely test-covered module.
- **Expected Behavior**: no diff-pattern flags fire; the file resolves with
  `structural_tier == "low"` (fan_in=0, not a hotspot); the file is genuinely
  covered by `tests/test_util.py`; `overall_risk_tier == "low"`.
- **Acceptance Criteria**: `flag_ids == []`; `file_risk_tiers["engine/util.py"]
  == "low"`; the actual derivation explicitly notes both the absence of flags
  and the real coverage as positive evidence, not silence.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating a clean diff as automatically
  risk-free without checking the axes explicitly; missing real test coverage
  that is present.
