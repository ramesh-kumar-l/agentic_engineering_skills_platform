# Case 07 — dependency-blocker-task

- **Input**: `fixtures/case-07-dependency-blocker-task/task.txt` + a
  synthetic `ci_report.json` with a reporting module and a db module.
- **Context**: "...once the migration script from the data team lands" —
  an explicit external precondition, testing the `dependency-blocker`
  checklist category specifically.
- **Expected Behavior**: relevance scorer surfaces both modules; the
  agent's `dependency-blocker` case must name the actual external blocker
  stated in the task and sequence the plan so it isn't started before the
  blocker clears.
- **Acceptance Criteria**: matches
  `expected/case-07-dependency-blocker-task.expected.json`; `step-sequence`
  case orders the blocker resolution first.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: writing a step sequence that ignores the
  stated external blocker entirely.
