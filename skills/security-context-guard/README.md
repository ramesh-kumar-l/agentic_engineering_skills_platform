# Security Context Guard — quickstart

Deterministic classify/minimize/sanitize engine, wrapped by an agent-driven
Security Decision Checklist workflow. Composition with
`codebase-intelligence` is optional (unlike `feature-planner`'s ADR-010) —
useful standalone. See `SKILL.md` for the full skill contract (when to use
it, security constraints, outputs).

**Status**: Level 2 — Evaluated · Trust Status: `EXPERIMENTAL` · 58/58 tests
passing (CLI test file written from the start) · 8/8 fixtures: deterministic
layer 100%, judgment layer 100% precision/recall (self-authored/single-rater,
fourth skill scored this way — see
[`L8`](../../project-memory-bank/12-known-limitations.md)) · zero runtime
dependencies · architecture pattern: [ADR-007](../../project-memory-bank/11-decisions.md)
+ [ADR-011](../../project-memory-bank/11-decisions.md) (the engine's
`suggested_verdict` is always advisory — it never authorizes an action
itself). A real dogfood run found and fixed a genuine bug in this skill's
own action classifier:
[`L16`](../../project-memory-bank/12-known-limitations.md). Full narrative:
[Building an AI Agent That Can't Authorize Its Own Actions](../../blogs/05-building-an-ai-agent-that-cant-authorize-its-own-actions.md).

## Run the engine

```bash
cd skills/security-context-guard

# Classify a file before it's exposed/pushed/sent somewhere
python -m engine.cli path/to/content.txt \
  --action "Push this branch to origin/main." \
  --paths some/file.py .env \
  --format both --out /path/to/output-dir
```

Or pipe content via stdin: `echo "..." | python -m engine.cli - --action "..."`.
Omit `--out` to print to stdout instead of writing files. `--ci-report` is
optional and only adds a hotspot-touch note — a missing or unreadable report
is a warning, never a failure.

The engine only produces the deterministic classification packet (matches +
`suggested_verdict`). The actual recommendation to a human is derived by the
agent following `SKILL.md`'s Step 3, not by this CLI alone — and the engine
never authorizes anything itself (see `SKILL.md` Security Constraints).

## Run the tests

```bash
cd skills/security-context-guard
pip install -e ".[dev]"
pytest
```

## Run the evaluation harness

```bash
cd evaluations/security-context-guard
python run_evaluation.py
```

Writes `RESULTS.md` with scores for both the deterministic classification
layer and the judgment layer (this session's actual checklist derivation vs.
ground truth).
