# Case 03 — clean-fit-understand-then-optimize-context

- **Input**: `fixtures/case-03-clean-fit-understand-then-optimize-context/task.txt`
  — a task asking which files to load before starting work. Run
  `understand-then-optimize-context` with `--dry-run`.
- **Context**: the third real registry template, reusing Phase 13's own
  dogfood composition.
- **Expected Behavior**: both steps `PENDING`, zero compatibility issues.
- **Acceptance Criteria**: `step_statuses == ["PENDING", "PENDING"]`,
  `compatibility_issue_count == 0`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: same drift class as case-01 — a stale
  registry entry pointing at a `--ci-report`-style flag context-optimizer
  no longer has would surface as a compatibility issue here.
