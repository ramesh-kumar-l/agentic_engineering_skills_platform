# Engineering Knowledge Capture — Evaluation Results

Deterministic layer (candidate set + suggested_capture_priority) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Knowledge Capture Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-clean-narrative
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.84ms)
- Mismatches: none
- Candidates: []
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 0
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-single-decision
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.81ms)
- Mismatches: none
- Candidates: [('decision-we-decided', 'MEDIUM')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-single-lesson
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.60ms)
- Mismatches: none
- Candidates: [('lesson-turns-out', 'MEDIUM')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-single-workaround
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (1.91ms)
- Mismatches: none
- Candidates: [('workaround-explicit', 'MEDIUM')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-compounding-decision-and-limitation
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.55ms)
- Mismatches: none
- Candidates: [('decision-we-decided', 'MEDIUM'), ('limitation-known-limitation', 'MEDIUM')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 2
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-hotspot-module-mentioned
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.56ms)
- Mismatches: none
- Candidates: [('decision-we-decided', 'HIGH')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-resolved-non-hotspot-module
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.51ms)
- Mismatches: none
- Candidates: [('lesson-we-learned', 'MEDIUM')]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-zero-modules-ambiguous
### Deterministic layer (candidates + suggested_capture_priority)
- Correctness: 5/5
- Efficiency: 5/5 (0.87ms)
- Mismatches: none
- Candidates: [('decision-we-decided', 'MEDIUM')]
- Warnings: ["codebase-intelligence report declared zero modules — structural location resolution is impossible for any candidate; every candidate's priority fails closed to MEDIUM rather than being silently downranked to LOW."]
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

This is the ELEVENTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, regression-hunter, release-readiness, and dependency-supply-chain) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the workflow is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (every fixture) and the location-resolution fail-closed default (case-08) — not as proof of real-world knowledge-capture judgment quality. The inter-rater-agreement experiment A5 calls for has still not been run. This skill also never writes into the memory bank itself and does not parse real commit history — see SKILL.md Known Limitations.