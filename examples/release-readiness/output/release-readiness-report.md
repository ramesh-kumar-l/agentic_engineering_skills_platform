# Release Readiness Scorecard

## Overall Verdict: **NOT_READY**
_This is a recommendation for a human to review, not an autonomous release gate — see SKILL.md's Security Constraints._

## Stats
- Files changed: 78 (added: 76, deleted: 0)
- Lines added: 3956, lines removed: 0
- Diff-hygiene flags: 9
- Files BLOCKED: 3
- Files NEEDS-REVIEW: 75
- Regression report composed: False (optional — see ADR-011 precedent)
- Security report composed: False (optional)

## Per-File Readiness Assessment (axes kept separate, never blended — see ADR-016)
### `evaluations/release-readiness/run_evaluation.py` (new) — readiness: **BLOCKED**
- Lines: +260 / -0
- **Axis 1 — Diff-hygiene flags** (1):
  - [medium] `debug-print-leftover` (line 254) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
- **Axis 2 — Structural blast radius**: tier=low, resolved=evaluations/release-readiness/run_evaluation.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/cli.py` (new) — readiness: **BLOCKED**
- Lines: +99 / -0
- **Axis 1 — Diff-hygiene flags** (4):
  - [medium] `debug-print-leftover` (line 64) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
  - [medium] `debug-print-leftover` (line 77) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
  - [medium] `debug-print-leftover` (line 90) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
  - [medium] `debug-print-leftover` (line 93) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/engine/cli.py, fan_in=0, fan_out=4
  - caller: `skills/acceptance-test-engineer/tests/test_cli.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/tests/test_cli.py` (fan_in=0)
  - caller: `skills/security-context-guard/tests/test_cli.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_cli.py, skills/adversarial-diff-reviewer/tests/test_cli.py, skills/security-context-guard/tests/test_cli.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_hygiene_scanner.py` (new) — readiness: **BLOCKED**
- Lines: +116 / -0
- **Axis 1 — Diff-hygiene flags** (4):
  - [medium] `debug-print-leftover` (line 29) — Debug statement (print/console.log/pdb/debugger/breakpoint) left in added code — likely leftover from local debugging, not intended for a released version.
  - [low] `todo-blocking-marker` (line 55) — TODO/FIXME/XXX marker left in added code — may indicate intentionally incomplete work not yet ready to ship.
  - [high] `hardcoded-secret-shaped` (line 68) — Line looks like a hardcoded secret/credential literal — an independent copy of security-context-guard's generic-credential-assignment pattern, in miniature; a lead, not proof of a real leak.
  - [low] `todo-blocking-marker` (line 112) — TODO/FIXME/XXX marker left in added code — may indicate intentionally incomplete work not yet ready to ship.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_hygiene_scanner.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/RESULTS.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +137 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-01-clean-low-risk-covered.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-02-debug-print-blocked-despite-covered-low-risk.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +36 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-04-hotspot-covered-needs-review.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-05-medium-structural-uncovered-needs-review.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-06-merge-conflict-marker-blocked.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +20 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-07-composed-regression-evidence-diverges-from-clear-axes.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/actual/case-08-multi-file-mixed-with-security-report.actual.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +36 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-01-clean-low-risk-covered.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +23 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-02-debug-print-blocked-despite-covered-low-risk.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +21 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +23 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-04-hotspot-covered-needs-review.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +16 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-05-medium-structural-uncovered-needs-review.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +15 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-06-merge-conflict-marker-blocked.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +16 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-07-composed-regression-evidence-diverges-from-clear-axes.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +24 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/eval_cases/case-08-multi-file-mixed-with-security-report.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +23 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-01-clean-low-risk-covered.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +10 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-02-debug-print-blocked-despite-covered-low-risk.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +10 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +11 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-04-hotspot-covered-needs-review.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +10 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-05-medium-structural-uncovered-needs-review.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +10 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-06-merge-conflict-marker-blocked.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +9 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-07-composed-regression-evidence-diverges-from-clear-axes.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +10 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/expected/case-08-multi-file-mixed-with-security-report.expected.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +15 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-01-clean-low-risk-covered/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +24 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-01-clean-low-risk-covered/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +7 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-02-debug-print-blocked-despite-covered-low-risk/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +24 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-02-debug-print-blocked-despite-covered-low-risk/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +7 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +31 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-03-hotspot-uncovered-blocked-with-no-hygiene-flags/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +8 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-04-hotspot-covered-needs-review/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +31 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-04-hotspot-covered-needs-review/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +8 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-05-medium-structural-uncovered-needs-review/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +24 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-05-medium-structural-uncovered-needs-review/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +7 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-06-merge-conflict-marker-blocked/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +17 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-06-merge-conflict-marker-blocked/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +11 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-07-composed-regression-evidence-diverges-from-clear-axes/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +24 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-07-composed-regression-evidence-diverges-from-clear-axes/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +7 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-07-composed-regression-evidence-diverges-from-clear-axes/regression_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +19 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-08-multi-file-mixed-with-security-report/ci_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +45 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-08-multi-file-mixed-with-security-report/diff.txt` (new) — readiness: **NEEDS-REVIEW**
- Lines: +21 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `evaluations/release-readiness/fixtures/case-08-multi-file-mixed-with-security-report/security_report.json` (new) — readiness: **NEEDS-REVIEW**
- Lines: +8 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/README.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +75 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/SKILL.md` (new) — readiness: **NEEDS-REVIEW**
- Lines: +366 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `<unknown>` (modified) — readiness: **NEEDS-REVIEW**
- Lines: +0 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/blast_radius_scorer.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/blast_radius_scorer.py, fan_in=1, fan_out=1
  - caller: `skills/release-readiness/engine/readiness_scorer.py` (fan_in=1)
  - caller: `skills/release-readiness/tests/test_blast_radius_scorer.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/release-readiness/tests/test_blast_radius_scorer.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/ci_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +67 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/ci_report_loader.py, fan_in=2, fan_out=1
  - caller: `skills/architecture-decision/engine/cli.py` (fan_in=0)
  - caller: `skills/architecture-decision/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/architecture-decision/tests/test_ci_report_loader.py` (fan_in=0)
  - caller: `skills/feature-planner/engine/cli.py` (fan_in=0)
  - caller: `skills/feature-planner/engine/report.py` (fan_in=1)
  - caller: `skills/feature-planner/tests/test_ci_report_loader.py` (fan_in=0)
  - caller: `skills/refactoring-safety/engine/cli.py` (fan_in=0)
  - caller: `skills/refactoring-safety/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/refactoring-safety/tests/test_ci_report_loader.py` (fan_in=0)
  - caller: `skills/regression-hunter/engine/cli.py` (fan_in=0)
  - ... and 8 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/architecture-decision/tests/test_ci_report_loader.py, skills/feature-planner/tests/test_ci_report_loader.py, skills/refactoring-safety/tests/test_ci_report_loader.py, skills/regression-hunter/tests/test_ci_report_loader.py, skills/release-readiness/tests/test_ci_report_loader.py, skills/root-cause-analyzer/tests/test_ci_report_loader.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/diff_parser.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +130 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/diff_parser.py, fan_in=1, fan_out=1
  - caller: `skills/adversarial-diff-reviewer/engine/report.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/tests/test_diff_parser.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/tests/test_risk_scanner.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/tests/test_stats.py` (fan_in=0)
  - caller: `skills/regression-hunter/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/regression-hunter/tests/test_diff_parser.py` (fan_in=0)
  - caller: `skills/regression-hunter/tests/test_regression_scanner.py` (fan_in=0)
  - caller: `skills/regression-hunter/tests/test_stats.py` (fan_in=0)
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_diff_parser.py` (fan_in=0)
  - ... and 2 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/adversarial-diff-reviewer/tests/test_diff_parser.py, skills/adversarial-diff-reviewer/tests/test_risk_scanner.py, skills/adversarial-diff-reviewer/tests/test_stats.py, skills/regression-hunter/tests/test_diff_parser.py, skills/regression-hunter/tests/test_regression_scanner.py, skills/regression-hunter/tests/test_stats.py, skills/release-readiness/tests/test_diff_parser.py, skills/release-readiness/tests/test_hygiene_scanner.py, skills/release-readiness/tests/test_stats.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/hygiene_patterns.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +75 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/hygiene_patterns.py, fan_in=1, fan_out=0
  - caller: `skills/release-readiness/engine/hygiene_scanner.py` (fan_in=1)
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/hygiene_scanner.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +81 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/hygiene_scanner.py, fan_in=1, fan_out=2
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_hygiene_scanner.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/release-readiness/tests/test_hygiene_scanner.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/models.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +211 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=high, resolved=skills/release-readiness/engine/models.py, fan_in=13, fan_out=0 [hotspot]
  - caller: `skills/acceptance-test-engineer/engine/render_json.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/engine/render_markdown.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/engine/report.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/engine/requirement_parser.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/engine/stats.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/engine/testability_scanner.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/engine/diff_parser.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/engine/render_json.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/engine/render_markdown.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/engine/report.py` (fan_in=1)
  - ... and 91 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/architecture-decision/tests/test_impact_scorer.py, skills/architecture-decision/tests/test_stats.py, skills/codebase-intelligence/tests/test_graph.py, skills/feature-planner/tests/test_relevance_scorer.py, skills/refactoring-safety/engine/test_coverage_scanner.py, skills/refactoring-safety/tests/test_safety_scorer.py, skills/refactoring-safety/tests/test_stats.py, skills/refactoring-safety/tests/test_target_resolver.py, skills/refactoring-safety/tests/test_test_coverage_scanner.py, skills/regression-hunter/engine/test_coverage_scanner.py, skills/regression-hunter/tests/test_risk_scorer.py, skills/regression-hunter/tests/test_stats.py, skills/regression-hunter/tests/test_target_resolver.py, skills/regression-hunter/tests/test_test_coverage_scanner.py, skills/release-readiness/engine/test_coverage_scanner.py, skills/release-readiness/tests/test_blast_radius_scorer.py, skills/release-readiness/tests/test_readiness_scorer.py, skills/release-readiness/tests/test_stats.py, skills/release-readiness/tests/test_target_resolver.py, skills/release-readiness/tests/test_test_coverage_scanner.py, skills/root-cause-analyzer/tests/test_candidate_scorer.py, skills/security-context-guard/tests/test_classification.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/readiness_scorer.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +66 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/readiness_scorer.py, fan_in=1, fan_out=2
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_readiness_scorer.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/release-readiness/tests/test_readiness_scorer.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/regression_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +62 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/regression_report_loader.py, fan_in=1, fan_out=1
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_regression_report_loader.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/release-readiness/tests/test_regression_report_loader.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/render_json.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +12 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/render_json.py, fan_in=1, fan_out=1
  - caller: `skills/acceptance-test-engineer/engine/cli.py` (fan_in=0)
  - caller: `skills/acceptance-test-engineer/tests/test_integration.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/engine/cli.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/tests/test_integration.py` (fan_in=0)
  - caller: `skills/architecture-decision/engine/cli.py` (fan_in=0)
  - caller: `skills/architecture-decision/tests/test_integration.py` (fan_in=0)
  - caller: `skills/codebase-intelligence/engine/cli.py` (fan_in=0)
  - caller: `skills/codebase-intelligence/tests/test_integration.py` (fan_in=0)
  - caller: `skills/feature-planner/engine/cli.py` (fan_in=0)
  - caller: `skills/feature-planner/tests/test_integration.py` (fan_in=0)
  - ... and 13 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_integration.py, skills/adversarial-diff-reviewer/tests/test_integration.py, skills/architecture-decision/tests/test_integration.py, skills/codebase-intelligence/tests/test_integration.py, skills/feature-planner/tests/test_integration.py, skills/refactoring-safety/tests/test_integration.py, skills/refactoring-safety/tests/test_report.py, skills/regression-hunter/tests/test_integration.py, skills/regression-hunter/tests/test_report.py, skills/release-readiness/tests/test_integration.py, skills/release-readiness/tests/test_report.py, skills/root-cause-analyzer/tests/test_integration.py, skills/security-context-guard/tests/test_integration.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/render_markdown.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +115 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/render_markdown.py, fan_in=1, fan_out=1
  - caller: `skills/acceptance-test-engineer/engine/cli.py` (fan_in=0)
  - caller: `skills/acceptance-test-engineer/tests/test_integration.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/engine/cli.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/tests/test_integration.py` (fan_in=0)
  - caller: `skills/architecture-decision/engine/cli.py` (fan_in=0)
  - caller: `skills/architecture-decision/tests/test_integration.py` (fan_in=0)
  - caller: `skills/codebase-intelligence/engine/cli.py` (fan_in=0)
  - caller: `skills/codebase-intelligence/tests/test_integration.py` (fan_in=0)
  - caller: `skills/feature-planner/engine/cli.py` (fan_in=0)
  - caller: `skills/feature-planner/tests/test_integration.py` (fan_in=0)
  - ... and 10 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_integration.py, skills/adversarial-diff-reviewer/tests/test_integration.py, skills/architecture-decision/tests/test_integration.py, skills/codebase-intelligence/tests/test_integration.py, skills/feature-planner/tests/test_integration.py, skills/refactoring-safety/tests/test_integration.py, skills/regression-hunter/tests/test_integration.py, skills/release-readiness/tests/test_integration.py, skills/root-cause-analyzer/tests/test_integration.py, skills/security-context-guard/tests/test_integration.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/report.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +112 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=high, resolved=skills/release-readiness/engine/report.py, fan_in=1, fan_out=10 [hotspot]
  - caller: `evaluations/acceptance-test-engineer/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/adversarial-diff-reviewer/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/architecture-decision/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/codebase-intelligence/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/feature-planner/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/refactoring-safety/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/regression-hunter/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/release-readiness/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/root-cause-analyzer/run_evaluation.py` (fan_in=0)
  - caller: `evaluations/security-context-guard/run_evaluation.py` (fan_in=0)
  - ... and 43 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_integration.py, skills/acceptance-test-engineer/tests/test_report.py, skills/adversarial-diff-reviewer/tests/test_integration.py, skills/adversarial-diff-reviewer/tests/test_report.py, skills/architecture-decision/tests/test_ci_report_loader.py, skills/architecture-decision/tests/test_integration.py, skills/architecture-decision/tests/test_report.py, skills/codebase-intelligence/tests/test_integration.py, skills/codebase-intelligence/tests/test_report.py, skills/feature-planner/tests/test_ci_report_loader.py, skills/feature-planner/tests/test_integration.py, skills/feature-planner/tests/test_report.py, skills/refactoring-safety/tests/test_ci_report_loader.py, skills/refactoring-safety/tests/test_integration.py, skills/refactoring-safety/tests/test_report.py, skills/regression-hunter/tests/test_ci_report_loader.py, skills/regression-hunter/tests/test_integration.py, skills/regression-hunter/tests/test_report.py, skills/release-readiness/tests/test_ci_report_loader.py, skills/release-readiness/tests/test_integration.py, skills/release-readiness/tests/test_regression_report_loader.py, skills/release-readiness/tests/test_report.py, skills/release-readiness/tests/test_security_report_loader.py, skills/root-cause-analyzer/tests/test_ci_report_loader.py, skills/root-cause-analyzer/tests/test_integration.py, skills/root-cause-analyzer/tests/test_report.py, skills/security-context-guard/tests/test_integration.py, skills/security-context-guard/tests/test_report.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/security_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +54 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/security_report_loader.py, fan_in=1, fan_out=1
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_security_report_loader.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/release-readiness/tests/test_security_report_loader.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/stats.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +50 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/stats.py, fan_in=1, fan_out=1
  - caller: `skills/acceptance-test-engineer/engine/report.py` (fan_in=1)
  - caller: `skills/acceptance-test-engineer/tests/test_stats.py` (fan_in=0)
  - caller: `skills/adversarial-diff-reviewer/engine/report.py` (fan_in=1)
  - caller: `skills/adversarial-diff-reviewer/tests/test_stats.py` (fan_in=0)
  - caller: `skills/architecture-decision/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/architecture-decision/tests/test_stats.py` (fan_in=0)
  - caller: `skills/feature-planner/engine/report.py` (fan_in=1)
  - caller: `skills/feature-planner/tests/test_stats.py` (fan_in=0)
  - caller: `skills/refactoring-safety/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/refactoring-safety/tests/test_stats.py` (fan_in=0)
  - ... and 7 more callers (see JSON output)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/acceptance-test-engineer/tests/test_stats.py, skills/adversarial-diff-reviewer/tests/test_stats.py, skills/architecture-decision/tests/test_stats.py, skills/feature-planner/tests/test_stats.py, skills/refactoring-safety/tests/test_stats.py, skills/regression-hunter/tests/test_stats.py, skills/release-readiness/tests/test_stats.py, skills/root-cause-analyzer/tests/test_stats.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/target_resolver.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +84 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/target_resolver.py, fan_in=1, fan_out=1
  - caller: `skills/refactoring-safety/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/refactoring-safety/tests/test_target_resolver.py` (fan_in=0)
  - caller: `skills/regression-hunter/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/regression-hunter/tests/test_target_resolver.py` (fan_in=0)
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_target_resolver.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/refactoring-safety/tests/test_target_resolver.py, skills/regression-hunter/tests/test_target_resolver.py, skills/release-readiness/tests/test_target_resolver.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/engine/test_coverage_scanner.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +40 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=medium, resolved=skills/release-readiness/engine/test_coverage_scanner.py, fan_in=1, fan_out=1
  - caller: `skills/refactoring-safety/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/refactoring-safety/tests/test_test_coverage_scanner.py` (fan_in=0)
  - caller: `skills/regression-hunter/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/regression-hunter/tests/test_test_coverage_scanner.py` (fan_in=0)
  - caller: `skills/release-readiness/engine/report.py` (fan_in=1 [hotspot])
  - caller: `skills/release-readiness/tests/test_test_coverage_scanner.py` (fan_in=0)
- **Axis 3 — Test coverage**: covered=yes
  - Covered by: skills/refactoring-safety/tests/test_test_coverage_scanner.py, skills/regression-hunter/tests/test_test_coverage_scanner.py, skills/release-readiness/tests/test_test_coverage_scanner.py
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/pyproject.toml` (new) — readiness: **NEEDS-REVIEW**
- Lines: +13 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `<unknown>` (modified) — readiness: **NEEDS-REVIEW**
- Lines: +0 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=(unresolved), fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_blast_radius_scorer.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +28 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_blast_radius_scorer.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_ci_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +48 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_ci_report_loader.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_cli.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +124 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_cli.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_diff_parser.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +83 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_diff_parser.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_integration.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +71 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_integration.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_readiness_scorer.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +73 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_readiness_scorer.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_regression_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +55 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_regression_report_loader.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_report.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +159 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_report.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_security_report_loader.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +51 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_security_report_loader.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_stats.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +81 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_stats.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_target_resolver.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +71 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_target_resolver.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

### `skills/release-readiness/tests/test_test_coverage_scanner.py` (new) — readiness: **NEEDS-REVIEW**
- Lines: +58 / -0
- **Axis 1 — Diff-hygiene flags** (0):
  - None detected by pattern matching.
- **Axis 2 — Structural blast radius**: tier=low, resolved=skills/release-readiness/tests/test_test_coverage_scanner.py, fan_in=0, fan_out=0
- **Axis 3 — Test coverage**: covered=no
- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)

## Warnings
- At least one changed file's readiness tier is BLOCKED (a diff-hygiene flag, or high structural blast radius with no test coverage) — this diff is NOT recommended for release without further changes.
