# Independent Validation — Real Dogfood Run (TEP Phase 5c, part 2)

## Setup

Continuing directly from
[[../test-generation/example-run.md|test-generation/example-run.md]]'s real
positive run: the agent-authored `test_classify.py` (1 positive + 4 negative
tests, all grounded in `_classify`'s real source) plus a fresh, real
`project_intelligence` test-environment profile for this repo (`pytest`,
dependency-confirmed).

```
python -m project_intelligence.cli \
  <a fresh codebase-intelligence report for this repo root> \
  --out examples/test-generation/synthetic-profile

python -m test_validation.cli \
  examples/test-generation/synthetic-output/generated-tests \
  examples/test-generation/synthetic-profile/test-environment-profile.json \
  . \
  --out examples/test-validation/output
```

Full output: `output/validation-report.json` (committed alongside this
write-up). Result: the real subprocess (`python -m pytest
test_classify.py -q`) actually ran, and actually passed:

```json
{
  "stats": {"test_files_considered": 1, "passed": 1, "failed": 0, "timed_out": 0},
  "outcomes": [
    {
      "test_file": ".../test_classify.py",
      "exit_code": 0,
      "passed": true,
      "stdout_excerpt": ".....                                          [100%]\n5 passed in 0.02s\n"
    }
  ]
}
```

Five test functions ran and passed inside that one file — the 1 positive +
4 negative tests the prior phase's plan requested.

## Two real bugs this dogfood run found and fixed

Neither surfaced in the 21 synthetic unit tests written before this real
run, because every one of them used `tmp_path` fixtures (always absolute
paths). The real run used relative paths, exactly as a caller invoking from
a repo's own root normally would:

1. **Relative `test_file`/`repo_root` resolved against the wrong
   directory.** `run_validation` sets the subprocess's `cwd` to
   `test_file.parent`; a relative test-file path or a `repo_root` of `"."`
   (both entirely normal CLI input) then resolved against that *new* cwd,
   not the caller's original one — the first real run failed outright
   (`file or directory not found`). Fixed by resolving both to absolute
   paths at the top of `run_validation` (`validation_runner.py`), before
   either is used. A regression test
   (`test_relative_test_file_and_repo_root_still_resolve_correctly`)
   exercises exactly this via `monkeypatch.chdir`.
2. **`.pytest_cache/` from the first (failing) run was itself listed as a
   "generated test."** `list_generated_tests`'s `rglob("*")` had no filter,
   so pytest's own cache artifacts from the prior invocation appeared as
   four bogus outcomes. Fixed by filtering to recognized test-source
   extensions (`.py`/`.java`/`.kt`) and excluding any hidden/`__pycache__`
   path component (`generated_tests_loader.py`), with three new unit tests.

Both are logged here rather than silently fixed, per this project's
disclose-don't-hide discipline — the real run is what found them; the
synthetic suite alone would not have.

## What the deterministic logic itself proves

`test_validation/tests/` (24 tests, after the two fixes above) includes real,
non-mocked subprocess execution: an always-passing fixture reports
`passed=True`/`exit_code=0`; an always-failing one reports `passed=False`/
`exit_code=1`; a deliberately slow one is actually killed by the timeout and
reports `timed_out=True`; an unsupported extension (`.java`) returns an
explicit "no supported runner" outcome rather than attempting a build-system
invocation it has no manifest for; and a real cross-file import via
`PYTHONPATH` injection actually resolves and passes.

## Known Limitations (disclosed, not fixed here)

- **No sandboxing beyond a process-level timeout.** This is this platform's
  first execution capability — every other skill and TEP package before
  this one is pure static analysis. Running a generated test here carries
  exactly the same risk as running that file in the target repo's own CI:
  no filesystem or network isolation is added. See
  [[../../project-memory-bank/11-decisions.md|ADR-029]]'s Security field.
- **Only Python (pytest) is actually executed.** A `.java`/`.kt` file is
  recognized as a real candidate but always returns the explicit
  "no supported runner" outcome — a real Maven/Gradle run needs the target
  repo's own build file, out of scope for validating one loose file.

## What this does and does not prove

N=1, self-run, single session. This run demonstrates: the full pipeline
end-to-end on a real symbol in this real repository — plan → agent-authored
file → real subprocess execution → real pass evidence — and that dogfooding
against real (even if relative) paths, rather than only `tmp_path` fixtures,
finds real bugs unit tests alone did not.
