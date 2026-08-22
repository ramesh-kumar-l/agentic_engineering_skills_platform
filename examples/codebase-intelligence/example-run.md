# Example run — this platform's own repository

Command:

```bash
cd skills/codebase-intelligence
python -m engine.cli /path/to/agentic_engineering_skills_platform --format both --out ./out
```

`report.md` (condensed) and `report.json` (full detail) from this exact run
are checked in alongside this file.

## What this run demonstrates

- 58 files scanned, 5 directories excluded (`.git`, `node_modules` fixture,
  and cache dirs), 0 files skipped.
- Correctly identifies the 4 real CLI entry points across the repo
  (`run_evaluation.py`, two fixture scripts, `engine/cli.py`) — earlier in
  development this list had false positives; see "What dogfooding caught"
  below.
- Ranks `engine/models.py` as the top hotspot (depended on by 8 modules, 0
  outgoing deps) — correctly identifies it as the shared schema every other
  engine module imports, exactly the kind of "highest blast radius if
  changed" signal this skill exists to surface.
- Correctly reports no repo-root external dependencies (the real manifest
  lives at `skills/codebase-intelligence/pyproject.toml`, not repo root —
  see the nested-manifest limitation below).

## What dogfooding caught (failure-first evidence)

The first run against this repo flagged `engine/models.py`, `engine/report.py`,
`engine/python_parser.py`, and two test files as false-positive entry points.
Root cause: `has_main_guard` did a plain substring search for the text
`__name__ == "__main__"`, which also matches when that text merely appears
inside a docstring, comment, or string literal (as it does in this very
engine's own source, and in tests that assert on that string). Fixed by
replacing the substring search with an AST check for an actual top-level
`if __name__ == "__main__":` statement (`engine/python_parser.py::_has_main_guard`).
Regression test added: `tests/test_python_parser.py::test_has_main_guard_ignores_string_mentions`.
This is recorded as the skill's first real failure in
`project-memory-bank/12-known-limitations.md`.

## Known limitation surfaced by this run

External dependency parsing only checks the scan root for
`requirements.txt`/`pyproject.toml`/`package.json` — it does not walk into
subdirectories for nested manifests (e.g. `skills/codebase-intelligence/pyproject.toml`
in this very repo). Documented in `project-memory-bank/12-known-limitations.md`.
