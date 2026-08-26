# Case 04 — tight-budget-excludes-lower-relevance

- **Input**: `fixtures/case-04-tight-budget-excludes-lower-relevance/task.txt`
  — mentions three equally-named files (alpha/beta/gamma); alpha is a
  hotspot, beta and gamma are not. Run with `--budget-lines 50`.
- **Context**: tests budget-constrained EXCLUDED tiering — the one CORE
  candidate must survive, lower-tier candidates that don't fit must be
  excluded explicitly, not silently.
- **Expected Behavior**: `engine/alpha.py` stays CORE; `engine/beta.py`
  and `engine/gamma.py` (SUPPORTING, tied scores) both flip to EXCLUDED.
- **Acceptance Criteria**: alpha's tier unchanged; beta/gamma tier ==
  EXCLUDED with a note.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a budget mechanism that silently drops
  candidates without marking them EXCLUDED (or that excludes the CORE
  candidate instead of the SUPPORTING ones) would defeat the whole point
  of tiering before budgeting.
