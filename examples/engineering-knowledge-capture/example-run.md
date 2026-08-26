# Real dogfood run — engineering-knowledge-capture

This is a real run, not a synthetic fixture: a fresh `codebase-intelligence`
report regenerated against this repo's current (twelve-skill) state,
composed with a real narrative built from verbatim excerpts of this
project's own actual engineering history — the "Mentor-review follow-up"
and "What Phase 11 built" sections of `project-memory-bank/
active-context.md` (the L23/L24 substring-bug fix, and Phase 11's dropped
license-detection scope decision) — not invented text.

## Commands run

```bash
cd skills/codebase-intelligence
python -m engine.cli ../../ --format json --out <scratch>/ci_out

cd ../engineering-knowledge-capture
python -m engine.cli <scratch>/dogfood-narrative.txt \
  --ci-report <scratch>/ci_out/report.json --format both --out <scratch>/ekc_out
```

## Narrative input

```
Fixed L23 fully, L24 partially — replaced the bare substring check
(target_stem in imports_text) with a word-boundary-aware match (\b<stem>\b)
in refactoring-safety/engine/target_resolver.py,
regression-hunter/engine/target_resolver.py,
release-readiness/engine/target_resolver.py, and
release-readiness/engine/test_coverage_scanner.py. [...]

Turns out the root cause was that a bare `stem in text` containment check
matches anywhere a stem substring appears, not just at a real word
boundary [...]

We decided to keep the three-copy portability discipline (no shared
imports between skills) rather than extracting target_resolver.py into a
shared library, even after finding the same bug independently in three
places, because this project's own architecture principle prioritizes
per-skill portability over DRY convenience.

Known limitation: license-risk detection was dropped mid-build in Phase 11
[...]

As a workaround for Phase 11, dependency-supply-chain ships without any
license-risk signal at all [...]
```

(Full text: this file's own `../../evaluations/engineering-knowledge-capture/`
sibling harness does not include this narrative — it lives only here, since
it is drawn from real project history rather than being a synthetic fixture.)

## Actual output

```
## Candidates (5)
- [MEDIUM] decision (decision-we-decided) — no resolvable location
  > We decided to keep the three-copy portability discipline (no shared
- [MEDIUM] lesson (lesson-turns-out) — no resolvable location
  > Turns out the root cause was that a bare `stem in text` containment check
- [MEDIUM] lesson (lesson-root-cause-was) — no resolvable location
  > Turns out the root cause was that a bare `stem in text` containment check
- [MEDIUM] limitation (limitation-known-limitation) — no resolvable location
  > Known limitation: license-risk detection was dropped mid-build in Phase 11
- [MEDIUM] workaround (workaround-explicit) — no resolvable location
  > As a workaround for Phase 11, dependency-supply-chain ships without any
```

## What this confirms

All four categories fire correctly on real (not synthetic) engineering
prose, including a genuine double-match on one sentence (`lesson-turns-out`
and `lesson-root-cause-was` both firing on the same "Turns out the root
cause was..." line — correct, not a bug: the sentence genuinely contains
both marker phrases, and the checklist's Step 4 false-positive check would
correctly treat these as one lesson, not two).

## What this found — a new, real, disclosed-not-fixed limitation

**Every candidate resolved to `null`** despite the narrative naming a real,
currently-existing module (`target_resolver.py`) four times, by full path,
in the paragraph immediately above the "We decided..." and "Turns out..."
sentences that `knowledge_scanner.py` actually flagged. This is a genuine
gap, not a fixture artifact: `location_resolver.py` only searches the
**exact matched line** for a module mention (see `report.py`'s
per-candidate resolution call), and in real prose — unlike this skill's
own synthetic fixtures, which were deliberately written with the module
name in the same sentence as the marker — the module name and the
decision/lesson marker often land in *adjacent* sentences of the same
paragraph instead of the same line.

This is now logged as **L28** in `project-memory-bank/12-known-limitations.md`:
disclosed, not fixed, the same way most first-discovery dogfood findings in
this project are handled (e.g. L14, L18, L21, L22) — a fix would mean
widening the resolution window from "the matched line" to "the matched
line's surrounding paragraph," which risks the opposite failure mode (a
module named three sentences earlier for an unrelated reason gets
incorrectly credited to this candidate). Left as a known limitation
pending real evidence that a wider window's precision loss is worth its
recall gain, rather than guessing at the right window size synthetically.

## Honest comparison to a synthetic fixture

The evaluation harness's `case-06-hotspot-module-mentioned` fixture (see
`evaluations/engineering-knowledge-capture/RESULTS.md`) deliberately puts
the module mention in the same sentence as the decision marker and
resolves correctly, scoring `HIGH`. This real run is the first evidence
that the synthetic fixtures' one-sentence-per-candidate shape doesn't
match how this project's own real retrospective narratives are actually
written — the same category of honest gap between "the workflow executes
correctly on fixtures" and "the workflow performs well on real prose" this
project's L8 caveat already generalizes, sharpened here with a concrete,
reproducible example rather than left abstract.
