# Case 05 — low-blast-radius-leaf

- **Input**: `fixtures/case-05-low-blast-radius-leaf/decision.txt` (two
  well-specified options touching a leaf module with zero dependents) + a
  1-module `ci_report.json` with empty fan_in/fan_out/hotspots.
- **Context**: add a debug-logging flag vs. document an existing env var.
- **Expected Behavior**: no decision flags fire; Option A's blast radius is
  low (a real but weak, low-stakes match); Option B matches zero modules
  because it's documentation-only, not because the scorer missed something.
- **Acceptance Criteria**: `option_impacts[0].blast_radius_tier == "low"`;
  `option_impacts[1].impacted_modules == []`; the actual derivation
  distinguishes "genuinely low-risk" (this case) from "ungrounded" (case-04's
  Option B) rather than treating both the same way.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating a low blast-radius score with an
  ungrounded one.
