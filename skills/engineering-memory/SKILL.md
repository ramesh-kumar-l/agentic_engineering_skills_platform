# Engineering Memory

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/engineering-memory/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to judge whether a retrieved record is genuinely relevant
  (vs. a coincidental keyword hit) and how much weight a staleness flag
  should carry — this skill's core value is judgment over retrieved leads,
  not a verdict engine.

## Purpose
Given a free-text **task description** and a real `codebase-intelligence`
report for the repo the task concerns, retrieve and rank the entries from
this project's **own memory bank** (`project-memory-bank/11-decisions.md`,
`12-known-limitations.md`) that are actually relevant to the task, each
with a relevance score, matched keywords/modules, source provenance, and
an explicit staleness flag. This is the fifteenth skill in the portfolio
— the last in the originally-scoped 15-skill portfolio
(`project-memory-bank/08-roadmap.md`) — and the eleventh to compose on a
required `codebase-intelligence` report (ADR-010).

## Problem
`engineering-knowledge-capture` (Phase 12) can flag new candidate
decisions/lessons/limitations from a session's narrative, but named its
own gap explicitly: *"the engine has no access to the memory bank's
actual contents and cannot know if something was already captured."*
Nothing in this portfolio, before this skill, could answer the opposite
question either: given a task an agent is about to start, which of this
project's *already-recorded* ADRs and known limitations actually bear on
it? Six prior limitations (L14, L19, L21, L23/L24, L28, L29, L30) already
disclose the same coincidental-substring-flooding mechanism across five
different skills — a real, standing example of exactly the kind of
knowledge this skill exists to resurface before a sixteenth instance gets
discovered the hard way, via another real dogfood run.

## When to Use
- Before starting a task on this repo — to surface ADRs and known
  limitations that already bear on it, before re-deriving or re-
  discovering something this project's own history already recorded.
- As a genuine, mandatory composition point on `codebase-intelligence`'s
  module list — this skill never guesses whether a memory record's named
  module still exists in the current repo; it resolves it against real,
  parsed data or flags the record as possibly stale.
- Alongside `engineering-knowledge-capture` as its natural complement:
  that skill goes narrative → candidate *new* entries; this skill goes
  task → retrieved *existing* entries. Running both together is how a
  human/agent closes `engineering-knowledge-capture`'s own named
  duplicate-detection gap — this skill does not bridge that automatically.

## When NOT to Use
- **As proof A8 ("engineering memory improves future agent performance")
  is validated.** Building this skill creates the retrieval capability
  A8 would need to be tested against — it is not itself that evidence.
  A8's status stays `UNKNOWN` (`project-memory-bank/16-assumptions-and-
  validation.md`).
- **As an automatic memory-bank writer.** This skill never writes into
  `project-memory-bank/` itself. Its output is a retrieval report only.
- **As a full corpus.** This version parses only `11-decisions.md` and
  `12-known-limitations.md` — `sprint-history/*.md`'s own Lessons Learned
  sections are a real, disclosed corpus gap, not yet parsed (see Known
  Limitations). An empty result set is not proof nothing in this
  project's history applies.
- **As proof a retrieved match is current guidance without checking its
  staleness flag.** A `FIXED`/`SUPERSEDED` record, or one whose mentioned
  module no longer exists, is still returned (never silently dropped —
  an agent might judge it still relevant despite the flag) but always
  with the flag attached. Treating an unflagged high score as
  automatically authoritative skips the judgment this skill exists to
  support, not replace.
- On a repository with no `codebase-intelligence` report yet — run that
  skill first; this skill refuses to run without one (ADR-010, reused an
  eleventh time) rather than silently guessing at structural significance.

## Preconditions
- A `codebase-intelligence` `report.json` already generated for the
  target repo (**hard precondition** — ADR-010, reused an eleventh time;
  run `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first).
- A `project-memory-bank/11-decisions.md`-shaped ADR log and a
  `12-known-limitations.md`-shaped limitations log (or equivalents using
  the same `## ADR-NNN: Title` / `## LNN: Title` section-header
  convention) reachable on disk.

## Inputs
- `--task <text>` (required): free-text task description to retrieve
  relevant memory for.
- `--ci-report <path>` (required): path to the `report.json` above.
- `--decisions-path <path>` (required): path to the ADR log.
- `--limitations-path <path>` (required): path to the known-limitations log.
- `--top-n <N>` (optional, default 10): maximum number of matches returned.

## Required Context
The full `codebase-intelligence` report's module list and dependency graph
(`fan_in`, `hotspots`) — the entire grounding surface for module-mention
resolution — plus this project's own `11-decisions.md` /
`12-known-limitations.md` text, the entire grounding surface for
retrieval. The engine derives nothing about either beyond what these
three inputs literally contain.

## Context Completeness
`codebase-intelligence`'s module list inherits whatever scan scope that
skill was run with (see [[12-known-limitations]] L2). A memory record
whose mentioned module genuinely still exists but wasn't captured by that
scan will be flagged `exists: false` — a false staleness signal in that
specific case, disclosed below, not silently presented as certain.

## Security Constraints
- Read-only. Never writes to `project-memory-bank/` or any other file the
  caller doesn't explicitly direct output to.
- Never fetches anything over the network.
- Every match's staleness flag and relevance score are always advisory
  (ADR-011/017/018/020 precedent) — the engine never decides whether a
  match is actually relevant or actually stale; only a human, via the
  agent's workflow, makes that call.

## Workflow
1. **Gather inputs** — confirm a `codebase-intelligence` report.json
   exists for the target repo (hard precondition); locate the memory-bank
   files to retrieve against.
2. **Run the engine** —
   `python -m engine.cli --task "..." --ci-report <path> --decisions-path <path> --limitations-path <path> --format both`.
3. **Agent walks the Engineering Memory Retrieval Checklist** (see
   [[05-evaluation-framework]]):
   ```
   1. Retrieved records actually relevant to the task (not a coincidental
      keyword hit) — judged, not assumed from a nonzero score
   2. Every staleness-flagged record's flag reviewed before treating it
      as current guidance
   3. Absence of a relevant record is not proof nothing applies — corpus
      is limited to 11-decisions.md + 12-known-limitations.md this pass
   4. A high relevance score is not authorization to act without
      checking the record's own original context (source file/line)
   5. This retrieval is not evidence toward A8 — it is the capability A8
      would need to be tested against, nothing more
   ```

## Agent Responsibilities
Verify a retrieved match is genuinely relevant before acting on it; weigh
every staleness flag explicitly rather than treating an unflagged match
as more authoritative than it is; check the memory bank directly for
context this report's excerpted body may have truncated; never treat an
empty result set as proof this project's history has nothing to say about
the task — it may only mean the corpus this pass covers is incomplete.

## Tool Permissions
Read-only filesystem access to the CI report and the two memory-bank
files, and (optionally) to write output report files. No network access,
no write access to `project-memory-bank/`.

## Human Checkpoints
A human (or the calling agent on the human's behalf) decides which
retrieved matches are actually relevant and how much weight a staleness
flag carries. This skill's output is a ranked retrieval report only —
never an instruction to act.

## Outputs
`MemoryQueryReport` (JSON and/or Markdown) — see `engine/models.py`.

## Verification
Every match traces to a specific `record_id` and `source_file:source_line`
in the memory-bank corpus; run `pytest` in this skill's directory (57
tests) to confirm deterministic behavior on the fixtures in `tests/`.

## Evaluation
See `evaluations/engineering-memory/RESULTS.md`. Deterministic layer: unit
tests per engine module, including a proactive regression test proving a
short/common module basename never false-matches via substring
containment (the L23/L24 class, tested before any bug, not after one).
Judgment layer: 8 hand-authored fixtures, scored the same self-authored/
single-rater way as every other judgment skill in this project (L8,
applied a fourteenth time) — disclosed as such, not overclaimed.

## Failure Conditions
Hard-fails (non-zero exit, `CiReportError`) on a missing or malformed
`codebase-intelligence` report, or on a missing decisions/limitations
file path — never proceeds on a guessed module list or an assumed-empty
corpus silently treated as valid input.

## Known Limitations
- Corpus is limited to `11-decisions.md` and `12-known-limitations.md`
  this pass — `sprint-history/*.md`'s Lessons Learned sections are not
  yet parsed. A real lesson recorded only in a sprint retrospective will
  never surface here. Disclosed, not silently omitted.
- `memory_bank_parser.py` parses only top-level `## ` section headers
  matching the `ADR-NNN:` / `LNN:` convention — a memory-bank file that
  drifts from this exact header shape (no colon, different prefix, a
  renumbered scheme) will silently parse to zero records for that file,
  surfaced only via the "no records parsed" warning, not a per-line
  diagnostic of what didn't match.
- Word-boundary/whole-token matching (`module_resolver.py`,
  `relevance_scorer.py`) is applied from day one specifically because six
  prior disclosed limitations (L14/L19/L21/L23/L24/L28/L29/L30) already
  proved the substring-containment alternative fails — this is
  "mitigated by construction," not "proven bug-free by a real dogfood
  run" the way those six limitations were found. Two distinct real repo
  paths sharing an identical basename (e.g. two different `models.py`
  files) still resolve ambiguously to whichever the CI report lists last
  for that basename, not to a chosen "correct" one — **confirmed, not
  just theoretical**, by this skill's own real dogfood run: see L31
  below and `examples/engineering-memory/example-run.md`.
- **L31** (real dogfood finding): `module_resolver.py`'s basename-exact
  resolution collapses every memory-bank record mentioning a common
  basename (`ci_report_loader.py`, `models.py`, `report.py`, `stats.py`,
  `cli.py` — each real and distinct across most of this portfolio's
  skills) into whichever single real file the CI report happens to list
  last for that basename. A real run against this project's own memory
  bank found every record mentioning `ci_report_loader.py` — ADR-016,
  L24, ADR-020, ADR-015, ADR-017, spanning five different skills —
  resolving to the same `root-cause-analyzer` copy in `matched_modules`,
  regardless of which skill's file the record actually named. Does not
  affect whether a record is judged relevant (task-keyword scoring is
  independent of module resolution), only which specific file a match's
  `matched_modules` list points to. Disclosed, not fixed here.
- `_MIN_SCORE_THRESHOLD = 1` in `report.py` means any nonzero score
  surfaces — a single incidental one-field keyword hit and a strong
  multi-field, module-grounded match are both "matches," distinguished
  only by their relative score, not a confidence tier. An agent scanning
  only the top result and ignoring the score value could overweight a
  weak match.
- Never writes into `project-memory-bank/` itself, and never bridges to
  `engineering-knowledge-capture`'s own named duplicate-detection gap —
  running both skills together on the same task remains a human/agent
  responsibility, not glue code this skill provides.
- This is the first skill in the portfolio whose primary input corpus is
  this project's **own** `project-memory-bank/` markdown rather than a
  target repo's external artifacts (ADR-021's "self-referential
  composition") — untested against any memory bank other than this
  project's own.

## Examples
See `examples/engineering-memory/example-run.md` — a real dogfood run
against this project's own `11-decisions.md` and `12-known-limitations.md`.

## Provenance
Built in Phase 15, composing on `codebase-intelligence` (Phase 1) per
ADR-010's established pattern, at the user's explicit direction — the
fifth one-time exception to the mentor-review roadmap freeze (see
`project-memory-bank/active-context.md`, 2026-08-26), not because A2/A5
moved off `UNKNOWN`. Unlike Phase 14, this phase was reached in its
designated order per A8's own "design only when reached" gate — it did
not jump ahead of a named "do not build" decision the way Phase 14 did.

## Changelog
- 0.1.0 (2026-08-26): Initial release.
