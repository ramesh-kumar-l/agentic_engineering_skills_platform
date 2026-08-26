# Case 06 — large-surface-area

- **Input**: `fixtures/case-06-large-surface-area/ci_report.json` — 10
  dependencies, 6 pinned and 4 range-unpinned, all in one manifest.
- **Context**: tests the surface-area stats (`total_dependencies`,
  `unpinned_count`, `unpinned_percentage`) as a distinct checklist item from
  individual per-dependency flags — the engine produces four separate
  `unpinned-range` flags (one per unpinned dependency), and the surface-area
  block summarizes the aggregate picture (40% unpinned) that no single flag
  states on its own.
- **Expected Behavior**: four `unpinned-range` flags;
  `surface_area.unpinned_percentage == 40.0`;
  `suggested_risk_level == "NEEDS_REVIEW"`.
- **Acceptance Criteria**: the derivation explicitly cites the aggregate
  40%/10-dependency figure, not just the individual flags — this is what
  distinguishes checklist item 6 (surface area) from item 2 (pin status).
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating four repeated low-severity flags as
  four independent low-priority issues instead of noticing they compose
  into a real aggregate signal (nearly half of direct dependencies are
  unpinned).
