# Case 03 — security-issue

- **Input**: `fixtures/case-03-security-issue/change.diff`.
- **Context**: A parameterized SQL query is replaced with string concatenation
  of user-controlled input.
- **Expected Behavior**: Both the deterministic risk-flag layer
  (`sql-string-concat`) and the agent's judgment layer independently flag
  this as a SQL injection vulnerability.
- **Acceptance Criteria**: `risk_flag_pattern_ids` includes
  `"sql-string-concat"`; a reported defect with `category == "security-issue"`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: false negative on the mechanical layer (pattern
  regex not firing); agent treating the risk flag as sufficient without its
  own confirming reasoning.
