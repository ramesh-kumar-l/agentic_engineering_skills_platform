# Acceptance Test Engineer — quickstart

Deterministic requirement-parsing + testability-flagging engine, wrapped by
an agent-driven acceptance-case-derivation workflow. See `SKILL.md` for the
full skill contract (when to use it, security constraints, outputs).

## Run the engine

```bash
cd skills/acceptance-test-engineer
echo "The upload endpoint should be fast and user-friendly." | python -m engine.cli - --format both --out /path/to/output-dir
```

Or point it at a saved requirement file: `python -m engine.cli path/to/requirement.txt`.
Omit `--out` to print to stdout instead of writing files.

The engine only produces the deterministic pre-processing packet (stats +
testability flags). The actual acceptance-case derivation is performed by the
agent following `SKILL.md`'s Step 3, not by this CLI alone.

## Run the tests

```bash
cd skills/acceptance-test-engineer
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/acceptance-test-engineer
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic testability-flag
layer and the judgment layer (this session's actual acceptance-case
derivation vs. ground truth).
