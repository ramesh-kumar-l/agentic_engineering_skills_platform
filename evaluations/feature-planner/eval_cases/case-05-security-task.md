# Case 05 — security-task

- **Input**: `fixtures/case-05-security-task/task.txt` + a synthetic
  `ci_report.json` with an auth module and a user-facing API module.
- **Context**: an admin-restricted password-reset endpoint — tests whether
  the agent surfaces a `security-touchpoint` case grounded in the real
  auth module the relevance scorer found, rather than a generic "add auth
  check" note.
- **Expected Behavior**: zero deterministic flags (scope and verification
  are both stated); relevance scorer surfaces both `user_api.py` and
  `auth.py`; the agent's `security-touchpoint` case must name the actual
  auth mechanism (`require_role`/`AuthMiddleware`), not an invented one.
- **Acceptance Criteria**: matches
  `expected/case-05-security-task.expected.json`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: describing a security touchpoint in the
  abstract without grounding it in the repo's actual auth module.
