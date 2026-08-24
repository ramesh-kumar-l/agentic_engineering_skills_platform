# Release Readiness — Evaluation Results

Deterministic layer (diff-hygiene flags + the per-file readiness_tier from Axis 1/2/3, ADR-016 + the report-level overall_verdict) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Release Readiness Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-clean-low-risk-covered
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.27ms)
- Mismatches: none
- Overall verdict: READY
- Files: [('engine/util.py', 'clear', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-debug-print-blocked-despite-covered-low-risk
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.27ms)
- Mismatches: none
- Overall verdict: NOT_READY
- Files: [('engine/util.py', 'blocked', ['debug-print-leftover'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-hotspot-uncovered-blocked-with-no-hygiene-flags
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.22ms)
- Mismatches: none
- Overall verdict: NOT_READY
- Files: [('engine/payment.py', 'blocked', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 4
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-hotspot-covered-needs-review
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.20ms)
- Mismatches: none
- Overall verdict: READY_WITH_CONDITIONS
- Files: [('engine/payment.py', 'needs-review', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-medium-structural-uncovered-needs-review
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.23ms)
- Mismatches: none
- Overall verdict: READY_WITH_CONDITIONS
- Files: [('engine/session.py', 'needs-review', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-merge-conflict-marker-blocked
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.20ms)
- Mismatches: none
- Overall verdict: NOT_READY
- Files: [('engine/config.py', 'blocked', ['merge-conflict-marker', 'merge-conflict-marker', 'merge-conflict-marker'])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-composed-regression-evidence-diverges-from-clear-axes
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.31ms)
- Mismatches: none
- Overall verdict: READY
- Files: [('engine/pricing.py', 'clear', [])]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 3
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-multi-file-mixed-with-security-report
### Deterministic layer (hygiene flags + readiness tier + overall verdict)
- Correctness: 5/5
- Efficiency: 5/5 (0.47ms)
- Mismatches: none
- Overall verdict: NOT_READY
- Files: [('engine/core.py', 'blocked', ['debug-print-leftover']), ('engine/util2.py', 'clear', []), ('engine/helper.py', 'needs-review', [])]
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

This is the NINTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, and regression-hunter) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (every fixture) and the optional regression-hunter/security-context-guard composition (case-07, case-08) — not as proof of real-world release-readiness judgment quality. The inter-rater-agreement experiment A5 calls for has still not been run. Case-03 and case-07 deliberately exercise real divergence between axes: case-03 has ZERO diff-hygiene flags but is still readiness_tier=blocked because a real hotspot with no test coverage is an absolute blocker on its own (Axis 2/3 alone can block, hygiene is not the only path to 'blocked'); case-07 has a CLEAR readiness_tier from Axes 1-3 while a composed regression- hunter report shows overall_risk_tier=high for the same file — the two are surfaced as separate fields BY DESIGN, never blended, so only the agent's Step 4 judgment can weigh which one matters more for this release.