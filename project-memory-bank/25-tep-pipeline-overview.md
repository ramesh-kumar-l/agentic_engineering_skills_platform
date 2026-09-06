# 25 — TEP pipeline overview: how the six packages actually connect

Files 19–24 each document one package's own schema in isolation. None of
them show the whole chain in one place — this file closes that gap. It adds
no new schema and changes no code; it is a reading aid over what
`evidence/`, `project_intelligence/`, `test_strategy/`, `scenario_planner/`,
`test_generation/`, and `test_validation/` already do.

## The pipeline, end to end

```mermaid
flowchart LR
    CI["codebase-intelligence\n(existing skill)"] --> PI["project_intelligence\nTestEnvironmentProfile"]
    CI --> SP["scenario_planner\nScenarioPlanReport"]
    RH["regression-hunter\n(existing skill)"] --> TS["test_strategy\nTestStrategyReport"]
    RH --> SP
    PI --> TS
    TS --> SP
    SP --> TG["test_generation\nGenerationPlanReport"]
    TG -->|"agent authors test files\nguided by the plan"| Files["generated test files\n(not written by any engine)"]
    Files --> TV["test_validation\nValidationReport"]
    PI --> TV

    EV["evidence\nRunProvenance"]
    EV -.wraps any single skill run,\ncaptures provenance,\nnot in the critical path.- CI
    EV -.-.- RH

    style EV fill:#eee,stroke:#999
    style Files fill:#fff3cd,stroke:#b8860b
```

`evidence/` is drawn separately on purpose: per
[[19-evidence-provenance-schema]]'s own Status line, it is "not yet consumed
by any other skill" — it wraps a skill's CLI invocation to record
provenance (which skill/version ran, against which commit, did it succeed),
useful on its own, but not an input any of the other five packages waits on.

## Package → schema → literal command

| Package | Produces (schema file) | Consumes | Literal CLI invocation |
|---|---|---|---|
| `evidence` | `RunProvenance` ([[19-evidence-provenance-schema]]) | any skill's CLI, run as a subprocess | `python -m evidence.cli <skill-name> <target-repo-path>` |
| `project_intelligence` | `TestEnvironmentProfile` ([[20-test-environment-profile-schema]]) | a `codebase-intelligence` `report.json` | `python -m project_intelligence.cli <ci-report.json> [--out DIR]` |
| `test_strategy` | `TestStrategyReport` ([[21-test-strategy-report-schema]]) | a `regression-hunter` report + a `TestEnvironmentProfile` | `python -m test_strategy.cli <regression-hunter-report.json> <test-environment-profile.json> [--out DIR]` |
| `scenario_planner` | `ScenarioPlanReport` ([[22-scenario-plan-report-schema]]) | a `TestStrategyReport` + a `regression-hunter` report + a `codebase-intelligence` `report.json` | `python -m scenario_planner.cli <test-strategy-report.json> <regression-hunter-report.json> <codebase-intelligence-report.json> [--out DIR]` |
| `test_generation` | `GenerationPlanReport` ([[23-generation-plan-report-schema]]) | a `ScenarioPlanReport` + the target repo root | `python -m test_generation.cli <scenario-plan-report.json> <target-repo-root> [--naming-convention-file PATH] [--out DIR]` |
| `test_validation` | `ValidationReport` ([[24-validation-report-schema]]) | agent-authored test files + a `TestEnvironmentProfile` + the target repo root | `python -m test_validation.cli <generated-tests-dir> <test-environment-profile.json> <target-repo-root> [--timeout SECONDS] [--out DIR]` |

## What this pipeline does not do

- **No package authors test code.** `test_generation` produces a
  deterministic *plan* (target file, framework, naming, scenario
  description) — an agent, not the engine, writes the actual test file
  content, per [[11-decisions|ADR-029]]. If a directory of generated test
  files exists, an agent wrote them against `test_generation`'s plan; no
  code path in this repo writes them automatically.
- **No sandboxing beyond what's disclosed.** `test_validation` is this
  platform's only execution capability — it subprocess-runs agent-authored
  files with a timeout, path-containment checks, and resource caps
  ([[11-decisions|ADR-029]], [[11-decisions|ADR-030]]), but that is bounding,
  not sandboxing. Untrusted target repos should not be pointed at this
  pipeline; see ADR-030's Security field for the exact boundary.
- **No risk scoring of its own** in `test_strategy` or `scenario_planner` —
  both compose existing signals from `codebase-intelligence` and
  `regression-hunter` rather than computing a new score
  ([[11-decisions|ADR-027]], [[11-decisions|ADR-028]]).

## Status

Descriptive only — added 2026-09-06 as part of the public-documentation
pass ([[11-decisions|ADR-031]]) after TEP Phase 5d shipped with no single
file showing this chain end to end. See
[[18-test-engineering-platform-contract]] for the phase-by-phase build
history and exit criteria that produced each package.
