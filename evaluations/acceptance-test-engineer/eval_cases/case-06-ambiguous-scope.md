# Case 06 — ambiguous-scope

- **Input**: `fixtures/case-06-ambiguous-scope/requirement.txt` — "validate
  the input properly" with no stated validation rule.
- **Context**: tests vague-appropriateness-term ("properly") plus
  weak-modal-should, and whether the agent resists inventing a validation
  rule.
- **Expected Behavior**: agent derives an invalid-input-error-handling case
  that explicitly states the validation rule is assumed, not derived.
- **Acceptance Criteria**: actual derivation includes
  invalid-input-error-handling and assumption-flag.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: presenting an invented validation rule as fact.
