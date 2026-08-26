# Case 04 — poor-fit-no-good-template

- **Input**: `fixtures/case-04-poor-fit-no-good-template/task.txt` — a
  root-cause-investigation task that doesn't match any of the 3 registered
  templates. Run `understand-then-plan` with `--dry-run` anyway (the
  engine has no template-selection logic; it only executes the template
  it's given by name).
- **Context**: this is a judgment-layer case, not a deterministic one —
  the engine mechanically "succeeds" at compiling a plan for the wrong
  template; the value is entirely in the agent recognizing the fit is
  poor and saying so (Checklist item 1), not in the engine's output.
- **Expected Behavior**: engine output is identical in shape to case-01
  (both PENDING, zero compatibility issues) — the deterministic layer
  cannot distinguish a poor fit from a good one by itself.
- **Acceptance Criteria**: deterministic layer matches case-01's shape;
  judgment layer must classify this `poor-fit`, not `template-fit`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a workflow-composer that always reports
  success regardless of task fit, with no judgment layer catching it,
  would silently normalize forcing tasks into the wrong composition.
