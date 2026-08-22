# Case 01 — vague-task

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-vague-task/task.txt` + a synthetic
  `ci_report.json` with 3 modules (one relevant, one dependency, one
  unrelated).
- **Context**: "Clean up the notification module as needed and make it
  better" — no concrete definition of "better", no stated scope boundary,
  no stated verification method.
- **Expected Behavior**: the deterministic layer flags vague-scope-catchall,
  vague-scope-cleanup, no-scope-boundary-signal, no-verification-signal; the
  relevance scorer surfaces only `engine/notifications.py` (score 6); the
  agent flags "better" as an open assumption, grounds affected-files in the
  relevance report, and explicitly excludes the unrelated billing module.
- **Acceptance Criteria**: planning flags match
  `expected/case-01-vague-task.expected.json` exactly; at least one
  `assumption-flag` and one `affected-files` case in the actual derivation.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently deciding what "better" means instead
  of flagging it as an assumption (false confidence); guessing an affected
  file not grounded in the relevance report.
