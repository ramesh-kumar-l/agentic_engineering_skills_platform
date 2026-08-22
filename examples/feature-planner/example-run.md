# Feature Planner — real dogfood run

Unlike Phases 1–3's synthetic evaluation fixtures, this is a genuine run
against this platform's own current repository state, demonstrating the
required composition with `codebase-intelligence` (ADR-010) end to end —
not a hypothetical.

## Step 1 — Regenerate a fresh codebase-intelligence report

The only existing report (`examples/codebase-intelligence/report.json`) was
generated in Phase 1, before `adversarial-diff-reviewer`,
`acceptance-test-engineer`, and `feature-planner` existed — using it here
would make the relevance scorer's search space artificially empty for any
task touching those newer skills. So a fresh report was generated against
the repo's current state instead:

```
cd skills/codebase-intelligence
python -m engine.cli <repo-root> --format both --out examples/feature-planner/ci-report
```

Output: `examples/feature-planner/ci-report/report.json` (3258 lines) and
`report.md`, covering all four skills now in the repo.

## Step 2 — Run feature-planner against a real task

Task (`examples/feature-planner/task.txt`):

> Only add a --verbose flag to acceptance-test-engineer's CLI that prints
> per-sentence testability flag detail. Verify via a new test that the flag
> prints one line per sentence with its matched flags.

```
cd skills/feature-planner
python -m engine.cli examples/feature-planner/task.txt \
  --ci-report examples/feature-planner/ci-report/report.json \
  --format both --out examples/feature-planner/output
```

**Planning flags**: none — the task states scope ("Only...") and
verification ("Verify via a new test...") explicitly.

**Relevance report** (top of 65 scored modules — see
`examples/feature-planner/output/feature-planning-report.md` for the full
list): the actual target file,
`skills/acceptance-test-engineer/engine/cli.py`, scored 13 and ranked
**13th**, well below several files that scored higher purely because the
task's keywords ("acceptance", "test", "engineer") also appear in the
shared directory name `skills/acceptance-test-engineer/` — every file under
that directory gets the same path-weight bonus regardless of whether it's
actually the right file to change.

## Honesty note — a real limitation, found here, not fixed

This is a genuine, previously-undocumented limitation of the naive
keyword-overlap relevance scorer, not a synthetic fixture claim: **path-based
scoring floods when a task's keywords collide with a shared directory name**
(new limitation, logged as L13 in
`project-memory-bank/12-known-limitations.md`). It was not fixed — the
two-layer architecture (ADR-007) is specifically designed so the
deterministic ranking is a *lead list*, not a verdict, and `SKILL.md`
already instructs the agent not to trust a relevance score alone. This run
is the concrete evidence that design choice matters: Step 3 below correctly
identifies `engine/cli.py` as the actual target despite its middling rank,
using the same judgment the checklist requires.

## Step 3 — Derive the structured plan (real, not fabricated)

**Scope**: Add an opt-in `--verbose` flag to
`skills/acceptance-test-engineer/engine/cli.py` that prints one line per
parsed sentence, showing the sentence text and any testability flags whose
`sentence_index` matches it.

**Non-goals**: does not change the default (non-verbose) report format;
does not add per-sentence detail for the two whole-document absence checks
(`sentence_index` is `None` for those); does not touch any other skill's CLI.

**Affected files** (grounded in Step 2's relevance report, not guessed):
`skills/acceptance-test-engineer/engine/cli.py` — correctly identified
despite ranking 13th, per the honesty note above.

**Steps**:
1. Add a `--verbose` flag to the `argparse` parser in `cli.py`.
2. When set, after building the report, iterate `report.sentences` and
   print each sentence's text plus any `TestabilityFlag` whose
   `sentence_index` matches it (group flags by index first, O(n), rather
   than rescanning per sentence).
3. **`skills/acceptance-test-engineer/tests/test_cli.py` did not exist** —
   this CLI had zero test coverage, the same gap shape as L10
   (`adversarial-diff-reviewer`, Phase 3), found here purely as a side
   effect of grounding this plan's "affected files" against the real
   module list. Fixed in this same session: added 4 tests (nonexistent-path
   exit 1, stdin read, `--out` writes both files, `--format json` writes
   only json) — suite is now 24/24. The `--verbose` feature itself was
   **not** implemented — that is out of scope for `feature-planner`, which
   plans, it does not implement (see `SKILL.md` "When NOT to Use").

**Risk & rollback**: low risk, additive-only change; rollback is deleting
the flag and its printing branch.

**Test hook**: new test asserts `--verbose` output includes one line per
sentence, and that a flagged sentence's line names its `pattern_id`.

**Assumptions**: "per-sentence testability flag detail" is read as
"sentence text + matched pattern id(s), one line each" — the task doesn't
specify an exact format, so this is the simplest reading consistent with
the existing `report.sentences`/`testability_flags` schema; `--verbose` is
assumed additive (extra output), not a replacement for the existing summary.

**Security notes**: none — read-only text processing, no new file/network/
credential access.

## Outcome

Real evidence the required-composition architecture (ADR-010) works: a
fresh `codebase-intelligence` report was genuinely necessary and genuinely
used, the relevance report grounded (if imperfectly ranked) the affected-
files decision, and the planning process itself surfaced and fixed a real
gap in a different skill's test coverage — the second cross-skill dogfood
finding in this project (after L10), and the first time a *planning* skill
(rather than a review/testability skill) found one.
