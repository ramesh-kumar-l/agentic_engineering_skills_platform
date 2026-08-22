# Codebase Intelligence Report

- Root: `D:\ClaudeProjects\agentic_engineering_skills_platform`
- Generated: 2026-08-22T19:41:55.829659+00:00
- Files scanned: 242 (excluded dirs: 6, skipped files: 0)

## Language breakdown
- python: 75
- markdown: 68
- json: 64
- unknown: 29
- toml: 4
- javascript: 2

## Entry points
- `evaluations/acceptance-test-engineer/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/adversarial-diff-reviewer/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/multi-package-python/pkg/cli.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/simple-python/app.py` (if __name__ == '__main__')
- `evaluations/feature-planner/run_evaluation.py` (if __name__ == '__main__')
- `skills/acceptance-test-engineer/engine/cli.py` (if __name__ == '__main__')
- `skills/adversarial-diff-reviewer/engine/cli.py` (if __name__ == '__main__')
- `skills/codebase-intelligence/engine/cli.py` (if __name__ == '__main__')
- `skills/feature-planner/engine/cli.py` (if __name__ == '__main__')

## Internal dependency hotspots (top 10)
Modules with the most internal fan-in + fan-out — likely the highest-blast-radius files to change.
- `skills/codebase-intelligence/engine/models.py` — depended on by 8, depends on 0
- `skills/codebase-intelligence/engine/report.py` — depended on by 1, depends on 6
- `skills/feature-planner/engine/models.py` — depended on by 7, depends on 0
- `skills/acceptance-test-engineer/engine/models.py` — depended on by 6, depends on 0
- `skills/adversarial-diff-reviewer/engine/models.py` — depended on by 6, depends on 0
- `skills/feature-planner/engine/report.py` — depended on by 1, depends on 5
- `skills/acceptance-test-engineer/engine/report.py` — depended on by 1, depends on 4
- `skills/adversarial-diff-reviewer/engine/report.py` — depended on by 1, depends on 4
- `skills/feature-planner/engine/cli.py` — depended on by 0, depends on 4
- `skills/acceptance-test-engineer/engine/testability_scanner.py` — depended on by 1, depends on 2

## External dependencies
_None found (no requirements.txt / pyproject.toml / package.json)._

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
