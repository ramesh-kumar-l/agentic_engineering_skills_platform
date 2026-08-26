# Regression Hunter — Real Dogfood Run

## Setup
A fresh `codebase-intelligence` report was regenerated against this
platform's current, full repository state — now 9 skills — via:

```
cd skills/codebase-intelligence
python -m engine.cli ../.. --format json --out ../../examples/regression-hunter/ci-report
```

`ci-report/report.json` is committed alongside this write-up so the run is
reproducible without regenerating it.

## The real diff
While building this phase, a genuine, small gap was noticed in
`codebase-intelligence`'s own `engine/scanner.py`: `DEFAULT_EXCLUDED_DIRS`
did not exclude `*.egg-info` directories (visible in this repo's own
`skills/refactoring-safety/refactoring_safety.egg-info/` directory, a
byproduct of `pip install -e .`), so a repo scan would walk into and index
generated packaging metadata as if it were real source. This was fixed for
real — `scanner.py`'s directory-exclusion filter now also excludes any
directory ending in `.egg-info` — with a new test
(`tests/test_scan_excludes_egg_info_dirs`) added, and
`codebase-intelligence`'s full suite re-run (24/24 passing, was 23).

The actual `git diff` for this real, already-tested, already-passing change
was captured directly:

```
cd .. && git diff -- skills/codebase-intelligence/engine/scanner.py \
  skills/codebase-intelligence/tests/test_scanner.py \
  > examples/regression-hunter/diff.txt
```

`diff.txt` is committed alongside this write-up. It touches two files: the
scanner logic itself (+4/-1 lines) and its test file (+11/-0 lines, a wholly
new test).

## Running the skill
```
cd skills/regression-hunter
python -m engine.cli ../../examples/regression-hunter/diff.txt \
  --ci-report ../../examples/regression-hunter/ci-report/report.json \
  --format both --out ../../examples/regression-hunter/output
```

## What it found
- Both changed files resolved correctly against the freshly regenerated
  report (`skills/codebase-intelligence/engine/scanner.py` and
  `skills/codebase-intelligence/tests/test_scanner.py`).
- Zero diff-pattern flags fired on either file — correct: the change only
  *adds* a filter condition and a new test; nothing was removed without
  replacement, no exception handling or conditional guard was deleted, no
  large unreplaced deletion occurred, and the test file's assertion count
  only increased.
- `scanner.py` resolved to `structural_tier: medium` (fan_in=1, fan_out=1,
  not itself a hotspot) and `test_scanner.py` resolved to `structural_tier:
  low` (fan_in=0, as expected for a test file nothing else imports).
- Both files' `overall_risk_tier` came back **LOW** — the correct, honest
  outcome for a small, purely additive, already-tested change to a
  moderate-fan-in module.

Full output: `output/regression-hunter-report.json` /
`output/regression-hunter-report.md`.

## A real, disclosed-not-fixed limitation (L23)

`scanner.py`'s Markdown output lists **22 "caller" modules** — every
`report.py`, `*_scanner.py`, and several test files across all nine skills
in this repository, including files with no real relationship to
`codebase-intelligence/engine/scanner.py` at all (e.g.
`skills/architecture-decision/engine/report.py`,
`skills/security-context-guard/tests/test_scanner.py`). This is a false
positive at scale, not a real caller list.

The root cause: `target_resolver.py`'s `_find_callers` resolves
`scanner.py`'s module stem as `"scanner"`, then checks whether that stem
appears as a **substring** anywhere in each candidate module's joined
`imports` text (`target_stem in imports_text`) — the same technique
`refactoring-safety`'s `target_resolver.py` already uses (an independent
copy of the identical heuristic, not a new bug introduced this phase).
`"scanner"` is a substring of `"testability_scanner"`,
`"decision_scanner"`, `"safety_scanner"`, `"regression_scanner"`,
`"symptom_scanner"`, and `"risk_scanner"` — every skill in this platform
that reuses Pattern 2's "scanner" naming convention for its own
anti-pattern-flag module. A module that merely imports its *own* skill's
differently-named scanner (e.g. `acceptance-test-engineer/engine/report.py`
importing `.testability_scanner`) gets counted as a caller of
`codebase-intelligence/engine/scanner.py`, which it has never heard of.

This is the same mechanism class already disclosed as L14 (`feature-
planner`'s relevance scorer), L19 (`root-cause-analyzer`'s keyword tier),
and L21 (`architecture-decision`'s blast-radius scorer) — coincidental
substring collision at repository scale — but it is the first time the
collision appears in **structural caller identification** (Axis 2) rather
than a keyword-relevance ranking, and the first time it is demonstrated to
affect two skills at once: `refactoring-safety`'s `target_resolver.py` and
`regression-hunter`'s `target_resolver.py` share the exact same
vulnerability, because the second is an independent copy of the first's
resolution pattern (per this project's stdlib-only, no-cross-package-import
portability discipline — see ADR-010's lineage). In this specific dogfood
run the false positives did not change the `overall_risk_tier` outcome
(structural tier is driven by `fan_in`/hotspot status from the real
`codebase-intelligence` graph, not by the length of `caller_modules`), but
the `caller_modules` list itself — which the agent's Step 3 workflow is
explicitly instructed to read alongside `fan_in` (see `SKILL.md`'s Agent
Responsibilities) — is materially misleading for any module whose stem is a
short, common word.

Not fixed here, for the same reason L14/L19/L21 were left disclosed rather
than patched: a real fix (e.g. requiring a word-boundary or dotted-segment
match instead of a bare substring check, or a minimum stem length) is a
real design tradeoff against a currently-understood, now-twice-disclosed
limitation, not evaluated here against other evidence of need. Logged as
**L23** in `project-memory-bank/12-known-limitations.md`.

## Outcome
N=1, self-run, single session. Not the inter-rater-agreement experiment
([[16-assumptions-and-validation]] A5) — no independent user has used this
skill yet. What this run does demonstrate: the required
`codebase-intelligence` composition executed correctly end-to-end against
this platform's real, current (9-skill) repository state; a real,
already-tested, already-passing improvement to `codebase-intelligence`
itself was correctly assessed as low-risk on both axes that matter (no
diff-pattern flags, no structural escalation); and the run surfaced one
genuine, disclosed limitation (L23) shared across two skills' independent
copies of the same caller-resolution heuristic — the same "a purely
synthetic fixture, authored by the same session that would have to notice
the gap to test for it, structurally could not have surfaced this" pattern
already established by L14/L16/L19/L21/L22 in prior phases.
