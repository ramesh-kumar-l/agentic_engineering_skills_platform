# Case 01 — all-pinned-clean

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-all-pinned-clean/ci_report.json` — 2
  dependencies (`alpha==1.0.0`, `beta==2.1.0`), both exact-pinned, from a
  single manifest.
- **Context**: the simplest clean case — no unpinned versions, no
  known-risk names, no duplicates.
- **Expected Behavior**: zero flags fire; `suggested_risk_level == "CLEAR"`.
- **Acceptance Criteria**: `flag_ids == []`; `suggested_risk_level == "CLEAR"`;
  the actual derivation explicitly notes the pinned status as positive
  evidence, not silence.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an empty flag list as unexamined
  rather than as a genuine "checked, found nothing" result.
