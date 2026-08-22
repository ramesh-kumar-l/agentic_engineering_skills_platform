# Codebase Intelligence — quickstart

Deterministic, stdlib-only structural analysis of a repository. See `SKILL.md`
for the full skill contract (when to use it, security constraints, outputs).

## Run it

```bash
cd skills/codebase-intelligence
python -m engine.cli /path/to/repo --format both --out /path/to/output-dir
```

Omit `--out` to print to stdout instead of writing files.

## Run the tests

```bash
cd skills/codebase-intelligence
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/codebase-intelligence
python run_evaluation.py
```

Writes `RESULTS.md` with actual scores against the 4 fixture repositories.
