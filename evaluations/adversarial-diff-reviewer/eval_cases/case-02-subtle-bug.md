# Case 02 — subtle-bug

- **Input**: `fixtures/case-02-subtle-bug/change.diff`.
- **Context**: `add_item` drops a `None`-sentinel guard in favor of a mutable
  default argument (`items=[]`).
- **Expected Behavior**: The agent recognizes the mutable-default-argument
  anti-pattern despite the diff looking like a simplification.
- **Acceptance Criteria**: A reported defect with `category == "subtle-bug"`,
  `file == "cart.py"`, mentioning shared/mutable state across calls.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is the canonical case regex cannot catch
  (no risk-flag pattern targets this) — a miss here would show the judgment
  layer isn't adding value over the deterministic layer alone.
