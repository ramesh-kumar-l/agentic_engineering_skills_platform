# Root Cause Analyzer — Evaluation Results

Deterministic layer (symptom-quality anti-pattern flags + codebase-intelligence-grounded, stack-trace/keyword tiered candidate scoring) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real investigation cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-stack-trace-clean
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.30ms)
- Mismatches: none
- Candidates surfaced: [('engine/cart.py', 'stack-trace'), ('engine/tax.py', 'keyword'), ('engine/checkout.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-keyword-only-no-trace
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.20ms)
- Mismatches: none
- Candidates surfaced: [('engine/search.py', 'keyword'), ('engine/index.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-vague-report
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.15ms)
- Mismatches: none
- Candidates surfaced: [('engine/app.py', 'keyword'), ('engine/worker.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 0.67
- Recall: 0.67
- True Positives: 2
- False Positives: 1
- False Negatives: 1
- Safety: _human review required_
- Explainability: _human review required_

## case-04-hotspot-candidate
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.21ms)
- Mismatches: none
- Candidates surfaced: [('engine/config_loader.py', 'keyword'), ('engine/app.py', 'keyword'), ('engine/worker.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-stack-trace-outside-repo
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.21ms)
- Mismatches: none
- Candidates surfaced: [('engine/export.py', 'keyword'), ('engine/reports.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-multiple-candidates-conflicting
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.17ms)
- Mismatches: none
- Candidates surfaced: [('engine/report_export.py', 'keyword'), ('engine/user_repository.py', 'keyword'), ('engine/report_scheduler.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-recent-change-correlation
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.19ms)
- Mismatches: none
- Candidates surfaced: [('engine/webhook_handler.py', 'keyword'), ('engine/payments.py', 'keyword')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-fix-risk-high-fanin
### Deterministic layer (symptom flags + candidates)
- Correctness: 5/5
- Efficiency: 5/5 (0.25ms)
- Mismatches: none
- Candidates surfaced: [('engine/response_builder.py', 'stack-trace'), ('engine/orders_api.py', 'keyword'), ('engine/users_api.py', 'keyword')]
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
Judgment layer: one or more fixtures had imperfect precision/recall — see above.

This is the FIFTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, and security-context-guard) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected investigation categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition, which every fixture exercises for real, not as proof of real-world root-cause diagnosis quality. The inter-rater-agreement experiment A5 calls for has still not been run.