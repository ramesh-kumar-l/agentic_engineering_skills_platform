# Feature Planner — Evaluation Results

Deterministic layer (planning-anti-pattern flags + codebase-intelligence-grounded relevance scoring) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real structured-plan cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-vague-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.19ms)
- Mismatches: none
- Relevant files surfaced: ['engine/notifications.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-well-scoped-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.18ms)
- Mismatches: none
- Relevant files surfaced: ['engine/export_cli.py', 'engine/exporter.py', 'engine/import_cli.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 4
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-hotspot-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.17ms)
- Mismatches: none
- Relevant files surfaced: ['engine/config_loader.py', 'engine/app.py', 'engine/worker.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-no-verification-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.18ms)
- Mismatches: none
- Relevant files surfaced: ['engine/payment_worker.py', 'engine/backoff.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-security-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.22ms)
- Mismatches: none
- Relevant files surfaced: ['engine/user_api.py', 'engine/auth.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-no-relevant-modules-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.16ms)
- Mismatches: none
- Relevant files surfaced: []
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-dependency-blocker-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.18ms)
- Mismatches: none
- Relevant files surfaced: ['engine/reporting.py', 'engine/db.py']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-conflicting-scope-task
### Deterministic layer (planning flags + relevance)
- Correctness: 5/5
- Efficiency: 5/5 (0.16ms)
- Mismatches: none
- Relevant files surfaced: ['engine/formatter.py', 'engine/cli.py']
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

This is the THIRD judgment-based skill evaluated this way (after adversarial-diff-reviewer and acceptance-test-engineer) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected plan categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (ADR-010), which every fixture exercises for real, not as proof of real-world planning quality. The inter-rater-agreement experiment A5 calls for has still not been run.