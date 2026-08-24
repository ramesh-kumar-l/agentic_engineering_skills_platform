# Release Readiness — Real Dogfood Run

## Setup
A fresh `codebase-intelligence` report was regenerated against this
platform's current, full repository state — now 10 skills — via:

```
cd skills/codebase-intelligence
python -m engine.cli ../.. --format json --out ../../examples/release-readiness/ci-report
```

`ci-report/report.json` is committed alongside this write-up so the run is
reproducible without regenerating it.

## The real diff
Unlike some prior phases' single-fix dogfood diffs, this phase's own build
IS the body of work being assessed — a genuinely fitting target for the
final skill in the Engineering Lifecycle group, whose whole purpose is
judging whether a body of work (not just one diff) is ready to ship. The
real diff was captured by staging (never committing) this phase's actual
new files and diffing the staged tree, then unstaging immediately:

```
git add skills/release-readiness evaluations/release-readiness
git diff --cached -- skills/release-readiness evaluations/release-readiness > examples/release-readiness/diff.txt
git reset -- skills/release-readiness evaluations/release-readiness
```

`diff.txt` (78 files, 3,956 lines added, 0 removed — every file is newly
added, none deleted or modified) is committed alongside this write-up.
Nothing was committed to the real git history at any point — `git status`
confirms `skills/release-readiness/`, `evaluations/release-readiness/`, and
`examples/release-readiness/` all remain untracked at the end of this run.

## Running the skill
```
cd skills/release-readiness
python -m engine.cli ../../examples/release-readiness/diff.txt \
  --ci-report ../../examples/release-readiness/ci-report/report.json \
  --format both --out ../../examples/release-readiness/output
```

## What it found
- `overall_verdict: NOT_READY` — 3 of 78 files landed at `readiness_tier ==
  "blocked"` (all from diff-hygiene flags), 75 at `needs-review`, 0 at
  `clear`.
- **A real, confirmed instance of an already-documented limitation**: the
  `debug-print-leftover` hygiene pattern fired on `engine/cli.py` (4 times)
  and `evaluations/release-readiness/run_evaluation.py` (once). Every one of
  those 5 matches is a legitimate `print()` call that IS this CLI's actual
  intended stdout/stderr output mechanism (`print(f"error: ...", file=sys.stderr)`,
  `print(f"wrote {path}")`, `print(content)`), not a debug leftover.
  `SKILL.md`'s Known Limitations section predicted exactly this failure
  shape before this run ("a legitimate `print()` call in a CLI tool's own
  intended stdout output") — this run confirms it concretely, on this
  skill's own real code, rather than leaving it a hypothetical. Not fixed:
  this is the documented, deliberate boundary between the deterministic
  hygiene table (a lead generator) and the agent's Step 4 judgment
  (category 7, "false-positive check"), the same "leads not verdicts"
  discipline every prior Pattern 2 skill's anti-pattern table has (L7/L11/
  L15/L17/L18).
- `tests/test_hygiene_scanner.py` also triggered 4 hygiene flags
  (`debug-print-leftover`, `todo-blocking-marker` x2,
  `hardcoded-secret-shaped`) — but these matches are inside the test file's
  own fixture `DIFF` string literals (synthetic diff text used to test the
  scanner itself), not real added application code. Same false-positive
  shape as the two files above, for a different, equally expected reason: a
  regex scanner reading a test file's own fixture strings cannot distinguish
  "this text describes a pattern for testing purposes" from "this is a real
  added debug statement."

## A real, disclosed-not-fixed limitation (L24) — a materially new manifestation of L23

Inspecting the 75 `needs-review` files surfaced something more consequential
than the hygiene false positives above: `target_resolver.py`'s
substring/stem-based module resolution — a THIRD independent copy of the
exact heuristic already disclosed as **L23** (`refactoring-safety`'s and
`regression-hunter`'s identical `target_resolver.py`) — produces **false-
positive test coverage**, not just an inflated caller list.

Example: `skills/release-readiness/engine/models.py` resolved with
`fan_in: 13` (structural tier `high`) and `test_coverage.has_coverage:
true`, covered by `skills/architecture-decision/tests/test_impact_scorer.py`
and `skills/architecture-decision/tests/test_stats.py`, among others. But
`release-readiness` has **no `tests/test_models.py` of its own** — every one
of those "covering" test modules belongs to an unrelated skill whose own
`models.py` (or a module importing something named `models`) happens to
share the stem `"models"`. The same pattern repeats for `stats.py`
(`covered` via `acceptance-test-engineer/tests/test_stats.py`),
`report.py` (`covered` via `acceptance-test-engineer/tests/test_report.py`),
`render_json.py`/`render_markdown.py` (`covered` via other skills'
`test_integration.py` files that happen to import their own skill's
identically-stemmed renderer), `ci_report_loader.py`, `target_resolver.py`,
and `test_coverage_scanner.py` — every module in this platform that reuses
Pattern 2's common naming convention for these roles.

This is a new, more consequential category of finding than L23. L23 (found
via `regression-hunter`'s dogfood run) inflated a *caller list* — a field
the report displays but which did not change the eventual risk-tier
outcome in that run. Here, the SAME heuristic (the identical
`target_resolver.py::_find_callers`-style substring match, reused
unmodified inside `test_coverage_scanner.py` as well) produces a **false
"covered" verdict** — the exact signal `readiness_scorer.py`'s rule table
uses to decide whether a structurally consequential file needs closer
review or not. In this specific run the outcome still landed on the
conservative side (`needs-review`, not `clear`, because the inflated
`fan_in`/hotspot signal from the same collision kept the structural tier at
medium/high) — but the mechanism is now shown capable of making a
genuinely untested new module look tested, which is the more dangerous
direction for a skill whose entire purpose is judging release readiness.

Not fixed here, for the same reason L14/L19/L21/L23 were left disclosed
rather than patched: a real fix (requiring a word-boundary or
dotted-segment match instead of a bare substring check, or scoping the
match to the same skill's own `skills/<name>/` path prefix) is a real
design tradeoff against a now-four-times-disclosed limitation class, not
evaluated here against other evidence of need across every skill that
reuses this exact pattern. Logged as **L24** in
`project-memory-bank/12-known-limitations.md`, cross-referencing L23 rather
than treating it as unrelated.

## Outcome
N=1, self-run, single session. Not the inter-rater-agreement experiment
([[16-assumptions-and-validation]] A5) — no independent user has used this
skill yet. What this run does demonstrate: the required
`codebase-intelligence` composition executed correctly end-to-end against
this platform's real, current (10-skill) repository state; the
diff-hygiene scanner's documented "leads not verdicts" boundary was
concretely confirmed on this skill's own real, legitimate `print()` calls
rather than left a hypothetical; and the run surfaced one genuine,
newly-disclosed limitation (L24) — a materially more consequential
manifestation of the L14/L19/L21/L23 substring-collision limitation class,
now shown to produce false-positive test-coverage signals, not just an
inflated caller list, in a THIRD independent copy of the same
`target_resolver.py` pattern. `overall_verdict: NOT_READY` for this
phase's own body of work is the correct, honest outcome — it is not yet
merged, it is not yet reviewed by a human, and the hygiene/coverage
findings above are exactly the kind of material a human reviewer should
see before deciding whether (and with what conditions) to proceed. This
skill's own advisory-only design (Security Constraints) is honored by this
write-up itself: nothing here was auto-committed or auto-released on the
strength of this report.
