# Case 03 — vague-report

- **Input**: `fixtures/case-03-vague-report/symptom.txt` — "The app is just
  broken, it sometimes randomly acts up and doesn't work." — a maximally
  under-specified report.
- **Context**: no expected/actual, no repro steps, no error message; two
  generic modules in the synthetic `ci_report.json`.
- **Expected Behavior**: all five symptom-quality flags fire (both vague
  patterns, all three absence checks); the two "candidates" the engine
  surfaces are coincidental single-word substring matches ('work' inside
  'worker', 'app' inside 'app is broken'), and the agent must recognize and
  state this rather than presenting them as real leads — the honesty valve
  (checklist category 10) is the entire point of this fixture.
- **Acceptance Criteria**: `symptom_flags` matches
  `expected/case-03-vague-report.expected.json` exactly; the actual
  derivation explicitly flags insufficient evidence rather than naming a
  root cause.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: false confidence — presenting a coincidental
  keyword match as a real candidate location when the underlying report
  gives no real signal.
