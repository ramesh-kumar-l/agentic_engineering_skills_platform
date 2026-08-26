# Case 03 — single-lesson

- **Input**: `fixtures/case-03-single-lesson/narrative.txt` — a
  "turns out" root-cause correction, no module named nearby.
- **Context**: tests the lesson category specifically (distinct pattern
  table from decision).
- **Expected Behavior**: one `lesson-turns-out` candidate, unresolved,
  `suggested_capture_priority == "MEDIUM"`.
- **Acceptance Criteria**: category is `lesson`, not `decision` or any other.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: category confusion between lesson and decision
  markers.
