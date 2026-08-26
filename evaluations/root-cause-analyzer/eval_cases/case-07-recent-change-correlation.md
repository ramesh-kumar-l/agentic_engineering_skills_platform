# Case 07 — recent-change-correlation

- **Input**: `fixtures/case-07-recent-change-correlation/symptom.txt` — a
  webhook 500 error that started right after a deploy, with release notes
  naming a specific changed function.
- **Expected Behavior**: the deterministic layer surfaces
  `engine/webhook_handler.py` as the top keyword candidate; the agent's
  Step 3 must separately surface the recent-change correlation (checklist
  category 6) as its own explicit finding, not bury it inside the
  candidate-location reasoning, and propose a cheap before/after diff as
  the confirmation step rather than a broad investigation.
- **Acceptance Criteria**: top candidate is `engine/webhook_handler.py`;
  actual derivation includes a dedicated `recent-change` case quoting the
  deploy/release-notes correlation.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: missing an explicit, stated recent-change
  timeline that the symptom text already handed to the investigator for
  free.
