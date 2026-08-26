# Case 07 — resolved-non-hotspot-module

- **Input**: `fixtures/case-07-resolved-non-hotspot-module/narrative.txt`
  — a lesson naming "stats.py"; the composed CI report resolves it with
  fan_in=1 and not a hotspot.
- **Context**: tests the MEDIUM band for a candidate that resolves
  successfully but isn't structurally significant — distinct code path
  from case-02/03/04's "never resolved at all" MEDIUM.
- **Expected Behavior**: one candidate, `resolved_module_path ==
  "engine/stats.py"`, `suggested_capture_priority == "MEDIUM"`.
- **Acceptance Criteria**: resolution succeeds (not null); priority stays
  MEDIUM, not HIGH (no hotspot/high fan-in) and not LOW (this scorer
  version never assigns LOW — see `priority_scorer.py`).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "resolved" with "important" —
  resolution and priority are separate signals.
