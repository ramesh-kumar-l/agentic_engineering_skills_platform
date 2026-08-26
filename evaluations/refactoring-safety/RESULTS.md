# Refactoring Safety — Evaluation Results

Deterministic layer (safety-quality anti-pattern flags + codebase-intelligence-grounded, per-target structural risk scoring) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Refactoring Safety Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-rename-clean-covered
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.26ms)
- Mismatches: none
- Operation type: rename — Targets: [('cache.py', 'engine/cache.py', 'medium'), ('cache_layer.py', None, 'low')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-vague-quick-rename
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.24ms)
- Mismatches: none
- Operation type: rename — Targets: [('auth.py', 'engine/auth.py', 'high'), ('authentication.py', None, 'low')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-missing-test-plan-signal
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.24ms)
- Mismatches: none
- Operation type: rename — Targets: [('pricing.py', 'engine/pricing.py', 'medium'), ('pricing_engine.py', None, 'low')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-hotspot-delete-untested
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.22ms)
- Mismatches: none
- Operation type: delete — Targets: [('legacy_router.py', 'engine/legacy_router.py', 'high')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-extract-low-risk-leaf
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.27ms)
- Mismatches: none
- Operation type: extract — Targets: [('formatter.py', 'engine/formatter.py', 'low')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-unresolved-target
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.25ms)
- Mismatches: none
- Operation type: rename — Targets: [('phantom_module.py', None, 'low'), ('ghost_module.py', None, 'low')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-bare-identifier-fallback
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.32ms)
- Mismatches: none
- Operation type: move — Targets: [('build_report', 'engine/report_builder.py', 'medium'), ('report_builder.py', 'engine/report_builder.py', 'medium')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-change-signature-boundary
### Deterministic layer (safety flags + target risk)
- Correctness: 5/5
- Efficiency: 5/5 (0.20ms)
- Mismatches: none
- Operation type: change-signature — Targets: [('notify.py', 'engine/notify.py', 'medium')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## Summary
Deterministic layer: all cases correct.
Judgment layer: perfect precision/recall across all 8 fixtures.

This is the SEVENTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, and architecture-decision) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition, which every fixture exercises for real — not as proof of real-world refactoring-safety judgment quality. The inter-rater-agreement experiment A5 calls for has still not been run. Case-01 and case-06 also exercise a real, deliberate ambiguity this engine cannot resolve on its own: an unresolved target can mean 'this is the new name in a rename, which legitimately doesn't exist yet' (case-01) or 'this refactor names nothing real in this repository' (case-06) — the engine reports the same resolved_module_path=None either way, and only the agent's Step 3 judgment (informed by the operation type) can tell them apart.