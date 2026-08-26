# Case 05 — duplicate-conflicting-versions

- **Input**: `fixtures/case-05-duplicate-conflicting-versions/ci_report.json`
  — `epsilon` declared as `==1.0.0` in `requirements.txt` and `==2.0.0` in
  `pyproject.toml`; both individually pinned, but they disagree.
- **Context**: tests the duplicate-detector independent of pin status — a
  case where every individual declaration is "pinned" but the two manifests
  still contradict each other (a real install will pick whichever manifest
  the tool used runs last, non-deterministically from the user's view).
- **Expected Behavior**: one `duplicate-conflicting-version` flag (medium
  severity); **no** `unpinned-*` flag (both declarations are individually
  pinned); `suggested_risk_level == "NEEDS_REVIEW"`.
- **Acceptance Criteria**: flag present; no false unpinned flag; derivation
  identifies which two manifests disagree and on what versions.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "pinned" (each declaration is exact)
  with "consistent" (the declarations agree with each other) — these are
  orthogonal checks in this engine, by design.
