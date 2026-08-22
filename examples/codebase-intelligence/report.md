# Codebase Intelligence Report

- Root: `D:\ClaudeProjects\agentic_engineering_skills_platform`
- Generated: 2026-08-22T18:23:26.120160+00:00
- Files scanned: 58 (excluded dirs: 5, skipped files: 0)

## Language breakdown
- python: 24
- markdown: 23
- json: 5
- unknown: 3
- javascript: 2
- toml: 1

## Entry points
- `evaluations/codebase-intelligence/run_evaluation.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/multi-package-python/pkg/cli.py` (if __name__ == '__main__')
- `evaluations/codebase-intelligence/fixtures/simple-python/app.py` (if __name__ == '__main__')
- `skills/codebase-intelligence/engine/cli.py` (if __name__ == '__main__')

## Internal dependency hotspots (top 10)
Modules with the most internal fan-in + fan-out — likely the highest-blast-radius files to change.
- `skills/codebase-intelligence/engine/models.py` — depended on by 8, depends on 0
- `skills/codebase-intelligence/engine/report.py` — depended on by 1, depends on 6
- `skills/codebase-intelligence/engine/cli.py` — depended on by 0, depends on 3
- `evaluations/codebase-intelligence/fixtures/multi-package-python/pkg/core.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/render_json.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/render_markdown.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/external_deps.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/generic_parser.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/graph.py` — depended on by 1, depends on 1
- `skills/codebase-intelligence/engine/python_parser.py` — depended on by 1, depends on 1

## External dependencies
_None found (no requirements.txt / pyproject.toml / package.json)._

## Directories missing a README (top 10)
- `evaluations/codebase-intelligence`
- `evaluations/codebase-intelligence/eval_cases`
- `evaluations/codebase-intelligence/expected`
- `evaluations/codebase-intelligence/fixtures/empty-edge-case`
- `evaluations/codebase-intelligence/fixtures/mixed-lang`
- `evaluations/codebase-intelligence/fixtures/mixed-lang/client`
- `evaluations/codebase-intelligence/fixtures/multi-package-python`
- `evaluations/codebase-intelligence/fixtures/multi-package-python/pkg`
- `evaluations/codebase-intelligence/fixtures/simple-python`
- `project-memory-bank`
