# Dependencies

This document explains exactly what this project depends on, why the list is
so short, and how installation works across the nine skills. If you're
looking for step-by-step setup instructions instead, see
[`QuickStarterGuide.md`](QuickStarterGuide.md).

## The short version

- **Runtime dependencies: zero.** Every skill engine runs on the Python
  standard library only.
- **Dev/test dependency: one.** `pytest>=7.0`, needed to run the test suites
  and evaluation harnesses.
- **Interpreter requirement:** Python **3.10 or newer** (every skill's
  `pyproject.toml` declares `requires-python = ">=3.10"` — the engines use
  `X | None` union-type syntax and `dataclasses`, both of which need 3.10+).
- **No Node.js, no Docker, no database, no external API keys, no network
  access required to run or test anything in this repo.**

## Why zero runtime dependencies is a deliberate choice, not an accident

This is documented formally as [ADR-006](project-memory-bank/11-decisions.md)
in the architectural decisions log, and it applies to all nine skills, not
just the first one:

- **Portability.** An agent runtime invoking a skill only needs a Python 3.10+
  interpreter and a shell — no `pip install` round trip, no dependency
  resolution, no risk of a transitive dependency pulling in something
  unvetted. This matters specifically because these skills are meant to be
  invoked *by AI agents*, often in sandboxed or ephemeral environments where
  a slow or flaky install step is a real reliability risk, not just an
  inconvenience.
- **Security surface.** Fewer dependencies means a smaller supply-chain
  attack surface. A `pip-audit` on this repo's *runtime* code will always
  return nothing to audit, by construction.
- **Simplicity over premature optimization.** `ast`, `re`, `json`, `pathlib`,
  `dataclasses`, and `argparse` cover everything all nine engines need
  (structural parsing, regex pattern matching, report rendering, CLI
  wiring). Reaching for a third-party parser or framework before there's
  concrete evidence the stdlib approach is insufficient would be exactly the
  kind of premature complexity this project's engineering discipline
  explicitly avoids (see [`project-memory-bank/00-project-vision.md`](project-memory-bank/00-project-vision.md)'s
  non-negotiable operating stance).
- **This is a real, disclosed tradeoff, not a free lunch.** [Known
  limitation L3](project-memory-bank/12-known-limitations.md) documents that
  non-Python import extraction is regex-based, not a real AST/parser for
  JS/TS/Java — a tree-sitter-quality multi-language parser would need a real
  dependency. That tradeoff is deliberately deferred until real usage shows
  it matters, not silently avoided.

## What's actually in each skill's `pyproject.toml`

All nine skills follow the identical shape:

```toml
[project]
name = "<skill-name>"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

`dependencies = []` is not a placeholder — it's the actual, current, correct
list for every skill:

| Skill | Runtime dependencies | Dev dependencies |
|---|---|---|
| `codebase-intelligence` | none | `pytest>=7.0` |
| `adversarial-diff-reviewer` | none | `pytest>=7.0` |
| `acceptance-test-engineer` | none | `pytest>=7.0` |
| `feature-planner` | none | `pytest>=7.0` |
| `security-context-guard` | none | `pytest>=7.0` |

## How to install

This repo is a collection of nine **independent** Python packages under
`skills/`, not one installable package at the root — there is no root
`pyproject.toml` and none is planned until there's real evidence a unified
package boundary is needed (avoid premature packaging, same discipline as
everything else in this project).

**Option A — just run the tests/tools with pytest available (fastest):**

```bash
pip install -r requirements.txt
```

This is enough to run every skill's test suite and evaluation harness, since
none of the engines themselves need installing to be *run* — `python -m
engine.cli ...` works directly from inside a skill's directory because each
`pyproject.toml` sets `pythonpath = ["."]` for pytest, and the engine package
itself has no external imports to resolve.

**Option B — editable install of a specific skill (if you want the package
importable from elsewhere, or want `pip check` to see it):**

```bash
cd skills/<skill-name>
pip install -e ".[dev]"
```

Repeat per skill you want installed. There is intentionally no single command
that installs all nine at once — see
[`QuickStarterGuide.md`](QuickStarterGuide.md) for a loop that does it if you
want every skill available at once.

## Non-Python tooling you need

- **Git** — to clone the repo and (for `adversarial-diff-reviewer`) to
  produce diffs via `git diff`.
- **A POSIX-ish shell or PowerShell** — the CLIs are plain `python -m
  engine.cli ...` invocations; nothing shell-specific is required beyond
  piping stdin on Unix-likes (`git diff | python -m engine.cli -`) or the
  PowerShell equivalent.

Nothing else. No Docker, no database, no cloud account, no API key, no
network access is required anywhere in this repository to clone it, run any
skill, run any test, or run any evaluation harness.

## Where dependency scope might grow

Per the adaptive-roadmap discipline in
[`project-memory-bank/08-roadmap.md`](project-memory-bank/08-roadmap.md), a
future skill could justify a real third-party dependency (e.g. a proper
multi-language parser for a future skill that needs it) — but only when
real evidence shows the stdlib-only approach is insufficient for that
specific skill, evaluated against the same decision checklist every
architectural decision in this project goes through (see
[`project-memory-bank/11-decisions.md`](project-memory-bank/11-decisions.md)).
This file will be updated the moment that happens — if you're reading this
and a skill now has a non-empty `dependencies` list, trust the
`pyproject.toml`, not a stale claim here.
