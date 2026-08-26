# Case 03 — low-fan-in-keyword-match

- **Input**: `fixtures/case-03-low-fan-in-keyword-match/task.txt` —
  names "the stats module"; the composed CI report gives
  `engine/stats.py` fan_in=1, not a hotspot.
- **Context**: tests that a real but structurally unremarkable match
  lands in SUPPORTING, not CORE, without being dropped entirely.
- **Expected Behavior**: one recommendation, `engine/stats.py`, tier
  `SUPPORTING`.
- **Acceptance Criteria**: path match; no structural boost applied;
  score below `CORE_THRESHOLD`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: confirms the structural boost isn't applied
  when it shouldn't be — a false CORE promotion here would undermine the
  whole point of tiering by real structural data.
