# Codebase Intelligence Report

- Root: `D:\ClaudeProjects\agentic_engineering_skills_platform`
- Generated: 2026-08-23T05:23:44.605889+00:00
- Files scanned: 478 (excluded dirs: 23, skipped files: 0)

## Language breakdown
- json: 141
- python: 141
- markdown: 118
- unknown: 69
- toml: 7
- javascript: 2

## Entry points
- `evaluations/acceptance-test-engineer/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/adversarial-diff-reviewer/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/architecture-decision/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/multi-package-python/pkg/cli.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/simple-python/app.py` (if __name__ == '__main__')
- `evaluations/feature-planner/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/root-cause-analyzer/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/security-context-guard/run_evaluation.py` (if __name__ == '__main__')
- `skills/acceptance-test-engineer/engine/cli.py` (if __name__ == '__main__')
- `skills/adversarial-diff-reviewer/engine/cli.py` (if __name__ == '__main__')
- `skills/architecture-decision/engine/cli.py` (if __name__ == '__main__')
- `skills/codebase-intelligence/engine/cli.py` (if __name__ == '__main__')
- `skills/feature-planner/engine/cli.py` (if __name__ == '__main__')
- `skills/root-cause-analyzer/engine/cli.py` (if __name__ == '__main__')
- `skills/security-context-guard/engine/cli.py` (if __name__ == '__main__')

## Internal dependency hotspots (top 10)
Modules with the most internal fan-in + fan-out — likely the highest-blast-radius files to change.
- `skills/architecture-decision/engine/models.py` — depended on by 8, depends on 0
- `skills/codebase-intelligence/engine/models.py` — depended on by 8, depends on 0
- `skills/root-cause-analyzer/engine/models.py` — depended on by 8, depends on 0
- `skills/architecture-decision/engine/report.py` — depended on by 1, depends on 6
- `skills/codebase-intelligence/engine/report.py` — depended on by 1, depends on 6
- `skills/feature-planner/engine/models.py` — depended on by 7, depends on 0
- `skills/root-cause-analyzer/engine/report.py` — depended on by 1, depends on 6
- `skills/acceptance-test-engineer/engine/models.py` — depended on by 6, depends on 0
- `skills/adversarial-diff-reviewer/engine/models.py` — depended on by 6, depends on 0
- `skills/feature-planner/engine/report.py` — depended on by 1, depends on 5

## External dependencies
- requirements.txt: pytest >=7.0

## Directories missing a README (top 10)
- `.claude`
- `evaluations/acceptance-test-engineer`
- `evaluations/acceptance-test-engineer/actual`
- `evaluations/acceptance-test-engineer/eval_cases`
- `evaluations/acceptance-test-engineer/expected`
- `evaluations/acceptance-test-engineer/fixtures/case-01-vague-requirement`
- `evaluations/acceptance-test-engineer/fixtures/case-02-well-specified-requirement`
- `evaluations/acceptance-test-engineer/fixtures/case-03-missing-error-handling`
- `evaluations/acceptance-test-engineer/fixtures/case-04-missing-boundary`
- `evaluations/acceptance-test-engineer/fixtures/case-05-implicit-permission-requirement`
