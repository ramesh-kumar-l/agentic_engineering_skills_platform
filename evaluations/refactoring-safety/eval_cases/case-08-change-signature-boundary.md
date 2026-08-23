# Case 08 — change-signature-boundary

- **Input**: `fixtures/case-08-change-signature-boundary/refactor.txt` (a
  signature-change operation, fully specified: callers/tests/rollback/
  verification stated) + a synthetic `ci_report.json` with two real
  callers and one real covering test.
- **Context**: changing `notify.py`'s public function signature — a
  boundary-changing operation on a moderately-connected, non-hotspot
  module.
- **Expected Behavior**: `operation_type == "change-signature"` (not the
  generic `"refactor"` fallback); no safety flags fire; `risk_tier ==
  "medium"` (2 real callers, not a hotspot).
- **Acceptance Criteria**: `flags == []`; both real callers
  (`engine/orders.py`, `engine/alerts.py`) appear in `caller_modules`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: the operation parser falling back to the
  generic "refactor" type instead of recognizing "change the signature of"
  explicitly, which would lose the boundary-changing-vs-internal
  distinction `safety_scorer.py` relies on.
