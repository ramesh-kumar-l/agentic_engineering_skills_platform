# Case 02 — clean-fit-understand-then-test-plan

- **Input**: `fixtures/case-02-clean-fit-understand-then-test-plan/task.txt`
  — a task asking for acceptance criteria before implementation. Run
  `understand-then-test-plan` with `--dry-run`.
- **Context**: exercises the TEXT_APPEND wiring mode specifically —
  `acceptance-test-engineer` has no `--ci-report` flag, so this template's
  step 2 must be declared and checked differently from case-01/03.
- **Expected Behavior**: both steps `PENDING`, zero compatibility issues
  (acceptance-test-engineer's real SKILL.md names `codebase-intelligence`
  in its Required Context section as optional composed context).
- **Acceptance Criteria**: `step_statuses == ["PENDING", "PENDING"]`,
  `compatibility_issue_count == 0`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: declaring CLI_FLAG wiring here instead of
  TEXT_APPEND would be a real bug (acceptance-test-engineer's CLI would
  reject an unrecognized `--ci-report` flag) — this case's fixture-level
  compatibility check can't catch a wrong wiring *mode*, only a missing
  marker string, which is disclosed as a limitation, not silently assumed
  complete.
