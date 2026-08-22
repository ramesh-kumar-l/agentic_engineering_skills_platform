# 12 — Known Limitations

Running failure/limitation catalog. First entries from Phase 1
(codebase-intelligence). Format follows the failure-record structure in
[[05-evaluation-framework]]: What failed | Why | Impact | Fix | Regression prevention.

---

## L1: `has_main_guard` false-positive on string mentions (FIXED during Phase 1)

- **What failed**: Entry-point detection flagged files that merely contain the
  text `__name__ == "__main__"` inside a docstring, comment, or string literal
  as real CLI entry points.
- **Why**: Original implementation did a plain substring search over full file
  text instead of checking the AST for an actual top-level `if` statement.
- **Impact**: Found via dogfooding (running the engine on its own repo) —
  `engine/models.py`, `engine/report.py`, `engine/python_parser.py`, and two
  test files were misreported as entry points.
- **Fix**: Replaced with an AST check (`engine/python_parser.py::_has_main_guard`)
  that requires an actual top-level `ast.If` comparing `__name__` to the
  string `"__main__"`.
- **Regression prevention**: `tests/test_python_parser.py::test_has_main_guard_ignores_string_mentions`.

## L2: External dependency parsing is root-only, not recursive

- **What failed**: `external_deps.py` only checks the scan root directory for
  `requirements.txt`/`pyproject.toml`/`package.json` — it does not look for
  manifests in subdirectories.
- **Why**: Scoped down for Phase 1 to keep the module simple; monorepo/
  multi-package layouts weren't in the original fixture set.
- **Impact**: On a monorepo (e.g. this platform's own repo, where the real
  manifest lives at `skills/codebase-intelligence/pyproject.toml`, not root),
  the report shows zero external dependencies even though some exist deeper
  in the tree. Observed directly via dogfooding — see
  `examples/codebase-intelligence/example-run.md`.
- **Fix**: Not yet fixed — deferred. Revisit if/when a real user hits this on
  an actual monorepo (avoid over-engineering ahead of evidence, per
  [[05-evaluation-framework]]).
- **Regression prevention**: N/A yet — tracked here so it isn't silently
  forgotten or re-discovered from scratch later.

## L3: Non-Python import extraction is heuristic, not a real parser

- **What failed**: N/A (documented limitation, not an observed bug).
- **Why**: `generic_parser.py` uses regex patterns for JS/TS/Java imports
  rather than a real AST/parser for those languages.
- **Impact**: Will miss dynamic imports (`import(...)`), re-exports, and
  unusual formatting in non-Python files. JS internal-dependency resolution
  in `graph.py` only handles relative specifiers (`./`, `../`) — bundler path
  aliases (e.g. `@/utils`) are not resolved and will be (correctly) treated as
  external/unresolved.
- **Fix**: Not planned unless real usage shows this matters — multi-language
  AST parsing is a significant investment the assumptions ledger doesn't yet
  justify (see [[16-assumptions-and-validation]]).
- **Regression prevention**: Explicitly documented in `SKILL.md` ("When NOT to
  Use" / "Known Limitations") so agents don't over-trust non-Python results.

## L4: No semantic or cross-file type understanding

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: The engine is intentionally structural only (imports, def/class
  names, docstrings) — this is a deliberate scope decision, not an oversight.
- **Impact**: Cannot answer "does function X actually call function Y" or
  "what type does this return" — only "does file A import file B."
- **Fix**: Out of scope for this skill; a future skill could build on this
  report rather than this skill absorbing that scope.
- **Regression prevention**: Documented in `SKILL.md` under "Context
  Completeness."
