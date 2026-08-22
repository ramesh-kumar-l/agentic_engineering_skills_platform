# Case 02 — well-scoped-task (negative case)

- **Input**: `fixtures/case-02-well-scoped-task/task.txt` + a synthetic
  `ci_report.json` with an export CLI, an import CLI, and an exporter
  helper module.
- **Context**: explicit scope ("Only... excluding the import CLI") and
  explicit verification ("Verify via a new test that...") — should trigger
  zero deterministic planning flags, same negative-case role as Phase 3's
  case-02.
- **Expected Behavior**: `planning_pattern_ids` is empty; the relevance
  scorer surfaces all three modules (the import CLI shares vocabulary even
  though it's explicitly out of scope); the agent must still explicitly
  exclude `engine/import_cli.py` as a non-goal despite its nonzero
  relevance score.
- **Acceptance Criteria**: zero planning flags; a `non-goal` case
  explicitly naming the excluded file; `affected-files` grounded only in
  the two in-scope modules.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating "nonzero relevance score" as
  equivalent to "in scope" and including the excluded file anyway.
