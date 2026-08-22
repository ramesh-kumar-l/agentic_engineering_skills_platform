# Case 06 — no-relevant-modules-task

- **Input**: `fixtures/case-06-no-relevant-modules-task/task.txt` + a
  synthetic `ci_report.json` whose 3 modules share zero vocabulary with the
  task.
- **Context**: "Integrate with the new third-party SMS gateway..." — tests
  the honesty-valve path when composition with codebase-intelligence
  genuinely finds nothing relevant, rather than a case where the scorer
  should have found something and didn't.
- **Expected Behavior**: `relevance.scores` is empty; `report.warnings`
  states no modules matched; the agent must not force-fit an unrelated
  module into "affected files" — it must flag this as an assumption (new
  functionality) and separately note the third-party-provider dependency
  blocker.
- **Acceptance Criteria**: matches
  `expected/case-06-no-relevant-modules-task.expected.json`; no
  `affected-files` case names an existing module from the fixture.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: picking the least-irrelevant existing module
  just to have something to put in "affected files" (false grounding).
