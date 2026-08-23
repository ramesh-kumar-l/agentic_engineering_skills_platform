# Case 01 — stack-trace-clean

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-stack-trace-clean/symptom.txt` (a well-specified
  bug report with expected/actual, repro steps, and a Python traceback) + a
  synthetic `ci_report.json` with 3 modules (the target, its dependency, and
  a caller).
- **Context**: cart total is missing tax; a traceback names
  `engine/cart.py`, line 44, in `total`.
- **Expected Behavior**: the deterministic layer parses one stack frame and
  ranks `engine/cart.py` first with `evidence_tier=stack-trace`, well above
  the two keyword-only candidates; the agent grounds the candidate location
  in the stack-trace evidence (not just keyword overlap) and states a
  concrete confirmation step before proposing a fix.
- **Acceptance Criteria**: no symptom flags fire (report is well-specified);
  `candidates.candidates[0].path == "engine/cart.py"` with
  `evidence_tier == "stack-trace"`; the actual derivation includes an
  `evidence-tier` case and a `confirmation-step` case.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating a keyword-only match as equally
  confident as a stack-trace hit; proposing a fix without a stated
  confirmation step (jumping straight from candidate to fix).
