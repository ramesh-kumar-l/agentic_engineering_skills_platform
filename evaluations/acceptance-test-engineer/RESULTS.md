# Acceptance Test Engineer — Evaluation Results

Deterministic testability-flag layer is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real acceptance test cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-vague-requirement
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.06ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-well-specified-requirement
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.06ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-missing-error-handling
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-missing-boundary
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-implicit-permission-requirement
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-ambiguous-scope
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-already-has-acceptance-criteria
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.10ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-conflicting-requirement
### Deterministic testability-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 4
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## Summary
Deterministic layer: all cases correct.
Judgment layer: perfect precision/recall across all 8 fixtures.

This is the second judgment-based skill evaluated in `project-memory-bank/16-assumptions-and-validation.md` (A5), same single-run, single-rater caveat as Phase 2 (L8): this session's agent authored the fixtures, the expected coverage categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures, not as proof of real-world acceptance-criteria quality — the inter-rater- agreement experiment A5 calls for has still not been run.