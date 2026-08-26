# Ten Skills In, I Stopped Building the Eleventh to Fix a Bug I'd Already Disclosed Four Times

*Part 6 in the Agentic Engineering Skills Platform series. All numbers cited
here are real, traceable to specific files in this repository at the time
of writing. [Repo README](../README.md) ·
[Part 5](05-building-an-ai-agent-that-cant-authorize-its-own-actions.md).*

## The number that should worry you isn't 10, it's 0

Ten AI-agent skills now exist in this repo: structural code analysis,
adversarial diff review, acceptance-test derivation, security classification,
root-cause analysis, architecture-decision support, refactor-safety scoring,
regression-risk assessment, and release-readiness scoring. 428 tests passing.
Ten evaluation harnesses. Ten real dogfood runs, each one used against this
project's own actual work, not a synthetic stand-in.

Zero of those ten skills have been used by anyone other than the person who
built them.

That's not a confession buried in fine print — it's the headline finding of
a deliberate pause this project just took. After Phase 10 shipped, instead
of starting an eleventh skill (Phase 11, Dependency/Supply Chain, was
already proposed and ready to go per the project's own roadmap), the project
stopped and asked a harder question: is building more skills actually the
right next move, or has building outpaced proving?

## The bug that took four disclosures to actually fix

Here's the concrete evidence that tipped the answer toward "stop and fix
something instead."

Three of these ten skills — `refactoring-safety`, `regression-hunter`, and
`release-readiness` — each independently implement a `target_resolver.py`
module that decides which files structurally depend on a given module. The
heuristic: check whether a module's stem (e.g. `"scanner"`) appears as a
**substring** anywhere in another module's import list.

That's a real bug. `"scanner"` is a substring of `"testability_scanner"`,
`"decision_scanner"`, `"safety_scanner"`, and half a dozen other unrelated
modules in this repo that happen to follow the same naming convention. The
dogfood run for `regression-hunter` found this directly: a query for
`scanner.py`'s callers returned **22 modules**, most of which had never
heard of it.

This bug was found and disclosed four separate times before it was fixed:

- **L14** (Phase 4) — first appearance, in a *different* heuristic
  (keyword-relevance scoring), same root cause: substring matching without
  boundaries.
- **L19, L21** (Phases 6-7) — the same class of collision, in two more
  independently-copied scoring modules.
- **L23** (Phase 9) — the exact `target_resolver.py` caller-list inflation
  described above.
- **L24** (Phase 10) — the sharpest version: the *same* heuristic, reused a
  third time in `release-readiness`, was shown to produce **false-positive
  test coverage** — a genuinely untested new module could be marked
  `has_coverage: true` because an unrelated skill's test file happened to
  import a same-named module. That's not a cosmetic display bug anymore;
  that's the exact signal a release-readiness rule table uses to decide
  whether a file needs closer review, silently wrong.

Four disclosures. Same honest write-up each time, in
[`project-memory-bank/12-known-limitations.md`](../project-memory-bank/12-known-limitations.md).
Same conclusion each time: "not applied... a real design tradeoff against a
currently-understood, now-N-times-disclosed limitation class, not evaluated
against evidence of need."

By the fourth time, that sentence had stopped being true. The evidence of
need was right there, written by the project's own hand, three phases
running.

## What actually changed

Two things, done in the same session as this write-up, deliberately *not*
as an eleventh skill:

**The bug got fixed** — a word-boundary-aware match
(`\bscanner\b` instead of `"scanner" in text`) closes the exact collision
class L23 and part of L24 described. `\w` includes underscore, so
`\bscanner\b` correctly rejects `"testability_scanner"` (no boundary between
`_` and `s`) while still matching a real, dotted import like
`"engine.scanner"`. Eight new regression tests, one per collision case,
mirroring the exact examples already documented in the limitations file.
Test count: 428, up from 420, zero regressions.

Worth being precise about what *didn't* get fixed: L24's headline example —
two different skills each legitimately importing their own identically-named
`models.py` — isn't solved by word-boundary matching alone. That still
produces a real, boundary-respecting false match, because the resolver has
no notion of "which skill does this belong to." Closing that needs
repo-layout-aware scoping, which wasn't built this pass — deliberately, to
avoid introducing new false negatives on a non-monorepo target repo without
evidence that tradeoff is worth it. The limitations file says exactly this,
not "fixed," for that part.

**A measurement harness got built** — `evaluations/usage-comparison/` is
the first artifact in this project that can log whether using a skill
actually saves tokens and time versus plain prompting on the same real task.
It ships empty. No numbers are claimed. The project's own stated goal —
skills that save developers real time, effort, and tokens — has never
actually been measured against a baseline, in ten phases. That's now at
least possible to check.

## The actual point

Radical honesty about limitations is only worth something if it eventually
changes what gets built next. A disclosed bug that gets disclosed again,
identically, four times, isn't honesty doing its job — it's honesty as a
substitute for action. The fix here isn't "build more skills, more
carefully." It's: when your own documentation tells you the same thing four
times, believe it the fourth time, not the fifth.

This project stays `EXPERIMENTAL` on every skill it ships — that label is
accurate and staying. What changed is what "next" means: not skill eleven,
but a real external user, an independent evaluation pass, and actual
before/after numbers, before this project claims to be something developers
should trust with their own time.
