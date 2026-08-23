# Regression Hunter Pre-Decision Report

## Stats
- Files changed: 2 (added: 0, deleted: 0)
- Lines added: 15, lines removed: 1
- Diff-pattern flags: 0
- Files at HIGH overall risk: 0

## Per-File Risk Assessment (three separate signals, not blended — see ADR-015)
### `skills/codebase-intelligence/engine/scanner.py` (modified) — overall risk: **LOW**
- Lines: +4 / -1
- **Axis 1 — Diff-pattern flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/codebase-intelligence/engine/scanner.py, fan_in=1, fan_out=1
  - caller: `skills/acceptance-test-engineer/engine/report.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/tests/test_stats.py` (fan_in=0)
  - caller: `skills/acceptance-test-engineer/tests/test_testability_scanner.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/engine/report.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/tests/test_risk_scanner.py` (fan_in=0)
  - caller: `skills/architecture-decision/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/architecture-decision/tests/test_decision_scanner.py` (fan_in=0)
  - caller: `skills/codebase-intelligence/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/feature-planner/engine/report.py` (fan_in=1)
  - caller: `skills/feature-planner/tests/test_planning_scanner.py` (fan_in=0)
  - ... and 12 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_stats.py, skills/acceptance-test-engineer/tests/test_testability_scanner.py, skills/adversarial-diff-reviewer/tests/test_risk_scanner.py, skills/architecture-decision/tests/test_decision_scanner.py, skills/feature-planner/tests/test_planning_scanner.py, skills/feature-planner/tests/test_stats.py, skills/refactoring-safety/tests/test_safety_scanner.py, skills/refactoring-safety/tests/test_test_coverage_scanner.py, skills/regression-hunter/tests/test_regression_scanner.py, skills/regression-hunter/tests/test_test_coverage_scanner.py, skills/root-cause-analyzer/tests/test_stats.py, skills/root-cause-analyzer/tests/test_symptom_scanner.py, skills/security-context-guard/tests/test_scanner.py

### `skills/codebase-intelligence/tests/test_scanner.py` (modified) — overall risk: **LOW**
- Lines: +11 / -0
- **Axis 1 — Diff-pattern flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/codebase-intelligence/tests/test_scanner.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
