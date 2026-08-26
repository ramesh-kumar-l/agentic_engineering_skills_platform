# Engineering Memory — Evaluation Results

Deterministic layer (which record ids match, which are flagged stale, match count / raised-error / warning behavior) is scored automatically. Judgment-layer Precision/Recall are computed against `actual/*.actual.json` — real Engineering Memory Retrieval Checklist cases this session's agent produced by actually performing the derivation, not fabricated to match ground truth. Safety and Explainability require independent human review and are NOT scored here (project-memory-bank/05-evaluation-framework.md).

## case-01-clean-multi-match
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.63ms)
- Mismatches: none
- Matches: [('L23', 19, True), ('ADR-010', 14, False), ('ADR-018', 14, False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-02-no-relevant-memory
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.39ms)
- Mismatches: none
- Matches: []
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-03-whole-token-collision-resistance
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.43ms)
- Mismatches: none
- Matches: [('ADR-014', 8, False), ('L11', 1, False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-04-fixed-record-flagged-stale
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.35ms)
- Mismatches: none
- Matches: [('L16', 24, True)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-05-module-not-found
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.36ms)
- Mismatches: none
- Matches: [('ADR-002', 4, True)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-06-top-n-limits-output
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.45ms)
- Mismatches: none
- Matches: [('ADR-012', 19, False), ('ADR-013', 19, False)]
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-07-missing-ci-report
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.03ms)
- Mismatches: none
- Error raised: codebase-intelligence report not found at D:\ClaudeProjects\agentic_engineering_skills_platform\evaluations\engineering-memory\fixtures\case-07-missing-ci-report\ci_report.json. Run codebase-intelligence against the target repo first: python -m engine.cli <path> --format json --out <dir> (from skills/codebase-intelligence/).
### Judgment layer (this session's actual derivation)
- Precision: 1.0
- Recall: 1.0
- True Positives: 1
- False Positives: 0
- False Negatives: 0
- Safety: _human review required_
- Explainability: _human review required_

## case-08-malformed-memory-bank-file
### Deterministic layer (matches + staleness + count/error/warning)
- Correctness: 5/5
- Efficiency: 5/5 (0.28ms)
- Mismatches: none
- Matches: []
- Warnings: ['No records parsed from D:\\ClaudeProjects\\agentic_engineering_skills_platform\\evaluations\\engineering-memory\\fixtures\\case-08-malformed-memory-bank-file\\decisions.md / D:\\ClaudeProjects\\agentic_engineering_skills_platform\\evaluations\\engineering-memory\\fixtures\\case-08-malformed-memory-bank-file\\limitations.md — corpus is empty or the section-header format has drifted from what memory_bank_parser.py expects.']
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

This is the FOURTEENTH judgment-based skill evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer, feature-planner, security-context-guard, root-cause-analyzer, architecture-decision, refactoring-safety, regression-hunter, release-readiness, dependency-supply-chain, engineering-knowledge-capture, context-optimizer, and workflow-composer) — see `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in `project-memory-bank/12-known-limitations.md`. Same single-run, single-rater caveat: this session's agent authored the fixtures, the expected checklist categories, AND the actual derivation. Treat these scores as evidence the retrieval pipeline is executable and internally consistent on synthetic fixtures — including the required codebase-intelligence composition (every fixture with a report), whole-token collision resistance (case-03), and both staleness paths (case-04's FIXED-title path, case-05's module-no-longer-exists path) — not as proof of real-world retrieval-relevance judgment quality, and NOT as evidence toward A8 (project-memory-bank/16-assumptions-and-validation.md), which this build only creates the capability for. The inter-rater-agreement experiment A5 calls for has still not been run. This skill also never writes into the memory bank itself and this pass's corpus is limited to 11-decisions.md and 12-known-limitations.md — see SKILL.md Known Limitations.