# Case 05 — stack-trace-outside-repo

- **Input**: `fixtures/case-05-stack-trace-outside-repo/symptom.txt` — a
  traceback whose only frame is inside a third-party library
  (`somelib/pool.py` under `site-packages`), not this repo.
- **Expected Behavior**: `stack_trace_parser` still parses the frame (it's
  a real stack-trace shape), but `candidate_scorer` finds no module match
  for it, and `report.py` emits the "none of their paths matched" warning.
  The agent must not silently drop the stack-trace evidence — it should
  explicitly state that the trace points outside the repo's own code and
  fall back to keyword-grounded candidates, flagging the gap as an
  assumption rather than pretending the trace was actionable.
- **Acceptance Criteria**: `report.warnings` contains the outside-repo
  warning; top candidate is `engine/export.py` at `evidence_tier=keyword`
  (not stack-trace, since nothing matched); actual derivation includes an
  `assumption-flag` case naming the third-party mismatch explicitly.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an unmatched stack frame as if it were
  still a stack-trace-tier candidate; giving up entirely instead of falling
  back to the next-best evidence (keyword overlap).
