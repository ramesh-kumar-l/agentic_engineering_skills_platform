# Case 01 — obvious-bug

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-obvious-bug/change.diff` — one file, one hunk.
- **Context**: `calculate_price` changes from multiplying by `(1 - discount)` to
  subtracting `discount` directly.
- **Expected Behavior**: The agent identifies that discount semantics changed
  from percentage to absolute amount — an obvious, high-severity logic bug.
- **Acceptance Criteria**: At least one reported defect with
  `category == "obvious-bug"`, `file == "billing.py"`, description matching
  keywords in `expected/case-01-obvious-bug.expected.json`.
- **Actual Result / Score**: see `../RESULTS.md` (scored against
  `actual/case-01-obvious-bug.actual.json`, this session's real review).
- **Failure Modes checked**: missing the defect entirely (false negative);
  no false positives on the same clean-looking single-line change.
