# Case 01 — rename-clean-covered

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-rename-clean-covered/refactor.txt` (a rename
  with callers, tests, and a rollback path all stated) + a synthetic
  `ci_report.json` with 3 modules including a real covering test module.
- **Context**: renaming `cache.py` to `cache_layer.py`, a low-fan-in,
  non-hotspot module.
- **Expected Behavior**: no safety flags fire (the text is well-specified);
  the rename-source target resolves to `engine/cache.py` at medium risk
  (fan_in=1, boundary-changing operation); the rename-destination target
  (`cache_layer.py`) correctly fails to resolve — expected for a rename, not
  a red flag; the target is genuinely covered by a real test module, so no
  `untested-blast-radius` flag fires.
- **Acceptance Criteria**: `flags == []`; `operation_type == "rename"`;
  `cache.py`'s target resolves with `risk_tier == "medium"` and non-empty
  `test_coverage_modules`; the actual derivation explicitly distinguishes
  "the destination doesn't exist yet because it's a rename target" from "an
  unresolved target is suspicious" rather than flagging both the same way.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating the rename-destination's unresolved
  status as equivalent to a genuinely fabricated/typo'd target; missing the
  real test coverage already present for the rename-source module.
