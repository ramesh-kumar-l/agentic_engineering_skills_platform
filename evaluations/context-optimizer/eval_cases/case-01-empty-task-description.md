# Case 01 — empty-task-description

- **Input**: `fixtures/case-01-empty-task-description/task.txt` — an empty
  file; a normal CI report with one file present.
- **Context**: tests the empty-input scope check — the engine must not
  fabricate recommendations from nothing.
- **Expected Behavior**: zero recommendations, an explicit "task
  description is empty" warning.
- **Acceptance Criteria**: `recommendations == []`; warnings non-empty.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently returning an empty-but-successful
  report with no explanation would hide *why* nothing was recommended.
