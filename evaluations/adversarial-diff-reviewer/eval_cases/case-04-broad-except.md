# Case 04 — broad-except

- **Input**: `fixtures/case-04-broad-except/change.diff`.
- **Context**: A payment charge call is wrapped in `except Exception: pass`,
  and the following line unconditionally logs success.
- **Expected Behavior**: The agent catches the compounding defect — not just
  "broad except" in isolation, but that it causes a false success log after a
  silently swallowed payment failure.
- **Acceptance Criteria**: `risk_flag_pattern_ids` includes
  `"broad-except-exception"`; a reported defect mentioning the false
  success log / swallowed failure, not just the bare except pattern.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: agent restating only the mechanical risk flag
  (broad except) without connecting it to the actual consequence (false
  success reporting on a financial operation).
