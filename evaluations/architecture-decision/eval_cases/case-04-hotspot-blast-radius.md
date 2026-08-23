# Case 04 — hotspot-blast-radius

- **Input**: `fixtures/case-04-hotspot-blast-radius/decision.txt` (two
  well-specified options, one touching a real hotspot module) + a 2-module
  `ci_report.json` where `engine/auth.py` is flagged as a hotspot,
  fan_in=15.
- **Context**: refactor the session-token format vs. patch the legacy
  format's known vulnerability in place.
- **Expected Behavior**: no decision flags fire (text is well-specified);
  Option A's blast radius is HIGH (hotspot); Option B matches zero modules
  (its target isn't named) — a genuinely different, contrasting result per
  option, this is ADR-013's core scoring rule exercised for real.
- **Acceptance Criteria**: `option_impacts[0].blast_radius_tier == "high"`;
  `option_impacts[1].impacted_modules == []`; the actual derivation does not
  treat Option B's empty match as evidence it's safer.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: reading "zero matched modules" as "zero risk"
  instead of "ungrounded."
