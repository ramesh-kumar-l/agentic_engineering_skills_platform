# Case 06 — large-noisy-diff

- **Input**: `fixtures/case-06-large-noisy-diff/change.diff`.
- **Context**: A cosmetic variable rename (`qty` -> `quantity`) touches every
  line of a small file; one line also silently changes a threshold comparison
  from `<=` to `<`.
- **Expected Behavior**: The agent does not treat the diff as "just a rename"
  and catches the boundary-condition regression hidden inside the noise.
- **Acceptance Criteria**: A reported defect with `category == "subtle-bug"`,
  `file == "inventory.py"`, mentioning the threshold/boundary change.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is the direct test of the "large noisy diff"
  failure-first category from `05-evaluation-framework.md` — a miss here
  means volume alone can hide a real defect from this skill.
