# Case 08 — zero-modules-ambiguous

- **Input**: `fixtures/case-08-zero-modules-ambiguous/narrative.txt` — a
  decision statement, composed against a CI report with `"modules": []`.
- **Context**: tests the explicit-warning fail-closed path, distinct from
  case-02's "narrative just doesn't mention a module" natural case — here
  the CI report itself signals it has nothing to resolve against.
- **Expected Behavior**: one candidate, unresolved,
  `suggested_capture_priority == "MEDIUM"`; `report.warnings` names the
  zero-modules condition explicitly.
- **Acceptance Criteria**: warning present; priority fails closed to
  MEDIUM, never silently LOW.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an ambiguous/degenerate CI report as
  equivalent to "confirmed no structural significance" (which would argue
  for LOW) rather than "unknown" (which argues for MEDIUM).
