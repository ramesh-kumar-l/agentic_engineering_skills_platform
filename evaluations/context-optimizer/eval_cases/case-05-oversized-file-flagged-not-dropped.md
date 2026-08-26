# Case 05 — oversized-file-flagged-not-dropped

- **Input**: `fixtures/case-05-oversized-file-flagged-not-dropped/task.txt`
  — names "the giant module" (500 lines). Run with `--budget-lines 100`.
- **Context**: tests ADR-019's fail-OPEN rule at the budget boundary — a
  single file whose own size exceeds the budget must never be silently
  dropped.
- **Expected Behavior**: `engine/giant.py` recommended, `oversized_alone
  == true`, tier unchanged (not EXCLUDED), with a note recommending an
  excerpt or split.
- **Acceptance Criteria**: `oversized_alone == true`; tier stays
  SUPPORTING; a note is present.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is the direct callback to the user's
  own <300-line-per-file modularity instruction this session — silently
  excluding this file would hide the exact file most likely to need that
  advice.
