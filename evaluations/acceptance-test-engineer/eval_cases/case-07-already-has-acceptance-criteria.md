# Case 07 — already-has-acceptance-criteria (positive case)

- **Input**: `fixtures/case-07-already-has-acceptance-criteria/requirement.txt`
  — two Given/When/Then scenarios already written out.
- **Context**: tests that the skill recognizes existing, sufficient criteria
  instead of manufacturing an unnecessary assumption-flag case.
- **Expected Behavior**: agent derives happy-path, invalid-input-error-
  handling, and negative-case directly from the given text; no
  assumption-flag case is needed since nothing is actually silent here.
- **Acceptance Criteria**: actual derivation covers happy-path,
  invalid-input-error-handling, negative-case; no fabricated assumption-flag.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: manufacturing an assumption where none is
  needed (over-flagging reduces trust as much as under-flagging).
