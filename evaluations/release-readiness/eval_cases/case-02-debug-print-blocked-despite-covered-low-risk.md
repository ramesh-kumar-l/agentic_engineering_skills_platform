# Case 02 — debug-print-blocked-despite-covered-low-risk

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-02-debug-print-blocked-despite-covered-low-risk/diff.txt`
  (adds a `print("DEBUG ...")` line to `engine/util.py`) + the same synthetic
  `ci_report.json` as case-01 (low fan_in, genuinely test-covered).
- **Context**: **Deliberate divergence case #1** — a file with a real hygiene
  blocker but LOW structural risk and REAL test coverage. This exercises
  ADR-016's rule that a hygiene flag is an absolute blocker regardless of
  every other axis.
- **Expected Behavior**: `debug-print-leftover` fires; `readiness_tier ==
  "blocked"` even though structural tier is low and coverage is real;
  `overall_verdict == "NOT_READY"`.
- **Acceptance Criteria**: `flag_ids == ["debug-print-leftover"]`;
  `file_readiness_tiers["engine/util.py"] == "blocked"`; `overall_verdict ==
  "NOT_READY"`; the actual derivation must NOT let low structural risk or
  real coverage "outvote" the hygiene flag.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: incorrectly reasoning that a low-risk, covered
  file's hygiene flag is a minor issue that doesn't block release.
