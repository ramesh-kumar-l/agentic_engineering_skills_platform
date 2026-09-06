# 24 — ValidationReport Schema (TEP Phase 5c, part 2 — Independent Validation)

Documents the schema implemented in `test_validation/models.py`, per
[[18-test-engineering-platform-contract]]'s TEP Phase 5c exit criteria:
independently execute agent-authored test files against the target repo and
record real pass/fail/exit-code/output evidence — the first execution
capability anywhere in this platform. See [[11-decisions|ADR-029]] for the
implementation decision and its explicit Security disclosure.

## Fields

| Field | Source | Rationale |
|---|---|---|
| `schema_version` | constant `"1.0"` | same pattern as every prior TEP report schema |
| `repo_root` | the CLI's `target_repo_root` argument, resolved to absolute | importable at execution time via `PYTHONPATH` |
| `generated_tests_dir` | the CLI's positional argument | which directory of agent-authored files was executed |
| `test_environment_profile_path` | the path passed on the CLI | which upstream input's detected framework was used |
| `stats` | computed | `test_files_considered`, `passed`, `failed`, `timed_out` |
| `outcomes` | computed, one per real candidate test file | see `ValidationOutcome` below |
| `warnings` | e.g. zero test files found | explicit disclosure, never a silent empty list |

Each `ValidationOutcome` carries:

- `test_file` — absolute path (see "Two real bugs" below for why this
  matters).
- `framework` — the primary test framework from the input profile (e.g.
  `"pytest"`), carried through, not re-detected.
- `command` — the exact subprocess argv actually run, or `[]` when no
  runner is supported for that file's extension.
- `exit_code`, `passed`, `timed_out` — what the process actually reported;
  `passed` is `True` only when `exit_code == 0` and the process did not
  time out.
- `stdout_excerpt` / `stderr_excerpt` — the last 2000 characters of each
  stream, enough to see a pytest summary line or a real traceback without
  storing unbounded output.
- `duration_ms` — real wall-clock time for that one subprocess invocation.

## What is deliberately excluded (no sandboxing beyond a timeout)

**This is this platform's first execution capability.** Every one of the 15
portfolio skills, and every TEP package before this one, is pure static
analysis; `validation_runner.py` runs real code via `subprocess.run`. A
strict per-file timeout is enforced (`DEFAULT_TIMEOUT_SECONDS = 30`,
overridable via `--timeout`), but there is **no filesystem or network
sandboxing** beyond what the OS-level test runner itself provides —
executing a generated test here carries exactly the same risk as running
that file inside the target repo's own CI. Disclosed explicitly, not a
claim of secure isolation.

Only Python (`pytest`, via `sys.executable -m pytest`) is actually executed.
A `.java`/`.kt` file is recognized as a real candidate file but always
returns an explicit "no supported runner" outcome — a real Maven/Gradle
run needs the target repo's own build file, out of scope for validating one
loose generated file, and this engine does not guess at a build-system
invocation it has no manifest for.

## Two real bugs this dogfood run found (and fixed, not just disclosed)

Both were fixed in the engine itself, not worked around in the demo — see
`examples/test-validation/example-run.md` for the full account:

1. `run_validation` sets the subprocess `cwd` to `test_file.parent`; a
   relative `test_file` or `repo_root` (e.g. `"."`, exactly what a caller
   invoking from a repo's own root would naturally pass) resolved against
   the *new* cwd instead of the caller's original one. Fixed by resolving
   both to absolute paths at the top of `run_validation`, before either is
   used.
2. `list_generated_tests` had no filter, so a prior run's own
   `.pytest_cache/` directory was itself listed and reported as bogus
   "generated test" outcomes. Fixed by restricting to recognized source
   extensions (`.py`/`.java`/`.kt`) and excluding hidden/`__pycache__` path
   components.

Neither surfaced in the 21 synthetic unit tests written before the real
run — all used `tmp_path` fixtures, which are always absolute paths. The
real, non-fixture run is what found them.

## Storage layout

Same convention as every prior TEP package: no `runs/`-style history
directory, the CLI writes wherever `--out` points (default: stdout). The
real demonstration is committed at `examples/test-validation/`
(`output/validation-report.json`, `example-run.md`).

## Packaging note

`test_validation/` uses the same flat module layout as every prior TEP
package, with the same `[tool.setuptools] packages = ["test_validation"]` /
`[tool.setuptools.package-dir] test_validation = "."` fix applied from the
start. `pyproject.toml`'s `dev` extra pulls in `pytest`, which is also the
runtime dependency actually shelled out to when validating Python test
files — disclosed in the description field, not a hidden coupling.
