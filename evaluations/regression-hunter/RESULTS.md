# Regression Hunter — Evaluation Results

Deterministic layer (diff-pattern flags + the combined per-file overall_risk_tier from Axis 1/2/3, ADR-015) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Regression Risk Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-clean-rename-covered-low-risk
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.26ms)
- Mismatches: none
- Files: [('engine/util.py', 'low', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-removed-exception-handling-hotspot-uncovered
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.69ms)
- Mismatches: none
- Files: [('engine/payment.py', 'high', ['removed-exception-handling'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-removed-conditional-guard-covered-medium
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.20ms)
- Mismatches: none
- Files: [('engine/session.py', 'medium', ['removed-conditional-guard'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-large-deletion-medium-fan-in-uncovered
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.39ms)
- Mismatches: none
- Files: [('engine/report_builder.py', 'high', ['large-deletion-no-addition'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-decreased-test-assertions
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.72ms)
- Mismatches: none
- Files: [('tests/test_mathlib.py', 'medium', ['decreased-test-assertions'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-signature-change-diff-uncovered-but-report-covered
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.44ms)
- Mismatches: none
- Files: [('engine/api.py', 'medium', ['modified-signature-no-test-change'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-unresolved-new-file
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (0.19ms)
- Mismatches: none
- Files: [('engine/new_feature.py', 'medium', ['modified-signature-no-test-change'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-multi-file-mixed-risk
### Deterministic layer (diff-pattern flags + overall risk tier)
- Correctness: 5/5
- Efficiency: 5/5 (1.18ms)
- Mismatches: none
- Files: [('engine/core.py', 'high', ['removed-exception-handling']), ('engine/util2.py', 'low', []), ('engine/helper.py', 'high', ['removed-conditional-guard'])]
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

This is the EIGHTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, and refactoring-safety) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition, which every fixture exercises for real — not as proof of real-world regression-detection judgment quality. The inter-rater-agreement experiment A5 calls for has still not been run. Case-06 and case-07 also exercise a real, deliberate divergence between axes: a diff-level 'no test file changed in THIS diff' flag can fire even when the composed codebase-intelligence report shows the file genuinely has real test coverage (case-06) — the two are independent signals by design, not a bug, and only the agent's Step 3 judgment can weigh which one matters more for a given diff.