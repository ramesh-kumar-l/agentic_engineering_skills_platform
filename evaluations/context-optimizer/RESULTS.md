# Context Optimizer — Evaluation Results

Deterministic layer (recommended file set, tier, oversized_alone) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Context Optimization Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-empty-task-description
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.42ms)
- Mismatches: none
- Recommendations: []
- Warnings: ['Task description is empty — no recommendations can be produced.']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-hotspot-keyword-match
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.36ms)
- Mismatches: none
- Recommendations: [('engine/scanner.py', 'CORE', False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-low-fan-in-keyword-match
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.55ms)
- Mismatches: none
- Recommendations: [('engine/stats.py', 'SUPPORTING', False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-tight-budget-excludes-lower-relevance
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.41ms)
- Mismatches: none
- Recommendations: [('engine/alpha.py', 'CORE', False), ('engine/beta.py', 'EXCLUDED', False), ('engine/gamma.py', 'EXCLUDED', False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-oversized-file-flagged-not-dropped
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.35ms)
- Mismatches: none
- Recommendations: [('engine/giant.py', 'SUPPORTING', True)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-thin-signal-still-recommended
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.48ms)
- Mismatches: none
- Recommendations: [('engine/report.py', 'SUPPORTING', False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-word-boundary-regression
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.55ms)
- Mismatches: none
- Recommendations: []
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-zero-files-ci-report
### Deterministic layer (recommendations + tier + oversized_alone)
- Correctness: 5/5
- Efficiency: 5/5 (0.52ms)
- Mismatches: none
- Recommendations: []
- Warnings: ['codebase-intelligence report declared zero files — no candidates can be scored. Reported explicitly, not silently returned as an empty-but-successful recommendation list.']
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

This is the TWELFTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, regression-hunter, release-readiness, dependency-supply-chain, and engineering-knowledge-capture) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (every fixture), the fail-OPEN budget/tiering default (case-04/case-05/case-06), and the tokenized word-boundary regression guard (case-07) — not as proof of real-world context-recommendation quality. The inter-rater-agreement experiment A5 calls for has still not been run. This skill also never loads any file into any actual context window itself — see SKILL.md Known Limitations.