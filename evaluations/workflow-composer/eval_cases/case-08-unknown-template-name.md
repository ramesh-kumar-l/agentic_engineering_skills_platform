# Case 08 — unknown-template-name

- **Input**: `fixtures/case-08-unknown-template-name/task.txt` — CLI
  invoked with template name `not-a-real-template`.
- **Context**: the only case that exercises `engine/cli.py` directly
  rather than `executor.run_workflow` — the "unknown template" failure
  mode is a CLI-layer concern (the engine layer only ever receives an
  already-resolved `WorkflowTemplate`).
- **Expected Behavior**: CLI exits 1 with an actionable stderr message
  listing known template names.
- **Acceptance Criteria**: `cli_exit_code == 1`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: a silent no-op or an unhandled exception on
  an unrecognized template name would be a much worse failure mode than
  an explicit, actionable error.
