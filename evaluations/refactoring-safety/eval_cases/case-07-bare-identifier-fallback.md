# Case 07 — bare-identifier-fallback

- **Input**: `fixtures/case-07-bare-identifier-fallback/refactor.txt` (a
  move operation naming its targets as bare identifiers, no backticks or
  quotes) + a synthetic `ci_report.json` with one real caller and one real
  test.
- **Context**: exercises the parser's bare-identifier fallback path (no
  explicit `` `foo.py` `` markers present anywhere in the text).
- **Expected Behavior**: `operation_type == "move"`; two targets parsed
  (`build_report`, `report_builder.py`), both resolving to the same module;
  no safety flags fire (text is fully specified).
- **Acceptance Criteria**: `flags == []`; both targets resolve to
  `engine/report_builder.py`; `risk_tier == "medium"` (one real caller, not
  a hotspot).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: the bare-identifier fallback extracting
  ordinary sentence words ("move", "new", "dedicated") as if they were real
  targets.
