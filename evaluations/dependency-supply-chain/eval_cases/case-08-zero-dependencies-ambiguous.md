# Case 08 — zero-dependencies-ambiguous

- **Input**: `fixtures/case-08-zero-dependencies-ambiguous/ci_report.json`
  — `external_dependencies: []`.
- **Context**: the fail-closed case. A genuinely dependency-free repo and a
  repo whose manifests live somewhere `codebase-intelligence`'s
  `external_deps.py` doesn't look (non-root-level, or an unsupported format
  like Pipfile) produce the exact same zero-dependency report — the engine
  cannot distinguish them, so it must not report `CLEAR` in either case.
- **Expected Behavior**: `report.warnings` is non-empty (the explicit
  zero-dependency caveat); `suggested_risk_level == "REQUIRES_REVIEW"`
  even though zero flags fired — the fail-closed rule (`risk_scorer.py`)
  treats zero dependencies as ambiguous evidence, not as proof of a clean
  supply chain.
- **Acceptance Criteria**: the derivation explicitly names the warning and
  explains WHY zero dependencies triggers review instead of celebrating a
  clean scan; never silently reports `CLEAR`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: the fail-open trap — mistaking "the engine
  found nothing" for "the engine confirmed there is nothing," the exact
  distinction ADR-011's fail-closed discipline exists to prevent.
