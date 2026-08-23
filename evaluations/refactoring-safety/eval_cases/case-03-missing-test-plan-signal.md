# Case 03 — missing-test-plan-signal

- **Input**: `fixtures/case-03-missing-test-plan-signal/refactor.txt` (a
  rename with callers/rollback stated, but the word "test" never appears)
  + a synthetic `ci_report.json` where the target genuinely does have a
  real covering test module.
- **Context**: the text-level absence signal (`no-test-plan-signal`) and
  the structural test-coverage signal (`test_coverage_modules`) deliberately
  point in different directions — this case exists specifically to test
  that the checklist walk keeps them distinct rather than collapsing them.
- **Expected Behavior**: `no-test-plan-signal` and `no-verification-signal`
  fire (text-level absence); `untested-blast-radius` does NOT fire, because
  `tests/test_pricing.py` genuinely imports the target module.
- **Acceptance Criteria**: exactly 2 flags fire; the `pricing.py` target's
  `test_coverage_modules` is non-empty; the actual derivation explicitly
  states that the text's silence about tests does not mean the target is
  actually untested.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "the description didn't mention
  tests" with "this target has no test coverage" — these are different
  claims backed by different evidence sources in this engine.
