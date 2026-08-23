# Case 08 — multi-file-mixed-risk

- **Input**: `fixtures/case-08-multi-file-mixed-risk/diff.txt` (three files
  changed in one diff: `engine/core.py` loses exception handling on a real
  hotspot, `engine/util2.py` gets a harmless comment, `engine/helper.py`
  loses a conditional guard plus most of its body) + a synthetic
  `ci_report.json` with 8 real callers of `engine/core.py` and real coverage
  only for `engine/util2.py`.
- **Context**: exercises per-file aggregation and stats — a single diff
  should never be reviewed as uniformly risky or uniformly safe when its
  files' real risk profiles genuinely differ.
- **Expected Behavior**: `engine/core.py` and `engine/helper.py` both land
  at `overall_risk_tier == "high"` (for different structural reasons — one
  hotspot, one medium-tier-plus-uncovered); `engine/util2.py` stays `"low"`;
  `stats.high_risk_file_count == 2`.
- **Acceptance Criteria**: the actual derivation must name each file's tier
  separately with its own reasoning, not describe the diff as one blended
  risk level.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: aggregating three files' distinct risk profiles
  into one summary judgment; missing that `engine/util2.py`'s change is
  genuinely safe amid two risky files in the same diff.
