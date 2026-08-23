# Architecture Decision — Evaluation Results

Deterministic layer (decision-quality anti-pattern flags + codebase-intelligence-grounded, per-option blast-radius scoring) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real decision-record cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-two-options-clean
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.29ms)
- Mismatches: none
- Option impacts: [('Option A', 'high', 14), ('Option B', 'high', 14)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-single-option-vague
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.15ms)
- Mismatches: none
- Option impacts: [('proposed', 'low', 2)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-options-missing-tradeoff
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.15ms)
- Mismatches: none
- Option impacts: [('Option A', 'medium', 3), ('Option B', 'low', 0)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-hotspot-blast-radius
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.17ms)
- Mismatches: none
- Option impacts: [('Option A', 'high', 18), ('Option B', 'low', 0)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-low-blast-radius-leaf
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.16ms)
- Mismatches: none
- Option impacts: [('Option A', 'low', 1), ('Option B', 'low', 0)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-missing-security-signal
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.18ms)
- Mismatches: none
- Option impacts: [('Option A', 'medium', 4), ('Option B', 'medium', 5)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-numbered-list-options
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.26ms)
- Mismatches: none
- Option impacts: [('Item 1', 'high', 14), ('Item 2', 'high', 12), ('Item 3', 'high', 12)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-vs-split-mixed-tier
### Deterministic layer (decision flags + option impacts)
- Correctness: 5/5
- Efficiency: 5/5 (0.26ms)
- Mismatches: none
- Option impacts: [('Alternative 1', 'high', 10), ('Alternative 2', 'high', 10)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## Summary
Deterministic layer: all cases correct.
Judgment layer: perfect precision/recall across all 8 fixtures.

This is the SIXTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, and root-cause-analyzer) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected decision-record categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition, which every fixture exercises for real — not as proof of real-world architecture-decision quality. The inter-rater-agreement experiment A5 calls for has still not been run. Case-01 and case-05 also surfaced a real, disclosed limitation: the keyword scorer treats a shared path prefix (here, every module under `engine/`) as a relevance signal, inflating blast radius for options that never actually mention the extra modules — the same class of limitation already logged as L14 (feature-planner) and L19 (root-cause-analyzer).