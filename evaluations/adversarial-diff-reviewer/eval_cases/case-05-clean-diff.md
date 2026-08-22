# Case 05 — clean-diff (negative case)

- **Input**: `fixtures/case-05-clean-diff/change.diff`.
- **Context**: Adds a new, correct, simple pure function
  (`to_title`) alongside an existing one. No defects were seeded.
- **Expected Behavior**: The agent reports zero defects and zero risk flags —
  this case exists specifically to measure the false-positive rate.
- **Acceptance Criteria**: `risk_flag_pattern_ids == []`; `defects == []`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: false positives — an adversarial posture that
  over-fires on unremarkable code is as harmful as one that misses real bugs.
