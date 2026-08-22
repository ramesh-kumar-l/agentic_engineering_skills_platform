# Adversarial Diff Reviewer — Evaluation Results

Deterministic risk-flag layer is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real findings this session's agent produced by actually performing the adversarial review, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-obvious-bug
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-subtle-bug
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-security-issue
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-broad-except
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-clean-diff
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 0
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-large-noisy-diff
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.07ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-missing-context
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
### Judgment layer (this session's actual review)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-concurrency-bug
### Deterministic risk-flag layer
- Correctness: 5/5
- Efficiency: 5/5 (0.04ms)
- Mismatches: none
### Judgment layer (this session's actual review)
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

This is the first evidence for a judgment-based skill in `project-memory-bank/16-assumptions-and-validation.md` (A5). It is single-run, single-rater evidence from this session's agent — the inter-rater-agreement experiment A5 calls for has NOT been run (that requires a second, independent reviewer/session). Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures, not as proof of real-world review quality.