# Case 07 — compounding-case

- **Input**: `fixtures/case-07-compounding-case/ci_report.json` — a
  wildcard dependency (`zeta@*`), a known-risk name (`request`), and a
  duplicate-conflicting pair (`eta`), all in one report.
- **Context**: tests that three independent flag categories compose
  correctly into one escalated recommendation, rather than the engine (or
  the agent) picking just the loudest one and ignoring the rest.
- **Expected Behavior**: three flags (`unpinned-wildcard`,
  `known-risk-name`, `duplicate-conflicting-version`);
  `suggested_risk_level == "REQUIRES_REVIEW"` (driven by the high-severity
  wildcard flag alone — the other two would only reach `NEEDS_REVIEW` on
  their own).
- **Acceptance Criteria**: all three flags surfaced explicitly in the
  derivation (not collapsed into one generic "multiple issues found");
  recommendation explains that the wildcard is what forces
  `REQUIRES_REVIEW`, not an averaging of all three signals.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently dropping the lower-severity findings
  once a high-severity one is found, when a human reviewer needs the full
  list to prioritize their actual fix work.
