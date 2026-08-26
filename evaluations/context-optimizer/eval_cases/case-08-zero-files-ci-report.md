# Case 08 — zero-files-ci-report

- **Input**: `fixtures/case-08-zero-files-ci-report/task.txt` — a normal
  task description; the CI report declares zero files.
- **Context**: tests the degraded-precondition path — a technically valid
  but empty CI report must not silently produce an empty-but-successful
  report.
- **Expected Behavior**: zero recommendations, an explicit "zero files"
  warning.
- **Acceptance Criteria**: `recommendations == []`; warnings mention
  "zero files".
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: distinguishes "nothing was relevant" from
  "nothing could be assessed" — collapsing the two would hide a real
  upstream scan problem from the caller.
