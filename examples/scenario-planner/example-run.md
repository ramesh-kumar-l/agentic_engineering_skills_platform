# Scenario Planner — Real Dogfood Run (TEP Phase 5b)

## Setup

Rather than fabricate new inputs, this run reuses the exact real, committed
artifacts from TEP Phase 5a's own dogfood run
([[../test-strategy/example-run.md|test-strategy/example-run.md]]):
the Test Strategy Engine report, the regression-hunter report it was built
from, and the codebase-intelligence report for this platform's own current,
full repository state — all three for the same repo, at the same commit.

## Running the Scenario Planner

```
python -m scenario_planner.cli \
  examples/test-strategy/output/test-strategy-report.json \
  examples/test-strategy/ci-report/regression-hunter-report.json \
  examples/test-strategy/ci-report/report.json \
  --out examples/scenario-planner/output
```

Full output: `output/scenario-plan-report.json` (committed alongside this
write-up). Result:

```json
{
  "stats": {
    "targets_considered": 0,
    "targets_with_structural_detail": 0,
    "targets_missing_structural_detail": 0,
    "scenarios_generated": 0
  },
  "plans": [],
  "warnings": [
    "test-strategy report contained zero flagged targets — nothing to plan scenarios for"
  ]
}
```

## Why this run doesn't show a positive result — and why that's honest, not a bug

This engine is a pure downstream consumer of the Test Strategy Engine's own
`targets` list (TEP Phase 5a's exit criteria and contract). Phase 5a's real
demo already found, and disclosed as
[[../../project-memory-bank/12-known-limitations.md|L36]], that its one real
changed file (`evidence/cli.py`) was suppressed as "already covered" by a
cross-skill identical-stem false positive inherited from regression-hunter
([[../../project-memory-bank/12-known-limitations.md|L24]]). Because that
report legitimately contains zero targets, there is nothing for the Scenario
Planner to plan scenarios for — an honest inherited result, not a new
defect. No new limitation entry is needed: this is the same L24/L36 chain
surfacing one level further downstream, exactly as its own design (trusting
the upstream target list rather than re-deriving it) predicts.

## What the detection logic itself proves

Since this real run's own upstream data cannot exercise the positive path,
`scenario_planner/tests/test_plan_builder.py` proves it directly with
synthetic fixtures — the same "disclose what a real run can't show, prove it
synthetically instead" pattern already established in TEP Phase 4 and 5a:

- a target with a regression-hunter flag gets one scenario per flag, citing
  that flag's own description verbatim (`source: "regression-flag"`);
- a target whose file *is* found in codebase-intelligence's structural
  listing gets one scenario per function and per class in that listing
  (`source: "structural-listing"`), each rationale explicitly stating that no
  line-range data exists to attribute the diff to one specific symbol — every
  symbol is offered as an equally plausible candidate, never a guess;
- a target with no flags and no structural listing gets exactly one
  file-level fallback scenario (`source: "file-level-fallback"`), never a
  fabricated function-level claim;
- a target with flags but no structural listing gets only the flag-grounded
  scenarios — the fallback never doubles up with a real signal;
- priority, `generation_feasible`, and `recommended_framework` are carried
  through unchanged from the Test Strategy Engine's own target — this engine
  computes no risk score and makes no feasibility judgment of its own.

26 tests total (`scenario_planner/tests/`), all passing.

## What this does and does not prove

N=1, self-run, single session — not an inter-rater-agreement experiment.
This run demonstrates: the required test_strategy + regression-hunter +
codebase-intelligence three-way composition executed correctly end-to-end
against this platform's real, current, full repository state; the engine
correctly propagated an upstream zero-target result rather than inventing
scenarios to compensate for it; and the positive "here are this target's
candidate scenarios" path — which this run's own honest upstream data
could not exercise — is proven separately and explicitly via unit tests.
