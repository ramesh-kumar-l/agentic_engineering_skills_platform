# Case 02 — vague-quick-rename

- **Input**: `fixtures/case-02-vague-quick-rename/refactor.txt` (vague
  confidence language, no callers/tests/rollback/verification stated) + a
  synthetic `ci_report.json` where the target is a real hotspot with 3 real
  callers.
- **Context**: renaming `auth.py`, a high-fan-in hotspot module, described
  as "trivial."
- **Expected Behavior**: `vague-refactor-language` fires plus all four
  absence flags (no stated test plan, rollback, caller-update, or
  verification step); the target resolves to a HIGH-risk hotspot with 7
  real callers and zero test coverage, so `untested-blast-radius` also
  fires at high severity.
- **Acceptance Criteria**: 6 flags fire exactly as listed in
  `expected/case-02-vague-quick-rename.expected.json`; `risk_tier == "high"`
  for the `auth.py` target; the actual derivation explicitly calls out that
  the "trivial" framing is unsubstantiated given zero stated evidence.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: accepting "trivial"/"shouldn't break anything"
  at face value instead of treating it as an unsubstantiated assumption;
  under-weighting a HIGH-risk, zero-coverage target because the text sounds
  confident.
