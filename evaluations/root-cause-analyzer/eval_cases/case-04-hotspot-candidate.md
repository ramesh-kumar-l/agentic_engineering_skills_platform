# Case 04 — hotspot-candidate

- **Input**: `fixtures/case-04-hotspot-candidate/symptom.txt` (stale config
  value, no stack trace) + a synthetic `ci_report.json` where the top
  candidate is a codebase-intelligence-flagged hotspot with fan_in=6.
- **Expected Behavior**: the candidate report surfaces `engine/config_loader.py`
  first with `is_hotspot=true` and `fan_in=6`; the agent explicitly reasons
  about blast radius (checklist category 5) and fix-risk (category 9) using
  that real structural signal, not just the keyword match.
- **Acceptance Criteria**: top candidate is `engine/config_loader.py` with
  `is_hotspot=true`; actual derivation includes a `blast-radius` case and a
  `fix-risk` case both citing the real fan_in value.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: identifying the right candidate but ignoring
  the hotspot/fan-in signal when reasoning about how carefully to fix it.
