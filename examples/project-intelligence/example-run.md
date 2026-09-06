# Project Intelligence — real dogfood run

TEP Phase 3's exit criteria ([[18-test-engineering-platform-contract]])
requires a `TestEnvironmentProfile`-equivalent "derived from a real target
repo," built by extending `codebase-intelligence`'s existing dependency
output rather than re-parsing manifests separately. This is that real,
non-fixture run.

## Step 1 — Generate a fresh codebase-intelligence report

Target: `skills/codebase-intelligence` itself — a real, current directory
in this repo, not a synthetic fixture.

```
cd skills/codebase-intelligence
python -m engine.cli . --format json --out ../../examples/project-intelligence/ci-report
```

Output: `examples/project-intelligence/ci-report/report.json`.

## Step 2 — Derive the TestEnvironmentProfile

```
cd project_intelligence
python -m project_intelligence.cli ../examples/project-intelligence/ci-report/report.json \
  --out ../examples/project-intelligence/output
```

Output: `examples/project-intelligence/output/test-environment-profile.json`.

## Result and hand-verification

- `primary_language: "python"` — matches `language_breakdown` (19 python
  files vs. 1 toml, 2 markdown), hand-counted against the target directory.
- `build_systems`: one finding, `"python (pyproject.toml)"`, confidence
  `"manifest-only"`. Verified: `skills/codebase-intelligence/pyproject.toml`
  really exists and really declares `dependencies = []` — zero runtime
  dependencies, by design (ADR-006, stdlib-only). The finding is correctly
  downgraded to manifest-only rather than claimed as dependency-confirmed,
  because there is genuinely no dependency to confirm it with.
- `test_frameworks` / `mock_frameworks` / `coverage_tools`: all empty,
  listed in `unavailable`. This is **honest, not a detection failure**: the
  skill's `pyproject.toml` does declare `dev = ["pytest>=7.0"]`, but under
  `[project.optional-dependencies]`, a table `external_deps.py` does not
  parse (it only reads `[project.dependencies]`) — a real, pre-existing gap
  surfaced by this exact run, now logged as
  [[12-known-limitations|L34]]. Per this project's disclose-don't-hide
  discipline, the profile reports "unavailable" rather than silently
  missing pytest without a trace, or guessing it's present because the
  language is Python.
- A `warnings` entry explains the zero-dependency case, pointing at
  L2 (root-only manifest scan) and L34 (optional-dependencies gap) as the
  two known reasons a real repo can under-report here.

## Why this run doesn't show a positive detection

Every skill in this repo is deliberately stdlib-only (ADR-006) — there is
no real target *inside this repo* with a non-empty, parseable dependency
list to positively detect against. The detection logic itself (pytest vs.
pytest-mock disambiguation, Maven/Gradle `group:artifact` coordinate
matching, coverage-tool signatures) is exercised and proven correct by
`project_intelligence/tests/test_detect.py`'s 8 cases against real
framework names (`pytest`, `pytest-mock`, `pytest-cov`,
`org.mockito:mockito-core`) — this dogfood run's job is proving the
end-to-end wiring against genuine `codebase-intelligence` output is honest,
not fabricating a positive result this repo doesn't actually have.

## What this does and does not prove

**Proves**: the profile is derived entirely from `codebase-intelligence`'s
already-produced `language_breakdown`, `external_dependencies`, and `files`
fields — no manifest was re-read or re-parsed by this package — and every
field in the output is either backed by real evidence or explicitly marked
`unavailable`.

**Does not prove**: that the detected frameworks (when present) are the
*correct* ones a human would pick, or that "unavailable" always means
"absent" rather than "not representable by the current
`external_dependencies` output" (see L34). Same boundary Phase 2 already
drew for run-provenance: this is evidence of what was derived, never a
claim of completeness or usefulness.
