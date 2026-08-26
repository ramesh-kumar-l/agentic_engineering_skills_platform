# Engineering Knowledge Capture

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/engineering-knowledge-capture/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to judge whether a mechanically-flagged candidate is
  genuinely worth capturing (this skill's core value is judgment — is this
  really new knowledge, does it duplicate something already documented,
  what's the right canonical form to draft it in — not just pattern matching)

## Purpose
Given a free-text **engineering narrative** (session notes, a retro, a PR
description) and a real `codebase-intelligence` report for the repo the
narrative concerns, produce a deterministic **Knowledge Capture Report** —
candidate decisions, lessons, limitations, and workarounds, each resolved
against real structural data where a module is named — that an agent uses
to decide what's genuinely worth drafting into a durable ADR / known-
limitation / lessons-learned entry. This is the twelfth skill in the
portfolio, and the eighth to compose on a required `codebase-intelligence`
report (ADR-010).

## Problem
This project's own memory bank (`project-memory-bank/11-decisions.md`,
`12-known-limitations.md`, `13-lessons-learned.md`) exists because every
phase's real decisions, lessons, and disclosed gaps are worth keeping —
but capturing them has always been a manual, easy-to-skip step: nothing in
this portfolio flagged candidate knowledge in a session's own narrative
text, or connected a candidate to *how structurally significant* the
module it concerns actually is. A decision about a hotspot module is worth
writing up before the next session forgets it; a decision about a rarely-
touched file is not equally urgent. Nothing in this project could tell the
difference before this skill.

## When to Use
- At the end of a work session, phase, or PR — before the narrative
  describing what happened is lost to normal memory decay — to get a
  candidate list of what might be worth formally capturing.
- As a genuine, mandatory composition point on `codebase-intelligence`'s
  module list and dependency graph — this skill never guesses which
  module a narrative's "the scanner module" refers to; it resolves it
  against real, parsed data or says explicitly that it couldn't.
- Alongside this project's own memory-bank discipline (ADRs,
  known-limitations, lessons-learned) as a first-pass candidate finder,
  not a replacement for the human/agent judgment that actually decides
  what gets written and where.

## When NOT to Use
- **As an automatic memory-bank writer.** This skill never writes into
  `project-memory-bank/` itself. Its output is a candidate list; drafting
  and committing the actual entry is a separate, human/agent-checkpointed
  step (see Human Checkpoints).
- **As a commit-history or git-log analyzer.** This skill only extracts
  from the narrative text it's given — it does not parse real commit
  messages or diffs to reconstruct past decisions on its own. See Known
  Limitations.
- **As proof a candidate duplicates or doesn't duplicate an existing
  entry.** The engine has no access to the memory bank's actual contents
  and cannot know if something was already captured — that check is the
  agent's Step 3 responsibility (Checklist item 5).
- On a repository with no `codebase-intelligence` report yet — run that
  skill first; this skill refuses to run without one (ADR-010, reused an
  eighth time) rather than silently guessing at structural significance.
- As proof `suggested_capture_priority == "MEDIUM"` means "unimportant" —
  MEDIUM is also this engine's explicit fail-closed default when a
  candidate's location can't be resolved or the CI report itself carried
  a warning (see Known Limitations on the LOW band).

## Preconditions
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — ADR-010, reused an eighth time; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first).

## Inputs
- `<narrative-file-or-'-'>` (required, positional): a free-text engineering
  narrative — session notes, a retro, a PR description.
- `--ci-report <path>` (required): path to the `report.json` above.

## Required Context
The full `codebase-intelligence` report's module list and dependency graph
(`fan_in`, `hotspots`) — this is the entire grounding surface for location
resolution; the engine derives nothing about the target repo beyond that.

## Context Completeness
`codebase-intelligence`'s module list inherits whatever scan scope that
skill was run with (see [[12-known-limitations]] L2 for its own
root-level/parsing caveats). A candidate whose module genuinely exists in
the repo but wasn't captured by that scan will not resolve — reported as
`resolved_module_path: null`, not silently dropped from the candidate list.

## Security Constraints
- Read-only. Never writes to `project-memory-bank/` or any other file the
  caller doesn't explicitly direct output to.
- Never fetches anything over the network — pattern tables are static,
  bundled data, not a live feed.
- `suggested_capture_priority` is always advisory (ADR-011/017 precedent)
  — the engine never decides what gets captured; only a human, via the
  agent's workflow, makes that call.

## Workflow
1. **Gather inputs** — confirm a `codebase-intelligence` report.json exists
   for the target repo; generate one first if not (hard precondition).
   Gather or write the engineering narrative to run against.
2. **Run the engine** — `python -m engine.cli <narrative> --ci-report <path> --format both`.
3. **Agent walks the Knowledge Capture Checklist** (see
   [[05-evaluation-framework]]):
   ```
   1. Narrative scope stated (what session/change/timeframe does this cover?)
   2. Candidates reviewed per category (decision/lesson/limitation/workaround)
   3. Structural relevance considered (hotspot/high-fan-in module -> higher
      priority to actually write up)
   4. False-positive check (is this genuinely new knowledge, or restating
      something already captured elsewhere in the memory bank?)
   5. Duplicate check against existing ADRs/L-numbers (agent responsibility
      — the engine has no memory-bank access and cannot know this itself)
   6. Draft canonical entry (ADR / L-number / lesson-learned shape) for
      candidates worth keeping — this skill's actual deliverable
   7. Explicit uncertainty flag — thin/ambiguous narrative or an
      unresolved location defaults toward MEDIUM priority and says so,
      never silently LOW
   ```

## Agent Responsibilities
Verify a flagged candidate is genuinely new knowledge before drafting an
entry for it; check the memory bank for an existing entry the candidate
might duplicate or update instead of duplicate; never claim a candidate's
`resolved_module_path` means the narrative's claim about that module was
independently verified — only that the name matched a real module.

## Tool Permissions
Read-only filesystem access to the narrative text and CI report, and
(optionally) to write output report files. No network access, no write
access to `project-memory-bank/`.

## Human Checkpoints
A human (or the calling agent on the human's behalf) decides which
candidates are genuinely worth capturing and drafts/commits the actual
memory-bank entry. This skill's output is a candidate list only.

## Outputs
`KnowledgeCaptureReport` (JSON and/or Markdown) — see `engine/models.py`.

## Verification
Every candidate traces to a specific regex match and evidence line in the
narrative; run `pytest` in this skill's directory (47 tests) to confirm
deterministic behavior on the fixtures in `tests/`.

## Evaluation
See `evaluations/engineering-knowledge-capture/RESULTS.md`. Deterministic
layer: unit tests per engine module. Judgment layer: 8 hand-authored
fixtures, scored the same self-authored/single-rater way as every other
judgment skill in this project (L8) — disclosed as such, not overclaimed.

## Failure Conditions
Hard-fails (non-zero exit, `CiReportError`) on a missing or malformed
`codebase-intelligence` report, or on a missing narrative file path —
never proceeds on a guessed module list or empty narrative silently
treated as valid input.

## Known Limitations
- No real git/commit-history parsing — this skill only extracts from the
  narrative text it is given. It does not reconstruct past decisions from
  commit messages or diffs on its own.
- Never writes into `project-memory-bank/` itself — output is a candidate
  list, not a merged entry. Drafting and committing is a separate,
  human/agent-checkpointed step.
- `knowledge_patterns.py`'s marker table (16 patterns across 4 categories)
  is explicitly non-exhaustive — absence of a match proves nothing; a real
  decision/lesson/limitation/workaround phrased without these specific
  keywords will not be flagged.
- `location_resolver.py` skips module stems shorter than 4 characters
  (e.g. "io", "cli") to avoid noisy false matches against ordinary English
  words — a real short-stem module mentioned in a narrative will never
  resolve. Disclosed, not a silent gap.
- `suggested_capture_priority`'s `LOW` band is defined (see
  `engine/models.py`) but this version's `priority_scorer.py` never
  assigns it — a resolved-but-structurally-unremarkable candidate (a real
  module, zero fan-in, not a hotspot) defaults to `MEDIUM` instead, on the
  principle that failing upward (reviewing one extra candidate) is safer
  than failing downward (missing a real one). A future version could
  introduce a confident LOW band for that specific case; not done here.
- This is the FOURTH independent copy of the word-boundary-aware
  containment check first applied (after being disclosed as a bug three
  times — [[12-known-limitations|L23]]/[[12-known-limitations|L24]]) to
  `target_resolver.py` in `refactoring-safety`/`regression-hunter`/
  `release-readiness` — and the first one built correct from the start.
- `location_resolver.py` only searches the **exact matched line** for a
  module mention, not the surrounding paragraph — a real dogfood run
  found every candidate resolving to `null` despite the relevant module
  being named four times in the sentence immediately above the flagged
  marker (see [[12-known-limitations|L28]] and
  `examples/engineering-knowledge-capture/example-run.md`). Disclosed,
  not fixed — widening the window risks crediting an unrelated candidate
  with a module named several sentences earlier for a different reason.

## Examples
See `examples/engineering-knowledge-capture/example-run.md` — a real
dogfood run against this project's own engineering history.

## Provenance
Built in Phase 12, composing on `codebase-intelligence` (Phase 1) per
ADR-010's established pattern, at the user's explicit direction — a
second, one-time exception to the mentor-review roadmap freeze (see
`project-memory-bank/active-context.md`, 2026-08-26), not because A2/A5
moved off `UNKNOWN`.

## Changelog
- 0.1.0 (2026-08-26): Initial release.
