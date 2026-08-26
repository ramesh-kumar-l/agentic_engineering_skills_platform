# Case 03 — hotspot-uncovered-blocked-with-no-hygiene-flags

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags/diff.txt`
  (a comment-text-only edit to `engine/payment.py`) + a synthetic
  `ci_report.json` where `engine/payment.py` is a real hotspot (fan_in=6,
  two real callers) with NO covering test module anywhere in the report.
- **Context**: **Deliberate divergence case #2** — a completely clean diff
  (zero hygiene flags of any kind) on a structurally critical, genuinely
  untested module. This exercises ADR-016's rule that a hygiene-flag-free
  diff is NOT automatically release-ready — Axis 2 (structural) + Axis 3
  (coverage) alone can also force `blocked`.
- **Expected Behavior**: `flag_ids == []`; `readiness_tier == "blocked"`
  anyway, because `structural_tier == "high"` (hotspot, fan_in=6) and no
  test coverage exists; `overall_verdict == "NOT_READY"`.
- **Acceptance Criteria**: the actual derivation must explicitly connect the
  blocked tier to Axis 2/3, NOT mistakenly conclude "no hygiene flags means
  ready" — this is the exact failure mode this case is designed to catch.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an empty hygiene-flag list as proof of
  release-readiness; missing a real, uncovered hotspot because the diff
  itself looks trivial.
