# 20 — TestEnvironmentProfile Schema (TEP Phase 3 — Project Intelligence extensions; extended by TEP Phase 4 — Android/JVM Test Environment Discovery)

Documents the schema implemented in `project_intelligence/models.py`, per
[[18-test-engineering-platform-contract]]'s TEP Phase 3 exit criteria: a
`TestEnvironmentProfile`-equivalent (language, build system, test
framework, mocking framework, coverage tool availability) derived from a
real target repo, built by **extending** `codebase-intelligence`'s
existing `external_dependencies` (and, for build systems only, `files`)
output, never by re-parsing manifests a second time. See
[[11-decisions|ADR-025]] for the implementation decision.

## Fields

| Field | Source | Rationale |
|---|---|---|
| `schema_version` | constant `"1.0"` | same pattern as [[19-evidence-provenance-schema]]'s `RunProvenance` |
| `repo_root` | `report["root_path"]` | which real target the profile is about |
| `ci_report_path` | the path passed on the CLI | which codebase-intelligence report this profile was derived from — makes the derivation itself re-checkable |
| `primary_language` | `max(language_breakdown, key=count)` | the exit criteria names "language" as a single field; ties are broken by dict iteration order and disclosed as a simplification, not hidden |
| `language_breakdown` | `report["language_breakdown"]`, carried through unchanged | full picture, not just the one primary language |
| `build_systems` | `external_dependencies[].source_file` (strong) or `files[]` top-level filename presence (weak) | see confidence tiers below |
| `test_frameworks` | `external_dependencies[].name` matched against `signatures.py`'s `TEST_FRAMEWORK_SIGNATURES` | direct reuse of existing dependency output, per the exit criteria's own wording |
| `mock_frameworks` | same, against `MOCK_FRAMEWORK_SIGNATURES` | ” |
| `coverage_tools` | same, against `COVERAGE_TOOL_SIGNATURES` | ” |
| `android_test_frameworks` | same `external_dependencies[].name`, matched against `ANDROID_TEST_FRAMEWORK_SIGNATURES` | TEP Phase 4 — the named JUnit/Robolectric/Espresso trio, kept as its own category rather than merged into `test_frameworks` (see below) |
| `android_frameworks_absent` | `{"JUnit","Robolectric","Espresso"} - {f.name for f in android_test_frameworks}` | explicit, individually-named absence — never inferred, never a guess |
| `unavailable` | any of the five categories above with zero findings | explicit disclosure, never a silent empty list indistinguishable from "not checked" |
| `warnings` | e.g. zero `external_dependencies` at all | points at the specific known limitation (L2, L34) that explains *why* a real repo can under-report, rather than leaving the reader to guess |

Each finding (`Finding`) carries `name`, `evidence` (the real dependency
names or filename that produced it), and `confidence`:

- **`dependency-confirmed`**: at least one `ExternalDependency` entry
  actually named this tool/library.
- **`manifest-only`**: a known manifest filename (e.g. `pyproject.toml`)
  is present in codebase-intelligence's `files` list, but zero dependency
  entries came from it — either the manifest genuinely declares none
  (this repo's own skills, by ADR-006 design), or it declares some that
  `external_deps.py` doesn't parse (L34). The profile cannot distinguish
  these two cases from `external_dependencies` output alone, and says so
  in `warnings` rather than picking one.

## Detection scope (deliberately bounded)

`signatures.py` covers general-purpose Python (pytest/nose/unittest2),
JS/TS (Jest/Mocha/Jasmine/AVA/Vitest, Sinon), and JVM (JUnit/TestNG,
Mockito/EasyMock/PowerMock, JaCoCo) ecosystems only. Matching is **exact-key
only** against a dependency's full name or its Maven/Gradle artifact-id
(the part after the last `:`) — never substring containment, specifically
to avoid `pytest-mock` partially matching a `pytest` signature key.

**Deliberately excluded from Phase 3, added by TEP Phase 4**: Android-
specific test frameworks (JUnit/Robolectric/Espresso). Implemented as
`ANDROID_TEST_FRAMEWORK_SIGNATURES`, a dedicated table feeding the
dedicated `android_test_frameworks`/`android_frameworks_absent` fields
above, rather than merged into the general-purpose tables — the exit
criteria asks about three specific named frameworks individually, which a
category-level flag alone would not surface. AGP (build-tool/plugin
detection) and source-set/variant awareness remain out of scope — not named
in Phase 4's own exit criteria sentence, only in the contract's broader,
not-yet-scoped "Scope for TEP Phase 2 onward" list.

**TEP Phase 4's real finding**: on every real Android repo hand-checked
during this phase, `android_test_frameworks` comes back empty even though
the frameworks are genuinely declared in source — because Android/Gradle
projects almost universally externalize dependency versions via variable
interpolation, `ext`/`deps` properties objects, or version catalogs, none
of which `external_deps.py`'s literal-string-only Gradle regex (L33)
resolves. Logged as [[12-known-limitations|L35]]; demonstrated end-to-end
in `examples/project-intelligence/android-example/example-run.md`; the
detection logic's correctness (once given matching data) is proven
separately via synthetic fixtures in
`project_intelligence/tests/test_android_detection.py`.

## Storage layout

Unlike `evidence/`'s per-run history (`evidence/runs/<skill>/<run_id>.json`,
gitignored), a `TestEnvironmentProfile` is not a repeated, timestamped
event — it's a derived snapshot of one target repo at one
codebase-intelligence report's time. No `runs/`-style directory or
`.gitignore` entry was added; the CLI writes wherever `--out` points
(default: stdout), matching `feature-planner`'s own CLI convention exactly.
The real demonstration run is committed at
`examples/project-intelligence/` (both the input `ci-report/report.json`
and the output `test-environment-profile.json`), following
`examples/feature-planner/`'s exact precedent. TEP Phase 4's Android
demonstration is a separate, parallel run at
`examples/project-intelligence/android-example/` (same input/output shape),
kept distinct rather than overwriting Phase 3's example since the two runs
target different real repos and prove different things.

## Packaging note (applies to `evidence/` too)

Both `evidence/` and `project_intelligence/` use a flat module layout
(`.py` files directly under the package directory, not nested under an
`engine/` subfolder like every skill uses). Setuptools' automatic package
discovery cannot resolve that layout unambiguously — a clean `pip install
-e ".[dev]"` fails with "Multiple top-level modules discovered." Fixed in
both packages' `pyproject.toml` with an explicit
`[tool.setuptools] packages = ["<name>"]` /
`[tool.setuptools.package-dir] <name> = "."` declaration, found and fixed
during this phase's implementation (both packages' CI jobs would otherwise
fail on a real clean checkout — see [[11-decisions|ADR-025]]).
