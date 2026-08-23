# Case 06 — unresolved-target

- **Input**: `fixtures/case-06-unresolved-target/refactor.txt` (a rename
  naming a module that doesn't exist anywhere in the report on either side)
  + a synthetic `ci_report.json` with one unrelated real module.
- **Context**: contrasts directly with case-01, where one side of a rename
  (the new name) is legitimately expected to be unresolved. Here, BOTH
  sides fail to resolve — a materially different, more suspicious signal.
- **Expected Behavior**: `no-verification-signal` fires (text never states
  how success is confirmed); both targets have `resolved_module_path ==
  None`; the report's warnings explicitly state blast radius could not be
  derived from real data.
- **Acceptance Criteria**: the actual derivation must explicitly flag that
  this refactor names nothing recognizable in the target repository, and
  must not silently treat the resulting "no blast-radius flags fired"
  outcome as evidence the refactor is safe.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: conflating "the engine found nothing risky"
  with "the engine found nothing to analyze" — these require materially
  different responses in the checklist walk.
