# Case 06 — merge-conflict-marker-blocked

- **Input**: a diff introducing three literal, unresolved merge-conflict
  markers into `engine/config.py`.
- **Context**: exercises the `merge-conflict-marker` hygiene pattern
  specifically — a shape distinct from debug leftovers/TODO markers/secrets.
- **Expected Behavior**: `flag_ids == ["merge-conflict-marker"]` (matched
  three times, once per marker line, though `flag_ids` as a set collapses
  to one distinct id); `readiness_tier == "blocked"`; `overall_verdict ==
  "NOT_READY"`.
- **Acceptance Criteria**: the actual derivation identifies this as an
  unambiguous, syntax-breaking blocker, the strongest-confidence hygiene
  category in the table.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: missing a conflict marker that isn't on a line
  starting with `+` in every hunk shape.
