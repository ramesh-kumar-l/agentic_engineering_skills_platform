# Case 02 — keyword-only-no-trace

- **Input**: `fixtures/case-02-keyword-only-no-trace/symptom.txt` (well-specified,
  no stack trace) + a synthetic `ci_report.json` with 3 modules.
- **Context**: search results come back unordered; no error/exception, so
  there is no traceback to parse.
- **Expected Behavior**: candidates are keyword-tier only (no stack-trace
  evidence exists to find); the agent explicitly flags that these are
  keyword-overlap leads, not confirmed locations, and states a concrete
  confirmation step to disambiguate between the two plausible modules.
- **Acceptance Criteria**: `candidates.stack_frames == []`;
  `engine/search.py` ranks first; the actual derivation includes an
  `assumption-flag` case stating the reduced confidence explicitly.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: presenting a keyword-only match with the same
  confidence language as a stack-trace-confirmed one.
