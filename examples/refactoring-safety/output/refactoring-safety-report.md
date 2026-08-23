# Refactoring Safety Pre-Decision Report

## Refactor Description
Extract the path-stem helper duplicated across `target_resolver.py` and
`test_coverage_scanner.py` in the refactoring-safety engine into a shared
module, and update both call sites to import it instead of repeating the
`PurePosixPath(path).stem` logic inline.

**Detected operation type:** `extract`

## Stats
- Words: 38
- Targets parsed: 2 (resolved: 2)
- Flags: 3 (high severity: 2)

## Safety Flags (mechanically-detected leads, not verdicts)
- [high] `no-test-plan-signal` — Refactor text never mentions tests or coverage — the checklist's verification category will have to be stated as an assumption rather than derived from the plan itself.
- [high] `no-rollback-signal` — Refactor text never addresses how to back out if something breaks — a refactor with no stated rollback path is riskier than one that states it has none, because the absence hasn't been considered.
- [medium] `no-verification-signal` — Refactor text never states how success will be verified after the change lands — a refactor plan with no verification step described is one where 'done' is undefined.

## Target Assessment (codebase-intelligence-grounded blast radius + test coverage, not just a name match)
### `target_resolver.py` -> `skills/refactoring-safety/engine/target_resolver.py` (risk: low, fan_in=1, fan_out=1, test coverage: yes)
- caller: `skills/refactoring-safety/engine/report.py` (fan_in=1, fan_out=8 [hotspot])
- caller: `skills/refactoring-safety/tests/test_target_resolver.py` (fan_in=0, fan_out=0)
- Covered by: skills/refactoring-safety/tests/test_target_resolver.py

### `test_coverage_scanner.py` -> `skills/refactoring-safety/engine/test_coverage_scanner.py` (risk: low, fan_in=1, fan_out=1, test coverage: yes)
- caller: `skills/refactoring-safety/engine/report.py` (fan_in=1, fan_out=8 [hotspot])
- caller: `skills/refactoring-safety/tests/test_test_coverage_scanner.py` (fan_in=0, fan_out=0)
- Covered by: skills/refactoring-safety/tests/test_test_coverage_scanner.py
