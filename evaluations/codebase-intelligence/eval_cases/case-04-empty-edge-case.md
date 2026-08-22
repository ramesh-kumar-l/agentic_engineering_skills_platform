# Case 04 — empty-edge-case

- **Input**: `fixtures/empty-edge-case/` (a single plain-text file, no source code
  of any recognized language).
- **Context**: Deliberately constructed failure/edge case per the failure-first
  checklist in `project-memory-bank/05-evaluation-framework.md` (category:
  "missing context" / degenerate input).
- **Expected Behavior**: Engine does not crash or raise; it returns a report with
  an empty module list, empty dependency graph, and empty entry-point list —
  gracefully reflecting "nothing recognizable here" rather than erroring.
- **Acceptance Criteria**: `file_count == 1` (the text file is still inventoried);
  `entry_point_paths == []`; `internal_edges == []`; `external_dependency_names == []`;
  no exception raised during the run.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: unhandled exception on repos with no code; empty
  dependency graph construction (Counter/most_common on empty input).
