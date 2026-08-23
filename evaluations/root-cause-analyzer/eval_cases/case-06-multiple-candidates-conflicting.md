# Case 06 — multiple-candidates-conflicting

- **Input**: `fixtures/case-06-multiple-candidates-conflicting/symptom.txt`
  (blank name field on export, no stack trace) + a synthetic `ci_report.json`
  with three modules that all share the word "report" but only two are
  plausibly related to the actual symptom.
- **Expected Behavior**: `engine/report_scheduler.py` scores nonzero (shared
  vocabulary) but is not actually involved; the agent must explicitly rule
  it out (checklist category 7) rather than listing all three candidates as
  equally likely, and must state that it cannot narrow between the two
  real candidates without more evidence (category 10).
- **Acceptance Criteria**: three candidates surfaced by the engine; actual
  derivation includes a `ruled-out` case naming `report_scheduler.py`
  specifically and an `assumption-flag` case stating the report can't be
  narrowed further without more evidence.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating every keyword-scoring module as an
  equally-weighted candidate instead of applying judgment to rule out the
  ones that don't actually fit the symptom's mechanism.
