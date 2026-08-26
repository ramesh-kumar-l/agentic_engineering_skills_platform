# Case 05 — step-failure-stops-chain

- **Input**: `fixtures/case-05-step-failure-stops-chain/task.txt` —
  `TRIGGER_FAIL` task text against a 3-step fake template
  (`skill-a` -> `skill-b` -> `skill-b`) using the pytest suite's own
  fake-skills fixtures, real (non-dry-run) execution.
- **Context**: exercises ADR-020's fail-closed default directly — a real
  subprocess failure must stop the chain, not let a later step run on
  absent/stale upstream data.
- **Expected Behavior**: step 1 `OK`, step 2 `FAILED`, step 3 `SKIPPED`.
- **Acceptance Criteria**: `step_statuses == ["OK", "FAILED", "SKIPPED"]`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: an executor that keeps running steps after a
  failure would let a downstream skill report false confidence built on
  broken upstream data — the exact failure mode ADR-020 exists to
  prevent.
