# Case 08 — fix-risk-high-fanin

- **Input**: `fixtures/case-08-fix-risk-high-fanin/symptom.txt` — a stack
  trace pointing at a shared response-envelope builder used by every API
  endpoint (fan_in=14, hotspot).
- **Expected Behavior**: top candidate is stack-trace-confirmed
  `engine/response_builder.py`; the agent must separately surface the
  fix-risk implication (checklist category 9) of touching a module with
  fan_in=14 — any fix needs multi-endpoint regression coverage, not just a
  fix at the one call site that happened to surface the bug.
- **Acceptance Criteria**: top candidate is `engine/response_builder.py`
  with `evidence_tier=stack-trace`; actual derivation includes a `fix-risk`
  case explicitly citing fan_in=14 and the multi-endpoint blast radius.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: identifying the right file but proposing a
  narrow fix without acknowledging how many other call sites depend on it.
