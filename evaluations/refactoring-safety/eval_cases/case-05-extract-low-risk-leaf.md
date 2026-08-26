# Case 05 — extract-low-risk-leaf

- **Input**: `fixtures/case-05-extract-low-risk-leaf/refactor.txt` (an
  extract operation, fully specified: tests + rollback stated) + a
  synthetic `ci_report.json` where the target is a genuine leaf module
  (zero fan-in, not a hotspot).
- **Context**: extracting a helper inside `formatter.py`, an internal,
  low-consequence structural change.
- **Expected Behavior**: no safety flags fire; `risk_tier == "low"` even
  though the operation touches a module — because `extract` is scored
  against hotspot status, not fan-in, and this module is neither a hotspot
  nor has any real callers.
- **Acceptance Criteria**: `flags == []`; `operation_type == "extract"`;
  target risk tier is `low`; the actual derivation explains this is
  genuinely low-impact, not merely unanalyzed (contrast with case-06, an
  unresolved target that also produces no flags for a different reason).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating every "extract" operation as
  automatically safe regardless of hotspot status, rather than checking the
  real structural data.
