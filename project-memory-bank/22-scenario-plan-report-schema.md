# 22 — ScenarioPlanReport Schema (TEP Phase 5b — Scenario Planner)

Documents the schema implemented in `scenario_planner/models.py`, per
[[18-test-engineering-platform-contract]]'s TEP Phase 5b exit criteria:
given a real `test_strategy` report.json, the `regression-hunter` report.json
and `codebase-intelligence` report.json it was derived from (same repo),
propose candidate test scenarios for each flagged target — grounded in
existing signals only, never a new risk score, never a guess about which
specific function a diff touched. See [[11-decisions|ADR-028]] for the
implementation decision.

## Fields

| Field | Source | Rationale |
|---|---|---|
| `schema_version` | constant `"1.0"` | same pattern as [[19-evidence-provenance-schema]], [[20-test-environment-profile-schema]], [[21-test-strategy-report-schema]] |
| `repo_root` | the input test-strategy report's `repo_root` | which real target this report is about |
| `test_strategy_report_path` / `regression_report_path` / `ci_report_path` | the paths passed on the CLI | which three inputs this report was derived from — makes the derivation re-checkable |
| `stats` | computed | `targets_considered`, structural-detail coverage counts, `scenarios_generated` |
| `plans` | computed, one per test-strategy target | see `TargetScenarioPlan` below |
| `warnings` | e.g. zero flagged targets | explicit disclosure, never a silent empty list |

Each `TargetScenarioPlan` carries:

- `file`, `priority`, `generation_feasible`, `recommended_framework` — copied
  verbatim from the test_strategy target this plan is for. This engine
  computes no priority or feasibility judgment of its own.
- `structural_detail_available` — `True` only if `file` was found in the
  codebase-intelligence report's `modules` listing.
- `scenarios` — a list of `ScenarioCandidate`, described below.

Each `ScenarioCandidate` carries:

- `scenario_name` — a short, fixed-template description (e.g. `"exercise
  function `foo`"`), never freeform or model-generated text.
- `symbol_kind` — `"function"`, `"class"`, or `"file"`.
- `target_symbol` — the specific function/class name, or `None` for a
  file-level scenario.
- `rationale` — the exact signal that justifies this scenario: a
  regression-hunter flag's own `description` field verbatim, or a sentence
  naming which structural listing this symbol came from and disclosing that
  no line-range data exists to attribute the diff to it specifically.
- `source` — `"regression-flag"`, `"structural-listing"`, or
  `"file-level-fallback"` — which of the two upstream signals (or neither)
  produced this candidate.

## What is deliberately excluded (no scoring, no line-level attribution)

This engine never computes a risk score, never re-ranks targets, and never
claims to know which function or class a diff actually touched. Codebase-
intelligence's `ModuleInfo` carries no line-range fields (confirmed by
direct inspection during this phase's research), so a changed diff line
cannot be cross-referenced to a specific function's body — deliberately
scoped out rather than approximated. When a file has a structural listing,
**every** function and class in it becomes one candidate scenario, each
rationale stating this limitation explicitly, rather than the engine
guessing at a single "most likely" symbol.

## Two signals, composed, not blended

A target's scenarios are the union of whatever "regression-flag" and
"structural-listing" candidates apply — never a choice between them. The
file-level fallback fires only when **neither** signal produced anything
(no flags recorded for the file, and the file absent from the modules
listing), so a target is never left with zero scenarios, and the fallback
never doubles up alongside a real signal.

## An inherited limitation, by design (extends L24/L36, no new entry needed)

Because this engine trusts the test_strategy report's `targets` list as
given, any real run whose upstream Test Strategy Engine result was
suppressed by [[12-known-limitations|L24]]/[[12-known-limitations|L36]]'s
cross-skill identical-stem false-positive inherits that same empty result
one level further downstream — demonstrated directly in
`examples/scenario-planner/example-run.md`. This is the same disclosed
limitation surfacing again, not a new failure mode, so no new limitation
entry was logged for it.

## Storage layout

Same convention as `evidence/`, `project_intelligence/`, and
`test_strategy/`: no `runs/`-style history directory, the CLI writes
wherever `--out` points (default: stdout). The real demonstration is
committed at `examples/scenario-planner/` (`output/scenario-plan-report.json`,
`example-run.md`), reusing the exact committed inputs from
`examples/test-strategy/` rather than duplicating them.

## Packaging note

`scenario_planner/` uses the same flat module layout as `evidence/`,
`project_intelligence/`, and `test_strategy/`, with the same
`[tool.setuptools] packages = ["scenario_planner"]` /
`[tool.setuptools.package-dir] scenario_planner = "."` fix applied from the
start.
