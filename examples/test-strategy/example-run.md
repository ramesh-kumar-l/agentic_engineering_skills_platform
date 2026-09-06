# Test Strategy Engine — Real Dogfood Run (TEP Phase 5a)

## Setup

A fresh `codebase-intelligence` report was generated against this
platform's current, full repository state:

```
cd skills/codebase-intelligence
python -m engine.cli ../.. --format json --out ../../examples/test-strategy/ci-report
```

`ci-report/report.json` is committed alongside this write-up.

## The real diff

Rather than fabricate a diff, this run uses the actual, historical `git
diff` that introduced `evidence/cli.py` during TEP Phase 2 (commit
`0c136a10`), extracted with:

```
git show --format="" 0c136a10... -- evidence/cli.py > examples/test-strategy/diff.txt
```

This is a real, honest choice of demo file: `evidence/cli.py` genuinely has
**no dedicated test file of its own** even today (it is a thin argparse
wrapper; `evidence/tests/` has no `test_cli.py`) — a real, currently-true
coverage gap in this platform, not a constructed fixture.

## Running the two upstream engines for real

```
cd skills/regression-hunter
python -m engine.cli ../../examples/test-strategy/diff.txt \
  --ci-report ../../examples/test-strategy/ci-report/report.json \
  --format json --out ../../examples/test-strategy/ci-report

cd ../.. 
python -m project_intelligence.cli examples/test-strategy/ci-report/report.json \
  --out examples/test-strategy/ci-report
```

Both outputs are committed: `ci-report/regression-hunter-report.json` and
`ci-report/test-environment-profile.json`.

**regression-hunter's real result** for `evidence/cli.py`: `is_new_file:
true`, one real `diff-pattern` flag fired (`modified-signature-no-test-
change`, severity `medium`), `structural.structural_tier: low` (fan_in=0 —
nothing else in the repo imports this CLI module), `overall_risk_tier:
low`. `test_coverage.test_coverage_modules` came back **non-empty**: nine
unrelated skills' own `tests/test_cli.py` files.

**project_intelligence's real result** for the same repo root: `pytest`
detected as `test_frameworks` (`dependency-confirmed`, since several
packages' `pyproject.toml` declare it under `[project.optional-
dependencies].dev`) — `mock_framework`/`coverage_tool`/
`android_test_framework` all reported `unavailable`.

## Running the Test Strategy Engine

```
python -m test_strategy.cli \
  examples/test-strategy/ci-report/regression-hunter-report.json \
  examples/test-strategy/ci-report/test-environment-profile.json \
  --out examples/test-strategy/output
```

Full output: `output/test-strategy-report.json`. Result:

```json
{
  "stats": {
    "files_considered": 1,
    "files_already_covered": 1,
    "targets_flagged": 0,
    "high_priority_count": 0,
    "medium_priority_count": 0,
    "low_priority_count": 0
  },
  "targets": [],
  "warnings": []
}
```

## Why this run doesn't show a positive "flagged" result — and why that's honest, not a bug

`evidence/cli.py` was **not** flagged, because regression-hunter's own
`test_coverage_modules` for it is non-empty. Inspecting that list shows
nine files — `project_intelligence/tests/test_cli.py`,
`skills/acceptance-test-engineer/tests/test_cli.py`, and seven more — none
of which import or exercise `evidence/cli.py` at all. Each merely has its
*own* skill's `cli.py` in its own dotted import path, and
`test_coverage_scanner.py`'s stem match (`cli`) fires on all of them. This
is a real, new instance of an already-disclosed limitation
([[../../project-memory-bank/12-known-limitations.md|L24]]): the cross-
skill identical-stem false positive that release-readiness's own copy of
this scanner partially fixed but regression-hunter's copy — and now this
engine, by inheriting it — has not. Logged as **L36**.

Per TEP Phase 5a's own contract ("extend, not replace ... do not build a
second, competing risk scorer"), the Test Strategy Engine trusts
regression-hunter's coverage signal as given, rather than re-deriving
coverage itself to work around this. That is the correct scope boundary,
not an oversight — but it means this specific real demo cannot show the
positive "flagged, needs a test" path.

## What the detection logic itself proves

`test_strategy/tests/test_strategy_builder.py` proves the positive path
directly with synthetic fixtures, since this real repo's own current state
cannot supply one honestly:

- a high- or medium-tier, uncovered file is flagged at matching priority,
  citing the exact regression-hunter tier that justified it;
- an already-covered file is never flagged, regardless of tier (the same
  rule that, correctly per its own logic, suppressed this run's real
  target);
- a deleted file is never flagged;
- targets sort high-before-medium-before-low;
- with no test framework detected, `generation_feasible` is `False` with an
  explicit reason — never a guess;
- with a detected framework, it is named exactly in
  `recommended_framework`.

26 tests total (`test_strategy/tests/`), all passing.

## What this does and does not prove

N=1, self-run, single session — not an inter-rater-agreement experiment.
What this run does demonstrate: the required regression-hunter +
project_intelligence composition executed correctly end-to-end against
this platform's real, current, full repository state; the engine correctly
computed zero targets for the one real changed file, for a reason that is
fully traceable to an already-understood upstream limitation rather than a
new defect; and the positive "a file needs a test" path — which this run's
own honest data could not exercise — is proven separately and explicitly
via unit tests, the same "disclose what a real run can't show, prove it
synthetically instead" pattern already established in TEP Phase 4's
Android demonstration.
