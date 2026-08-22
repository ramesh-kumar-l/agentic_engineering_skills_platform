# Case 01 — vague-requirement

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-vague-requirement/requirement.txt` — one
  sentence with two unquantified adjectives and a weak modal verb.
- **Context**: "should load fast and be user-friendly" — no measurable
  threshold, no stated error path, no numbers.
- **Expected Behavior**: the deterministic layer flags vague-performance-term,
  vague-quality-term, weak-modal-should, no-error-handling-signal, and
  no-boundary-signal; the agent derives a happy-path case and explicitly
  flags the vague terms as an open assumption rather than picking a number.
- **Acceptance Criteria**: testability flags match
  `expected/case-01-vague-requirement.expected.json` exactly; at least one
  `happy-path` and one `assumption-flag` case in the actual derivation.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently inventing a load-time number instead of
  flagging it as an assumption (false confidence).
