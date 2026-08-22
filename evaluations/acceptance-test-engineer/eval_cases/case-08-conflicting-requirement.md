# Case 08 — conflicting-requirement

- **Input**: `fixtures/case-08-conflicting-requirement/requirement.txt` — two
  sentences that contradict ("visible to all" vs. "only premium can click").
- **Context**: tests failure-first category 10 (incorrect requirement /
  contradiction) applied to acceptance-case derivation — can the agent
  surface a genuine internal contradiction rather than silently resolving it?
- **Expected Behavior**: agent derives an authorization-boundary case, an
  explicit assumption-flag case naming the contradiction, and a negative-case
  for the non-premium click path.
- **Acceptance Criteria**: actual derivation includes authorization-boundary,
  assumption-flag (naming the conflict explicitly), and negative-case.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently picking one interpretation of the
  conflict and presenting it as the only reading.
