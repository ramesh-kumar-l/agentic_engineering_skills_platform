# Case 04 — missing-boundary

- **Input**: `fixtures/case-04-missing-boundary/requirement.txt` — a
  playlist/song requirement with no stated size limit.
- **Context**: no-boundary-signal should fire; tests whether the agent flags
  the missing limit instead of inventing one.
- **Expected Behavior**: agent derives a boundary-edge-value case that states
  the limit is unknown/assumed, plus an explicit assumption-flag case.
- **Acceptance Criteria**: `no-boundary-signal` present in testability flags;
  actual derivation includes boundary-edge-value and assumption-flag.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently picking an arbitrary max-songs number.
