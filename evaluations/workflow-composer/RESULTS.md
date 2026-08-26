# Workflow Composer — Evaluation Results

Deterministic layer (step statuses, compatibility-issue count, dry-run side-effect absence, CLI exit code) is scored automatically — real registry templates run against the bundled `tiny-repo` fixture, real subprocess execution; fail-closed paths (step failure, compatibility drift) run against the pytest suite's `fake-skills` fixtures for determinism. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Workflow Composition Checklist cases this session's agent produced by actually reasoning about each fixture, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here.

## case-01-clean-fit-understand-then-plan
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (4.32ms)
- Mismatches: none
- Actual: {'step_statuses': ['PENDING', 'PENDING'], 'compatibility_issue_count': 0, 'no_output_files': True}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-clean-fit-understand-then-test-plan
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (3.14ms)
- Mismatches: none
- Actual: {'step_statuses': ['PENDING', 'PENDING'], 'compatibility_issue_count': 0, 'no_output_files': True}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-clean-fit-understand-then-optimize-context
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (1.83ms)
- Mismatches: none
- Actual: {'step_statuses': ['PENDING', 'PENDING'], 'compatibility_issue_count': 0, 'no_output_files': True}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-poor-fit-no-good-template
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (1.78ms)
- Mismatches: none
- Actual: {'step_statuses': ['PENDING', 'PENDING'], 'compatibility_issue_count': 0, 'no_output_files': True}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-step-failure-stops-chain
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (1137.87ms)
- Mismatches: none
- Actual: {'step_statuses': ['OK', 'FAILED', 'SKIPPED'], 'compatibility_issue_count': 0}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-compatibility-drift-blocks-execution
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (0.13ms)
- Mismatches: none
- Actual: {'step_statuses': ['SKIPPED', 'SKIPPED'], 'compatibility_issue_count': 1}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-dry-run-zero-subprocess-calls
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (1.90ms)
- Mismatches: none
- Actual: {'step_statuses': ['PENDING', 'PENDING'], 'compatibility_issue_count': 0, 'no_output_files': True}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-unknown-template-name
### Deterministic layer (step statuses + compatibility)
- Correctness: 5/5
- Efficiency: 5/5 (27.46ms)
- Mismatches: none
- Actual: {'cli_exit_code': 1}
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## Summary
Deterministic layer: all cases correct.
Judgment layer: perfect precision/recall across all 8 fixtures.

This is the THIRTEENTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, regression-hunter, release-readiness, dependency-supply-chain, engineering-knowledge-capture, and context-optimizer) — see project-memory-bank/16-assumptions-and-validation.md (A5) and L8 in project-memory-bank/12-known-limitations.md. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected categories, AND the actual derivation. Treat these scores as evidence the workflow-composer engine is executable and internally consistent — including the tenth ADR-010 composition (cases 01/03), the TEXT_APPEND wiring mode (case 02), the fail-closed step-failure default (case 05), and the compatibility-drift pre-execution gate (case 06) — not as proof of real-world workflow-composition quality, and NOT as Experiment B (ADR-009) — real timing data in these results is disclosed evidence, never cited as validating A10's status.