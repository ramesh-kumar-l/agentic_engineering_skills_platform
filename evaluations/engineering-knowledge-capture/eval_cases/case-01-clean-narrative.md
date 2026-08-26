# Case 01 — clean-narrative

- **Input**: `fixtures/case-01-clean-narrative/narrative.txt` — a plain
  status update with no decision/lesson/limitation/workaround language.
- **Context**: the baseline negative case — confirms the scanner does not
  flag routine status text as a capture candidate.
- **Expected Behavior**: zero candidates, zero warnings.
- **Acceptance Criteria**: `report.candidates == []`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: over-eager pattern matching flagging ordinary
  prose as a "decision" or "lesson" just because it uses everyday words.
