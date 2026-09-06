# 21 — TestStrategyReport Schema (TEP Phase 5a — Test Strategy Engine)

Documents the schema implemented in `test_strategy/models.py`, per
[[18-test-engineering-platform-contract]]'s TEP Phase 5a exit criteria:
given a real `regression-hunter` report.json and a real `project_intelligence`
test-environment-profile.json for the same target repo, decide which
changed files need a regression test — by **reusing** both engines'
existing signals, never re-deriving risk or environment detection. See
[[11-decisions|ADR-027]] for the implementation decision.

## Fields

| Field | Source | Rationale |
|---|---|---|
| `schema_version` | constant `"1.0"` | same pattern as [[19-evidence-provenance-schema]] and [[20-test-environment-profile-schema]] |
| `repo_root` | the input profile's `repo_root` | which real target this report is about |
| `regression_report_path` / `profile_path` | the paths passed on the CLI | which two inputs this report was derived from — makes the derivation re-checkable |
| `stats` | computed | `files_considered`, `files_already_covered`, `targets_flagged`, and a count per priority tier |
| `targets` | computed, one per flagged file | see `TestTarget` below |
| `warnings` | e.g. zero changed files | explicit disclosure, never a silent empty list |

Each `TestTarget` carries:

- `file` — the changed file's path, copied verbatim from the regression-
  hunter report.
- `priority` — copied **directly** from regression-hunter's own
  `overall_risk_tier` string (`"high"|"medium"|"low"`) for that file. This
  engine computes no risk score of its own; a file with `overall_risk_tier:
  "low"` still appears here (as a low-priority, informational note) if it
  has no test coverage, so the absence of coverage is never silently
  dropped just because the risk happens to be low.
- `reason` — a fixed, tier-keyed sentence naming the exact regression-hunter
  signal that produced this target (never a freeform or model-generated
  explanation).
- `risk_tier` — the same value as `priority`, kept as a separate field so a
  future priority scheme (e.g. weighting by flag count too) cannot silently
  lose track of which regression-hunter tier justified the entry.
- `generation_feasible` — `True` only if the input `TestEnvironmentProfile`
  named at least one detected test framework; `False` otherwise, with
  `feasibility_note` explaining why and pointing at the profile's own
  `unavailable` list — **never a guess** that, say, pytest is available
  just because the target looks like a Python repo.
- `recommended_framework` — the exact detected framework name, or `None`
  when infeasible.

## What is deliberately excluded (filtering, not scoring)

A file is **dropped entirely** — never appears in `targets` — if
regression-hunter's `test_coverage.test_coverage_modules` is non-empty for
it, regardless of tier, and if `is_deleted_file` is true (nothing to test
in a file that no longer exists). Both are direct pass-throughs of
regression-hunter's own fields; this engine adds no additional filtering
logic beyond these two, matching the contract's "do not build a second,
competing risk scorer" mandate literally.

## A real, disclosed limitation this design inherits (L36)

Because `targets` filtering trusts regression-hunter's
`test_coverage_modules` signal as-is, it also inherits that signal's own
already-disclosed limitation ([[12-known-limitations|L24]]): a module whose
stem is a common name shared across unrelated skills (e.g. `cli`, `models`,
`report`) can be reported as "covered" by a completely unrelated test file
that merely shares the same stem in its own dotted import path. The real
demonstration run in `examples/test-strategy/example-run.md` hits this
exact case — logged as [[12-known-limitations|L36]] rather than silently
worked around, since fixing it would mean re-deriving coverage detection,
which this phase's contract explicitly rules out.

## Storage layout

Same convention as `evidence/` and `project_intelligence/`: no `runs/`-
style history directory, the CLI writes wherever `--out` points (default:
stdout). The real demonstration is committed at
`examples/test-strategy/` (`ci-report/regression-hunter-report.json`,
`ci-report/test-environment-profile.json`, `diff.txt`,
`output/test-strategy-report.json`, `example-run.md`), following
`examples/project-intelligence/`'s exact precedent.

## Packaging note

`test_strategy/` uses the same flat module layout as `evidence/` and
`project_intelligence/`, with the same `[tool.setuptools] packages =
["test_strategy"]` / `[tool.setuptools.package-dir] test_strategy = "."`
fix already established by ADR-025, applied from the start this time
rather than found after the fact.
