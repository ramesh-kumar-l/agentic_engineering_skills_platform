# Case 02 — single-option-vague

- **Input**: `fixtures/case-02-single-option-vague/decision.txt` (one
  sentence, no alternatives, "just"/"obviously" language) + a 1-module
  `ci_report.json`.
- **Context**: proposing a background job queue for email sending.
- **Expected Behavior**: all five flags fire (vague-decision-language +
  four absence flags); the parser falls back to a single "proposed" option
  and the engine warns explicitly that no alternatives were parsed.
- **Acceptance Criteria**: `flags` includes all five pattern IDs;
  `options[0].label == "proposed"`; the actual derivation flags the
  confidence language as unsupported rather than accepting it.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: accepting "obviously simplest" as evidence;
  inventing an alternative the text never stated.
