# Case 06 — compatibility-drift-blocks-execution

- **Input**: `fixtures/case-06-compatibility-drift-blocks-execution/task.txt`
  — a 2-step fake template whose downstream fixture has no SKILL.md at
  all, real (non-dry-run) execution requested.
- **Context**: exercises the compatibility checker as a pre-execution
  gate, not just a step-failure handler — this is a distinct fail-closed
  mechanism from case-05.
- **Expected Behavior**: exactly 1 compatibility issue found; both steps
  `SKIPPED`; no subprocess ever spawned.
- **Acceptance Criteria**: `compatibility_issue_count == 1`,
  `step_statuses == ["SKIPPED", "SKIPPED"]`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: without this gate, a registry entry with
  stale wiring would only be caught if and when the real downstream skill
  happened to reject the argument at runtime — this check catches it
  before any subprocess runs at all.
