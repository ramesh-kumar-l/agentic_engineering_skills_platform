# Case 02 — single-decision

- **Input**: `fixtures/case-02-single-decision/narrative.txt` — one
  "we decided" statement, no module named nearby.
- **Context**: tests the base decision-category match and the unresolved-
  location fail-closed default (MEDIUM, never LOW).
- **Expected Behavior**: one `decision-we-decided` candidate,
  `resolved_module_path == null`, `suggested_capture_priority == "MEDIUM"`.
- **Acceptance Criteria**: candidate present; priority is MEDIUM, not LOW,
  despite having no structural grounding.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating "no location found" as "not
  important" (silently downranking to LOW) instead of failing closed.
