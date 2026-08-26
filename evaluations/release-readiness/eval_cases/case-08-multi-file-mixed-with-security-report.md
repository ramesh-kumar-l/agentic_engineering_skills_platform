# Case 08 — multi-file-mixed-with-security-report

- **Input**: a 3-file diff (`engine/core.py` gets a debug print leftover,
  `engine/util2.py` is a clean type-annotation edit with real coverage,
  `engine/helper.py` has real fan_in=1 but no coverage) + a synthetic
  `security_report.json` (a stand-in for a real `security-context-guard`
  `report.json`) with `suggested_verdict: "REQUIRES_HUMAN_APPROVAL"`.
- **Context**: exercises per-file tier divergence within ONE diff (three
  files land on three different tiers) plus the OPTIONAL, report-level
  security evidence composition path.
- **Expected Behavior**: `engine/core.py` -> `blocked`; `engine/util2.py`
  -> `clear`; `engine/helper.py` -> `needs-review`; `overall_verdict ==
  "NOT_READY"` (one blocked file is sufficient); `security_evidence`
  surfaced with `suggested_verdict == "REQUIRES_HUMAN_APPROVAL"`, and a
  warning naming it explicitly.
- **Acceptance Criteria**: the actual derivation must name all three files'
  distinct tiers explicitly, not report one aggregate judgment for the
  whole diff, and must surface the security evidence as composed, not
  re-derived.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: collapsing three different per-file outcomes
  into one summary that loses the distinction; missing the optional
  security evidence because it doesn't affect the deterministic tier.
