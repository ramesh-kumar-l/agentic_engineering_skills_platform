# Case 07 — numbered-list-options

- **Input**: `fixtures/case-07-numbered-list-options/decision.txt` (a
  3-item numbered list, well-specified) + a 2-module `ci_report.json` where
  `engine/notifications.py` is a hotspot, fan_in=11.
- **Context**: webhooks vs. faster polling vs. status quo for a
  notification service.
- **Expected Behavior**: no decision flags fire; the numbered-list parser
  produces 3 options (not 2); all three touch the hotspot module, including
  the two "do nothing structural" options; Item 1 (webhooks) proposes code
  that doesn't exist yet in the report, so its true blast radius is
  ungrounded.
- **Acceptance Criteria**: `option_count == 3`; all three
  `option_impacts[*].blast_radius_tier == "high"`; the actual derivation
  states Item 1's new-code blast radius as an explicit gap.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: the list-item parser collapsing 3 items into 2
  (an off-by-one on the numbered-list regex); missing that "no-op" options
  still carry real hotspot risk.
