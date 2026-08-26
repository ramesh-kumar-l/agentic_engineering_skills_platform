# Case 07 — word-boundary-regression

- **Input**: `fixtures/case-07-word-boundary-regression/task.txt` — the
  keyword "scan"; the only file in the CI report is
  `engine/testability_scanner_utils.py`, whose name contains "scanner" as
  a component.
- **Context**: the L23 collision shape, applied to `relevance_scorer.py`'s
  tokenized matcher — "scan" must not match the "scanner" token.
- **Expected Behavior**: zero recommendations.
- **Acceptance Criteria**: `recommendations == []`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is the exact regression this skill's
  tokenizer was built to prevent from day one — a false positive here
  would mean the fifth independent copy of this fix shipped with the bug
  anyway.
