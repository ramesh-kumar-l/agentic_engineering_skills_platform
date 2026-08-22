# 17 — Experiment A/B Viability Check (Phase 3)

Phase 3's exit criteria explicitly asks for a first check of whether
Experiment A and Experiment B ([[01-product-thesis]]) are viable to run, now
that 3 skills exist. This file is that check — an honest viability
assessment plus two clearly-labeled, non-rigorous internal pilots. It is
**not** Experiment A or B themselves. Do not cite this file anywhere as
evidence those experiments have been "run" — see ADR-009 in
[[11-decisions]] for why pilots and experiments must never be conflated.

## What Experiment A and B actually require

- **Experiment A**: engineer + normal AI workflow vs. engineer + skill, on
  matched real tasks, measuring Time-to-Correct-Result, defects, rework,
  review findings, test quality, satisfaction.
- **Experiment B**: normal AI vs. individual skill vs. composed workflow, to
  test whether composition adds value over either alone.

Both require: a real task (not synthetic), a real comparison condition
(ideally an external engineer, or at minimum two independent runs), and a
measurement of outcome quality/time — none of which a single agent session
authoring both sides of the comparison can honestly supply.

## Experiment A viability: NOT YET VIABLE to run rigorously

Missing: an external engineer (or any second, independent party) to supply
the "normal AI workflow" condition without knowledge of the skill's expected
answer; a real task with pre-existing stakes (not invented for the pilot); a
Time-to-Correct-Result measurement across two genuinely separate attempts.
This session cannot supply any of the three — proceeding to run "Experiment
A" here would produce a number that looks like evidence but isn't.

### Pilot A (not Experiment A) — N=1, self-run, un-blinded

Task: define what "add a `--version` flag to the engine CLI, working without
the required positional path argument" actually requires, once via
`acceptance-test-engineer`, once by just reasoning about it directly.

- **Via the skill**: Step 1 flagged `no-error-handling-signal` and
  `no-boundary-signal` (expected — no error/boundary concept in this
  requirement). Step 3 derived a happy-path case (`--version` alone prints
  the version and exits 0) and an explicit assumption-flag case: the
  requirement doesn't say how `--version` should interact with other flags,
  so that interaction is not assumed silently.
- **Via direct reasoning (no skill)**: the natural next step is simply
  `parser.add_argument("--version", action="version", version=...)` — no
  pause to ask what happens when it's combined with other flags/the
  positional argument.
- **What actually happened when checked**: `argparse`'s built-in
  `action="version"` already bypasses the required positional argument and
  exits 0 — verified by directly running a 6-line Python snippet, not by the
  skill (which correctly refused to assume this, per its "no runtime
  execution" limitation, L9 in [[12-known-limitations]]).
- **Pilot finding**: the skill's category-10 discipline (never silently
  resolve an assumption) surfaced a real design question that direct,
  unstructured reasoning would likely have skipped past. In this instance the
  question resolved in the implementer's favor (argparse already handles it)
  — so the skill's value here was making an implicit assumption explicit and
  checkable, not catching an actual defect. **N=1. Not generalizable. Not a
  substitute for Experiment A.**

## Experiment B viability: technically possible for the first time

3 skills now exist covering `UNDERSTAND` (`codebase-intelligence`) → `VERIFY`
(`adversarial-diff-reviewer`) → `DEFINE CORRECTNESS`
(`acceptance-test-engineer`) — the first point in the roadmap where a real
composed chain can be attempted at all. Still missing for the *real*
Experiment B: a genuinely independent baseline run, a task with real stakes,
and more than one data point.

### Pilot B (not Experiment B) — N=1, self-run, un-blinded

Task: define acceptance criteria for "add a README to every directory that
is currently missing one," once using `acceptance-test-engineer` alone, once
composed with `codebase-intelligence`'s real (if stale) Phase 1 dogfood
output (`examples/codebase-intelligence/report.md`).

- **Alone**: the engine flags `no-boundary-signal` (no directories named);
  Step 3 cannot state which directories without inventing a list, so "which
  directories" must be an explicit assumption-flag case.
- **Composed**: `report.md`'s "Directories missing a README" section lists 9
  real directory paths from this repo's actual Phase 1 scan. With that as
  input, Step 3 produces a concrete, grounded acceptance case enumerating
  those exact 9 directories instead of flagging an assumption.
- **Pilot finding**: composition visibly resolved one specific gap
  (concreteness of "which directories") that the individual skill alone
  could only flag as unresolved. This is a real, observable difference, but
  it is one data point on one requirement type (an enumeration task where
  `codebase-intelligence`'s output happens to directly answer the missing
  question) — it does not show composition wins in general, only that it can
  in a case shaped like this one. **N=1. Not generalizable. Not a substitute
  for Experiment B.**

## Decision

Neither experiment has been run. [[16-assumptions-and-validation]] A2 and A10
are updated to reference this file and these two pilot findings; their
status is **not** upgraded beyond what one non-blinded, self-run data point
each can support. Both experiments remain blocked on the same missing
ingredient: a second, independent party (external engineer, or at minimum a
separate blind agent session) supplying one side of the comparison without
visibility into the other. Do not run either experiment "for real" using
only this session — that would repeat the exact self-authored-evidence
pattern already flagged as L8 in [[12-known-limitations]], now generalized
across both skills and both experiments.
