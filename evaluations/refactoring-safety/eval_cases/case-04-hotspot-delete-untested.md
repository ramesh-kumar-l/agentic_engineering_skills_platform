# Case 04 — hotspot-delete-untested

- **Input**: `fixtures/case-04-hotspot-delete-untested/refactor.txt` (a
  delete with callers/rollback/verification stated, but no tests) + a
  synthetic `ci_report.json` where the target is a real hotspot with no
  covering test module.
- **Context**: deleting `legacy_router.py`, a hotspot with 2 real callers
  and no test coverage at all.
- **Expected Behavior**: `no-test-plan-signal` fires (text never says
  "test"); `untested-blast-radius` fires at high severity (real hotspot,
  zero coverage); `no-rollback-signal`, `no-caller-update-signal`, and
  `no-verification-signal` do NOT fire, since the text states all three.
- **Acceptance Criteria**: exactly 2 flags fire; `risk_tier == "high"`;
  `test_coverage_modules == []`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating "verify via CI" and "reversible via
  git revert" as if they substitute for actual test coverage of the deleted
  module itself.
