# Case 08 — vs-split-mixed-tier

- **Input**: `fixtures/case-08-vs-split-mixed-tier/decision.txt` (a single
  one-line question, no markers, using "vs") + a 1-module `ci_report.json`
  where `engine/search.py` is a hotspot, fan_in=9.
- **Context**: a new Elasticsearch cluster vs. the existing Postgres
  full-text search for the product catalog.
- **Expected Behavior**: the `vs` fallback shape produces 2 options; all
  three absence flags fire (no reversibility, tradeoff, or security
  language at all) — the only fixture where all three fire together; both
  alternatives match the same hotspot module.
- **Acceptance Criteria**: `option_count == 2`; `flags` includes all three
  absence pattern IDs; the actual derivation states plainly that this text
  is too thin to be a real decision record yet.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating a one-line question as if it were
  already a complete decision; missing that the vs-split shape itself
  satisfies the alternatives-signal check even without the word "option".
