# Test Generation — Real Dogfood Run (TEP Phase 5c, part 1)

## Setup: the honest inherited-zero-result run

Reusing the exact real, committed scenario_planner output from TEP Phase 5b's
own dogfood run
([[../scenario-planner/example-run.md|scenario-planner/example-run.md]]),
against this platform's own repo root.

```
python -m test_generation.cli \
  examples/scenario-planner/output/scenario-plan-report.json \
  . \
  --out examples/test-generation/output
```

Full output: `output/generation-plan-report.json` (committed alongside this
write-up). Result:

```json
{
  "stats": {
    "scenarios_considered": 0,
    "specs_produced": 0,
    "specs_with_source_excerpt": 0,
    "negative_slots_requested": 0
  },
  "specs": [],
  "warnings": [
    "scenario-plan report contained zero candidate scenarios — nothing to plan test generation for"
  ]
}
```

Same reason as every downstream consumer of this chain so far: the upstream
scenario-plan report has zero candidates because *its* upstream test-strategy
report has zero targets — the same
[[../../project-memory-bank/12-known-limitations.md|L24/L36]] chain
surfacing one level further downstream, not a new defect. No new limitation
entry is needed (see [[../../project-memory-bank/11-decisions.md|ADR-029]]).

## Setup: the real positive run

Because the real chain above cannot exercise the positive path, this run
uses a synthetic-but-real scenario-plan-report.json (hand-authored, shaped
exactly like a real scenario_planner output) that names one real symbol in
this actual repository: `test_generation/naming_convention.py`'s `_classify`
function.

```
python -m test_generation.cli \
  examples/test-generation/synthetic-scenario-plan-report.json \
  . \
  --out examples/test-generation/synthetic-output
```

Full output: `synthetic-output/generation-plan-report.json` (committed
alongside this write-up). The naming convention was inferred (not
overridden) from this repo's own real test files — `test_*.py`, correctly
the majority pattern across every `skills/*/tests/` directory. The source
excerpt is the real text of `_classify` and the two functions after it (a
40-line bounded window, not a real parser — see Known Limitations below).
The plan requested 1 positive slot + 4 negative slots (this project's
requested 3–5 band), each carrying an explicit instruction not to fabricate
cases the real excerpt can't support.

## What an agent authored from that plan

`synthetic-output/generated-tests/test_classify.py` (committed) — one
positive test (`test_*.py` convention, matched) plus four negative tests,
each grounded in a real, distinct branch visible in the excerpt (an
unrecognized filename; a Java-suffix stem with the wrong extension; a
Python-prefix stem with the wrong extension; a Kotlin-only suffix with the
wrong extension). All four negative slots were genuinely fillable from the
real excerpt — no padding was needed to reach the requested count, and the
file's own docstring says so.

This authoring step happened in-session, by the agent reading the plan and
the real source — never by `test_generation`'s own deterministic code,
per this phase's core design decision (see ADR-029).

## What the deterministic logic itself proves

`test_generation/tests/` (30 tests) proves the composition mechanism
directly: 1 positive + 4 negative slots per candidate; naming convention and
scenario fields carried through unchanged; source-excerpt availability
tracked per spec and in aggregate stats; a zero-candidate input warns and
produces no specs, never a fabricated one.

## What this does and does not prove

N=1, self-run, single session. This run demonstrates: the required
scenario_planner composition executed correctly end-to-end against this
platform's real, current repository state (both the honest-zero and the
real-symbol runs); the naming-convention inference correctly read this
real repo's own test-file majority pattern; and the full positive path —
plan → real agent-authored file → (next) real execution — is exercised on
a real symbol in this real repository, not a fixture standing in for one.
See [[../test-validation/example-run.md|test-validation/example-run.md]]
for the execution half.

## Known Limitations

- `source_excerpt_reader.py` is a bounded line-scan, not a real parser —
  the excerpt above visibly spills a few lines into the *next* function
  after `_classify`, because it has no brace/indent-depth awareness. "A
  hint, not ground truth," same standard as `jvm_parser.py`.
- Naming-convention inference is a majority vote over this repo's *entire*
  tree — a repo mixing multiple genuinely different conventions in
  different subtrees gets one convention for all of it, not a per-directory
  one. Not exercised by either run above (this repo is Python-uniform).
