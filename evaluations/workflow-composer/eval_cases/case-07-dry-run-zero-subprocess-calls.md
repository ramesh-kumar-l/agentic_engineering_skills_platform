# Case 07 — dry-run-zero-subprocess-calls

- **Input**: `fixtures/case-07-dry-run-zero-subprocess-calls/task.txt` —
  same task shape as case-01, run with `--dry-run` against the real
  `understand-then-plan` template.
- **Context**: confirms the `--dry-run` contract itself — a plan can be
  validated (registry lookup + compatibility check) with zero real-world
  side effects, useful before committing to a timed real run.
- **Expected Behavior**: both steps `PENDING`; **no output files** written
  under the run's out-dir (distinct from case-01, which only checks step
  statuses).
- **Acceptance Criteria**: `step_statuses == ["PENDING", "PENDING"]` AND
  no `*.json`/`*.md` step-output files exist afterward.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a dry-run that still spawns subprocesses (or
  writes partial output) would defeat its own purpose as a cheap
  pre-execution check.
