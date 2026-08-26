# Case 02 — hotspot-keyword-match

- **Input**: `fixtures/case-02-hotspot-keyword-match/task.txt` — names
  "the scanner module"; the composed CI report marks `engine/scanner.py`
  as a real hotspot (fan_in=9).
- **Context**: tests the intended positive path — a real keyword match on
  a structurally significant file promotes to CORE.
- **Expected Behavior**: one recommendation, `engine/scanner.py`, tier
  `CORE`, `is_hotspot == true`.
- **Acceptance Criteria**: path/tier match; hotspot boost applied.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is this skill's whole reason to compose
  on codebase-intelligence — a false negative here (failing to promote a
  real hotspot match) would be a serious defect.
