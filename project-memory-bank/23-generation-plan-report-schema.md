# 23 — GenerationPlanReport Schema (TEP Phase 5c, part 1 — Test Generation)

Documents the schema implemented in `test_generation/models.py`, per
[[18-test-engineering-platform-contract]]'s TEP Phase 5c exit criteria: given
a real `scenario_planner` report, produce a deterministic plan naming
exactly which positive + 3–5 negative test slots to author per target —
never authoring the test code inside this engine. See
[[11-decisions|ADR-029]] for the implementation decision.

## Fields

| Field | Source | Rationale |
|---|---|---|
| `schema_version` | constant `"1.0"` | same pattern as every prior TEP report schema |
| `repo_root` | the CLI's `target_repo_root` argument | which real target repo this plan is about |
| `scenario_plan_report_path` | the path passed on the CLI | which upstream input this plan was derived from |
| `naming_convention` | inferred or overridden, see below | applies to every spec in this report |
| `stats` | computed | `scenarios_considered`, `specs_produced`, source-excerpt coverage, total negative slots requested |
| `specs` | computed, one per scenario_planner candidate | see `TargetGenerationSpec` below |
| `warnings` | e.g. zero candidates | explicit disclosure, never a silent empty list |

Each `TargetGenerationSpec` carries:

- `file`, `target_symbol`, `symbol_kind`, `scenario_name`,
  `scenario_rationale`, `scenario_source`, `recommended_framework` — copied
  verbatim from the scenario_planner candidate this spec is for. This engine
  makes no new judgment about which scenarios matter.
- `naming_convention` — the same value as the report-level field, carried
  onto each spec so an agent authoring one file doesn't need to re-reference
  the report root.
- `source_excerpt` / `source_excerpt_available` — a best-effort, bounded
  line-scan of the real source around `target_symbol` (see
  `source_excerpt_reader.py`), or `None` when the file/symbol couldn't be
  found textually. Never a claim of a complete, parser-verified symbol body.
- `positive_slot` — exactly one `GenerationSlot` (`kind: "positive"`)
  instructing the agent to author one happy-path test.
- `negative_slots` — exactly four `GenerationSlot`s (`kind: "negative"`),
  the fixed mid-point of this project's requested 3–5 band, each explicitly
  instructing the agent not to pad with a fabricated case the real excerpt
  can't support.

## What is deliberately excluded (no code authored here)

This engine never writes a `.py`/`.java` test file itself. Deciding what a
plausible negative case even is requires reading real source and reasoning
about it — codebase-intelligence's structural listing carries no parameter/
type/exception data (confirmed by direct inspection of `ModuleInfo` and the
JVM parser during this phase's research), so a Python script cannot derive
real negative conditions from it. That reasoning is the AI-judgment half of
this project's standing deterministic-engine-plus-agent-judgment split
(ADR-005/007) — this engine's entire output is the plan an agent authors
from, not the authored content itself.

## The 3–5 negative-slot band is requested, not fabricated

`generation_planner.py` always requests exactly 4 negative slots (the fixed
mid-point of the user's requested 3–5 band) — but each slot's instruction
text explicitly tells the authoring agent to author *fewer*, with a comment
explaining why, rather than duplicate a case, if the real source excerpt
genuinely can't support that many distinct conditions. The real dogfood run
(`examples/test-generation/example-run.md`) found all four fillable for a
real function with five real branches — no padding was needed there, but
the instruction exists for the case where it would be.

## Naming-convention storage: an explicit config file, not a hidden cache

Two Explore-agent research passes confirmed `project-memory-bank/` is the
wrong place for this (it's this platform's *own* development history — even
`engineering-memory`/`engineering-knowledge-capture` never auto-write
there) and that no existing skill infers or persists a naming convention at
all. The chosen mechanism: `naming_convention.py` infers a convention fresh
each run (majority vote over the target repo's real test files, reusing
regression-hunter's own `test_coverage_scanner.py` file-recognition
heuristic rather than reinventing it), and the resolved value is emitted
into this run's own `--out` report. A later run passes `--naming-convention-
file` pointing at a prior report (or a hand-edited copy) to reuse or
override it — no new hidden cache directory, no state this engine manages
on the caller's behalf, matching this codebase's existing `--out`-only,
explicit-args architecture exactly.

## Storage layout

Same convention as every prior TEP package: no `runs/`-style history
directory, the CLI writes wherever `--out` points (default: stdout). The
real demonstrations are committed at `examples/test-generation/`
(`output/generation-plan-report.json` for the honest-zero real-chain run;
`synthetic-output/generation-plan-report.json` and
`synthetic-output/generated-tests/test_classify.py` for the real-symbol
positive run; `example-run.md`).

## Packaging note

`test_generation/` uses the same flat module layout as every prior TEP
package, with the same `[tool.setuptools] packages = ["test_generation"]` /
`[tool.setuptools.package-dir] test_generation = "."` fix applied from the
start.
