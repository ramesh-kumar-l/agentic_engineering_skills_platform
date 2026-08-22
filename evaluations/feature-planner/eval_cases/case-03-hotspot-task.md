# Case 03 — hotspot-task

- **Input**: `fixtures/case-03-hotspot-task/task.txt` + a synthetic
  `ci_report.json` where `engine/config_loader.py` is marked a dependency-
  graph hotspot with `fan_in=12`.
- **Context**: "Update the shared config loader..." — tests whether the
  agent's risk assessment actually uses the blast-radius signal the
  relevance scorer computes, not just the keyword match.
- **Expected Behavior**: relevance scorer surfaces `config_loader.py`
  (score 10, `is_hotspot=true`, `fan_in=12`) plus two lower-scored
  dependents; the agent's `risk-blast-radius` case must cite the hotspot/
  fan_in signal specifically, and the plan should include a rollback
  strategy given the elevated risk.
- **Acceptance Criteria**: matches
  `expected/case-03-hotspot-task.expected.json`; `risk-blast-radius` case
  references the hotspot/fan_in evidence, not just "this seems risky."
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: flagging risk generically without grounding it
  in the actual dependency-graph data available from composition.
