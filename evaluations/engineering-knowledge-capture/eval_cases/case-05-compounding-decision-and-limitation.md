# Case 05 — compounding-decision-and-limitation

- **Input**: `fixtures/case-05-compounding-decision-and-limitation/narrative.txt`
  — a decision paragraph followed by a "known limitation" paragraph
  describing the decision's direct consequence.
- **Context**: tests that two independent candidate categories in one
  narrative compose into two distinct candidates, not one collapsed note —
  mirrors dependency-supply-chain's compounding-case fixture.
- **Expected Behavior**: two candidates (`decision-we-decided`,
  `limitation-known-limitation`), both unresolved, both MEDIUM.
- **Acceptance Criteria**: both candidates surfaced explicitly and kept
  separate in the derivation.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently merging the decision and its
  consequence into a single vague "issues found" note.
