# Dependency / Supply Chain — Evaluation Results

Deterministic layer (flag set + suggested_risk_level) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Dependency Risk Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-all-pinned-clean
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.44ms)
- Mismatches: none
- suggested_risk_level: CLEAR
- Flags: []
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-unpinned-range
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.24ms)
- Mismatches: none
- suggested_risk_level: NEEDS_REVIEW
- Flags: ['unpinned-range']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-known-risk-name
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.26ms)
- Mismatches: none
- suggested_risk_level: NEEDS_REVIEW
- Flags: ['known-risk-name']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-wildcard-version
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.19ms)
- Mismatches: none
- suggested_risk_level: REQUIRES_REVIEW
- Flags: ['unpinned-wildcard']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-duplicate-conflicting-versions
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.22ms)
- Mismatches: none
- suggested_risk_level: NEEDS_REVIEW
- Flags: ['duplicate-conflicting-version']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-large-surface-area
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.27ms)
- Mismatches: none
- suggested_risk_level: NEEDS_REVIEW
- Flags: ['unpinned-range', 'unpinned-range', 'unpinned-range', 'unpinned-range']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-compounding-case
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.34ms)
- Mismatches: none
- suggested_risk_level: REQUIRES_REVIEW
- Flags: ['unpinned-wildcard', 'known-risk-name', 'duplicate-conflicting-version']
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-zero-dependencies-ambiguous
### Deterministic layer (flags + suggested_risk_level)
- Correctness: 5/5
- Efficiency: 5/5 (0.21ms)
- Mismatches: none
- suggested_risk_level: REQUIRES_REVIEW
- Flags: []
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

This is the TENTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, regression-hunter, and release-readiness) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (every fixture) — not as proof of real-world dependency-risk judgment quality. The inter-rater- agreement experiment A5 calls for has still not been run. This skill also has no live CVE database and no per-dependency license data — see SKILL.md Known Limitations; the checklist's item 4 (license risk) is deliberately answered 'not available' in every case below, not fabricated.