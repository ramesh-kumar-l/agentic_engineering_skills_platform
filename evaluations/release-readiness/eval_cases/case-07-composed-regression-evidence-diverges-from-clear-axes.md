# Case 07 — composed-regression-evidence-diverges-from-clear-axes

- **Input**: a small, low-fan-in, genuinely test-covered, hygiene-flag-free
  change to `engine/pricing.py` + a synthetic `regression_report.json` (a
  stand-in for a real `regression-hunter` `report.json`) showing
  `overall_risk_tier: "high"` for that same file, due to a real diff-pattern
  flag (`modified-signature-no-test-change`).
- **Context**: **Deliberate divergence case #3 (this phase's second
  official divergence fixture, per the roadmap's requirement of at least
  2)** — Axes 1-3 (always available) say `clear`/`READY`; the OPTIONAL,
  composed Axis 4 (regression evidence, surfaced from a different skill's
  real analysis) says `high`. ADR-016 deliberately does NOT blend Axis 4
  into `readiness_tier` — this case exists to prove that design choice is
  visible and correct, not silently lost.
- **Expected Behavior**: `readiness_tier == "clear"`, `overall_verdict ==
  "READY"` (from Axes 1-3 alone); `regression_evidence.available == true`
  and `overall_risk_tier == "high"` (surfaced, not blended).
- **Acceptance Criteria**: the actual derivation must explicitly flag that
  `READY` here does NOT mean "no regression risk" — a human must weigh the
  composed regression-hunter finding separately, exactly the honesty-valve
  behavior category 9/10 of the checklist requires.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: silently treating `READY` as proof no other
  evidence exists; failing to surface a real, composed high-risk finding.
