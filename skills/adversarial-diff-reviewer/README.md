# Adversarial Diff Reviewer — quickstart

Deterministic diff-parsing + risk-flagging engine, wrapped by an agent-driven
adversarial review workflow. See `SKILL.md` for the full skill contract (when
to use it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 23/23 tests
passing (includes CLI coverage added after
[`L10`](../../project-memory-bank/12-known-limitations.md)) · 8/8 fixtures:
deterministic layer 100%, judgment layer 100% precision/recall
(self-authored/single-rater — see
[`L8`](../../project-memory-bank/12-known-limitations.md), and read
[why that caveat matters](../../blogs/04-your-ai-eval-says-100-percent.md)
before trusting the number) · zero runtime dependencies · architecture
pattern: [ADR-007/ADR-008](../../project-memory-bank/11-decisions.md).

## Run the engine

```bash
cd skills/adversarial-diff-reviewer
git diff | python -m engine.cli - --format both --out /path/to/output-dir
```

Or point it at a saved diff file: `python -m engine.cli path/to/change.diff`.
Omit `--out` to print to stdout instead of writing files.

The engine only produces the deterministic pre-processing packet (stats + risk
flags). The actual adversarial review is performed by the agent following
`SKILL.md`'s Step 3, not by this CLI alone.

## Run the tests

```bash
cd skills/adversarial-diff-reviewer
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/adversarial-diff-reviewer
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic risk-flag layer and
the judgment layer (this session's actual review findings vs. ground truth).
