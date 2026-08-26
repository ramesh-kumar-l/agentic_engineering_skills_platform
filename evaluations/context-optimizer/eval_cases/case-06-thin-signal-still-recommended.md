# Case 06 — thin-signal-still-recommended

- **Input**: `fixtures/case-06-thin-signal-still-recommended/task.txt` —
  a thin task whose only real signal is one import line matching a
  keyword.
- **Context**: tests that the engine has no secondary noise-reduction
  cutoff above zero relevance (ADR-019's fail-OPEN discipline).
- **Expected Behavior**: `engine/report.py` recommended at score 1, tier
  `SUPPORTING`, not dropped for being "too weak."
- **Acceptance Criteria**: recommendation present; tier SUPPORTING.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a stricter minimum-score cutoff would have
  silently dropped this candidate — exactly the failure mode this skill
  is designed to avoid (missing needed context is worse than one extra
  weak recommendation).
