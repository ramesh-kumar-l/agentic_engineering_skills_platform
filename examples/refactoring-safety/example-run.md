# Refactoring Safety — Real Dogfood Run

## Setup
A fresh `codebase-intelligence` report was regenerated against this
platform's current, full repository state — now 8 skills — via:

```
cd skills/codebase-intelligence
python -m engine.cli ../.. --format json --out ../../examples/refactoring-safety/ci-report
```

`ci-report/report.json` is committed alongside this write-up so the run is
reproducible without regenerating it.

## The real decision
This phase's own build produced two modules
(`skills/refactoring-safety/engine/target_resolver.py` and
`skills/refactoring-safety/engine/test_coverage_scanner.py`) that each
independently derive a module's path stem via
`PurePosixPath(path).stem` — a small, real duplication introduced during
this phase's own implementation, not an invented example. `refactor.txt`
states the actual refactor this duplication suggests:

> Extract the path-stem helper duplicated across `target_resolver.py` and
> `test_coverage_scanner.py` in the refactoring-safety engine into a shared
> module, and update both call sites to import it instead of repeating the
> `PurePosixPath(path).stem` logic inline.

## Running the skill
```
cd skills/refactoring-safety
python -m engine.cli ../../examples/refactoring-safety/refactor.txt \
  --ci-report ../../examples/refactoring-safety/ci-report/report.json \
  --format both --out ../../examples/refactoring-safety/output
```

## What it found
- `operation_type` correctly detected as `extract` (not the generic
  `refactor` fallback), from the phrase "Extract the path-stem helper."
- Both targets (`target_resolver.py`, `test_coverage_scanner.py`) resolved
  by module-stem match to their real paths inside
  `skills/refactoring-safety/engine/`.
- Both targets scored `risk_tier: low` — correct: `extract` is an
  internal-structure-only operation, and neither module is a
  `codebase-intelligence` hotspot.
- Both targets came back genuinely test-covered
  (`tests/test_target_resolver.py`, `tests/test_test_coverage_scanner.py`
  each import their respective module).
- Three safety flags fired: `no-test-plan-signal`, `no-rollback-signal`,
  `no-verification-signal` — accurate. The refactor description above,
  written the way an engineer would actually phrase a quick internal
  cleanup, never states how it will be tested, whether it's reversible, or
  how success will be confirmed. It should have.

Full output: `output/refactoring-safety-report.json` /
`output/refactoring-safety-report.md`.

## A real, disclosed-not-fixed limitation (L22)
Both targets' Markdown output lists **two** caller modules each — the
engine's own `report.py` (a real relative-import caller) and their
respective test files (real callers via `engine.target_resolver`/
`engine.test_coverage_scanner`-style absolute imports). But
`codebase-intelligence`'s own `dependency_graph.fan_in` for
`target_resolver.py` reports **1**, not 2:

```
fan_in target_resolver.py: 1
```

Checking why: `codebase-intelligence`'s dependency-graph builder only
constructed a `DependencyEdge` for `report.py`'s relative import
(`.target_resolver`) — the test file's absolute-style import
(`engine.target_resolver`) was not recognized as an edge into the same
graph, even though it's a real caller. This engine's own
`target_resolver.py::_find_callers` finds both callers correctly, because
it does its own independent substring scan over each module's raw
`imports` list rather than trusting `codebase-intelligence`'s pre-built
`fan_in` count — but `safety_scorer.py`'s risk-tier calculation uses the
authoritative `fan_in` number (1), not the length of `caller_modules` (2),
for scoring risk. In this specific case the discrepancy didn't change the
outcome (an `extract` operation on a non-hotspot module stays `low` risk
either way), but on a **boundary-changing** operation
(rename/delete/move/change-signature) where the threshold sits right at
the fan_in boundary, this gap could under-score a target's real risk tier
by one caller.

This is not fixed here — it is `codebase-intelligence`'s own dependency-
graph construction that undercounts absolute-style cross-package imports as
edges (a different skill's concern, out of scope for this phase to
silently patch), and this engine's `caller_modules` list already surfaces
the full picture separately for a human/agent to notice. Logged as **L22**
in `project-memory-bank/12-known-limitations.md` — a sharper, differently-
shaped instance of the same "the deterministic layer's number and the
deterministic layer's own detailed list can silently disagree" class of
gap already seen in this project (though this is the first time the
disagreement traces back to a **different** skill's report, not this
skill's own scoring logic).

## Outcome
N=1, self-run, single session. Not the inter-rater-agreement experiment
([[16-assumptions-and-validation]] A5) — no independent user has used this
skill yet. What this run does demonstrate: the required
`codebase-intelligence` composition executed correctly end-to-end against
this platform's real, current (8-skill) repository state, every claim in
the output traces to real structural data (not fabricated), and the run
surfaced one genuine, disclosed cross-skill limitation (L22) that a purely
synthetic fixture — authored by the same session that would have to notice
the gap to test for it — structurally could not have surfaced, the same
pattern already established by L14/L16/L19/L21 in prior phases.
