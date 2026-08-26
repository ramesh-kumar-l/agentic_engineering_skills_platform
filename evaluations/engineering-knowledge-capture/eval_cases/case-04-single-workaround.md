# Case 04 — single-workaround

- **Input**: `fixtures/case-04-single-workaround/narrative.txt` — an
  explicit "workaround" statement naming an upstream issue.
- **Context**: tests the workaround category specifically.
- **Expected Behavior**: one `workaround-explicit` candidate, unresolved,
  `suggested_capture_priority == "MEDIUM"`.
- **Acceptance Criteria**: category is `workaround`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a workaround being treated as automatically
  lower-priority than a decision/lesson just because of its category.
