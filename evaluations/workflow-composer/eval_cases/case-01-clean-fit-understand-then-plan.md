# Case 01 — clean-fit-understand-then-plan

- **Input**: `fixtures/case-01-clean-fit-understand-then-plan/task.txt` — a
  task explicitly asking for a feature plan. Run `understand-then-plan`
  with `--dry-run` against the bundled tiny-repo fixture.
- **Context**: the simplest case — confirms a task that genuinely fits a
  registered template plans cleanly with zero compatibility drift.
- **Expected Behavior**: both steps report `PENDING` (dry-run), zero
  compatibility issues (real `feature-planner`/`codebase-intelligence`
  SKILL.md files still declare the composition correctly).
- **Acceptance Criteria**: `step_statuses == ["PENDING", "PENDING"]`,
  `compatibility_issue_count == 0`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a registry entry that no longer matches the
  real skills' declared contracts would surface here as a false
  compatibility issue on the simplest possible case.
