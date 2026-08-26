# Engineering Memory — real dogfood run

A real, non-synthetic retrieval run against this project's own actual
`project-memory-bank/11-decisions.md` and `12-known-limitations.md` — not
a fixture stand-in. Command run from `skills/engineering-memory/`, using a
real `codebase-intelligence` report freshly generated for this repo:

```bash
python -m engine.cli \
  --task "We're building the fifteenth and final skill in the
originally-scoped portfolio, engineering-memory, which retrieves relevant
ADRs and known limitations from this project's own memory bank for a
given task, using word-boundary matching to avoid the substring-collision
bug this project has hit six times before across five other skills, and
flags stale or superseded records rather than presenting them as current
guidance." \
  --ci-report <path-to-real-report.json> \
  --decisions-path <platform-root>/project-memory-bank/11-decisions.md \
  --limitations-path <platform-root>/project-memory-bank/12-known-limitations.md \
  --format both --top-n 8 --out-dir <out-dir>
```

This is the task description this session actually used to build Phase 15
itself — the same "eat your own dog food on a real task from this
session" discipline every prior phase's `example-run.md` followed.

## What actually happened

The corpus parsed cleanly: **50 real records** (20 decisions, 30
limitations) from this project's actual memory bank at the time of the
run — every `## ADR-NNN:` and `## LNN:` section, with every `## L8
update:` sub-entry correctly excluded from the count.

Top 8 matches, real scores:

| Rank | Record | Score | Stale |
|---|---|---|---|
| 1 | ADR-016 (`release-readiness`) | 53 | no |
| 2 | L24 (target_resolver.py false-positive coverage) | 48 | no |
| 3 | L29 (`context-optimizer` keyword flooding) | 47 | no |
| 4 | ADR-020 (`workflow-composer`) | 44 | no |
| 5 | ADR-018 (`engineering-knowledge-capture` word-boundary) | 42 | no |
| 6 | ADR-015 (`regression-hunter`) | 37 | no |
| 7 | ADR-017 (`dependency-supply-chain`) | 33 | **yes** |
| 8 | L23 (target_resolver.py substring bug) | 31 | **yes** |

Both staleness flags fired correctly on real data: L23 flagged because its
own title carries `(FIXED 2026-08-26, mentor-review follow-up)`; ADR-017
flagged because it mentions `license_patterns.py` in its body, and that
file does not exist as a real module in the current
`codebase-intelligence` report (the ADR explicitly declined to build a
license-risk feature — the file was discussed, never shipped).

## The finding this run actually surfaced

`module_resolver.py`'s basename-exact-equality resolution — built from
day one specifically to defeat the L23/L24/L28-class *substring*
collision — has a different, real ambiguity of its own once the corpus is
this project's actual memory bank: **many real, distinct files across
this portfolio share an identical basename.** `ci_report_loader.py` alone
exists in essentially every composing skill (`root-cause-analyzer`,
`architecture-decision`, `refactoring-safety`, `regression-hunter`,
`release-readiness`, `dependency-supply-chain`, `engineering-knowledge-
capture`, `context-optimizer`, `workflow-composer`, this skill itself,
and more). `resolve_module_mentions`'s `by_basename` lookup keeps only
one `(path, fan_in, is_hotspot)` tuple per basename — whichever
`codebase-intelligence` module happened to be iterated last — so **every**
record in this run that mentions `` `ci_report_loader.py` `` resolved to
the same single path (`skills/root-cause-analyzer/engine/
ci_report_loader.py`), regardless of which skill's ADR actually named it.
This is visible directly in the real output: ADR-016, L24, ADR-020,
ADR-015, and ADR-017 all list `root-cause-analyzer/engine/
ci_report_loader.py` in their `matched_modules`, even though none of them
is actually about `root-cause-analyzer`.

This was **disclosed as a residual risk in `SKILL.md` before this run**
("two different real repo paths sharing an identical basename... resolve
ambiguously to whichever the CI report lists last, not to a chosen
'correct' one") — this dogfood run is the first **concrete confirmation**
that it isn't a hypothetical edge case but the *normal* case once the
corpus is a real, many-skill codebase with a repeated-basename convention
(`models.py`, `report.py`, `stats.py`, `cli.py`, `ci_report_loader.py` all
recur across most skills). Logged as **L31** in
`project-memory-bank/12-known-limitations.md` — disclosed, not fixed here,
same "one real data point, don't guess a fix" discipline this project
applied to L14/L18/L21/L22/L23/L24/L28/L29/L30 on their first discovery.

**Directly relevant to this skill's own scope**: the retrieval and
staleness logic both worked correctly on real data — 8/8 top matches were
substantively on-topic for the real task, and both real staleness signals
(a FIXED title, a genuinely-missing mentioned module) fired correctly.
The gap is narrower than "wrong answer": `matched_modules` for a
common-basename mention can misattribute *which specific file* a record
was about, without affecting whether the record itself was correctly
judged relevant. An agent reading a match's module list at face value,
without checking the record's own source line, could draw a wrong
conclusion about which skill's code a given ADR or limitation actually
concerns.
