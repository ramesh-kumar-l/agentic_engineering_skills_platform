# Context Optimizer

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/context-optimizer/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to judge whether a recommended file set is actually
  complete and non-noisy for the stated task (this skill's core value is
  judgment — is a semantically-relevant file missing that keyword
  matching couldn't catch, is a recommended file actually noise — not
  just scoring)

## Purpose
Given a free-text **task description** (what an agent is about to work
on) and a real `codebase-intelligence` report for the target repo,
produce a deterministic **Context Optimization Report** — a ranked list
of files an agent should actually consider loading into context, tiered
CORE/SUPPORTING/EXCLUDED by relevance and real structural signal
(fan_in/hotspot), optionally constrained to a line budget — instead of an
agent guessing or loading an entire repository. This is the thirteenth
skill in the portfolio, and the ninth to compose on a required
`codebase-intelligence` report (ADR-010).

## Problem
This project's own standing modularity rule — keep engine files under 300
lines so an agent reads only the specific file it needs, not a bloated
`services.py` — has always been enforced by hand, phase by phase, with no
tool that actually recommends *which* files a given task needs in the
first place. An agent starting a task either reads everything in a
directory speculatively (wasteful) or guesses from filenames alone
(unreliable, and blind to real structural significance like fan-in or
hotspot status). Nothing in this portfolio connected a task description
to a ranked, budget-aware file recommendation grounded in real repo data
before this skill.

## When to Use
- At the start of a task, before deciding what to read — to get a ranked
  candidate file list instead of guessing or loading everything.
- As a genuine, mandatory composition point on `codebase-intelligence`'s
  file list, module metadata, and dependency graph — this skill never
  guesses which files exist or how structurally significant they are; it
  scores against real, parsed data.
- When a rough context/line budget matters (a smaller model, a cost
  constraint, a desire to stay lean) and the caller wants files
  prioritized rather than an unranked list.

## When NOT to Use
- **As an automatic context loader.** This skill never loads any file
  into any actual agent session. Its output is a recommendation list; a
  human or the calling agent decides what to actually read (see Human
  Checkpoints).
- **As a semantic or embedding-based search tool.** Relevance is literal,
  tokenized keyword matching against path/docstring/function/class/import
  metadata already in the CI report — a file that is conceptually
  relevant but shares no literal keyword with the task description will
  not be recommended. See Known Limitations.
- **As proof `estimated_tokens` is an accurate token count.** It is a
  crude, disclosed line-count heuristic, not a real tokenizer. See Known
  Limitations.
- On a repository with no `codebase-intelligence` report yet — run that
  skill first; this skill refuses to run without one (ADR-010, reused a
  ninth time) rather than silently guessing at the file list.
- As proof an `EXCLUDED` tier means "irrelevant" — it only ever means
  "relevant but budget-constrained out." A genuinely irrelevant file
  (zero relevance score) never appears in the report at all.

## Preconditions
- A `codebase-intelligence` `report.json` already generated for the
  target repo (**hard precondition** — ADR-010, reused a ninth time; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first).

## Inputs
- `<task-file-or-'-'>` (required, positional): a free-text task
  description — what the agent is about to work on.
- `--ci-report <path>` (required): path to the `report.json` above.
- `--budget-lines <int>` (optional): a total line-count budget. A file
  whose own line count exceeds this alone is flagged, never silently
  excluded.

## Required Context
The full `codebase-intelligence` report's file list, module metadata
(docstring/functions/classes/imports), and dependency graph (`fan_in`,
`hotspots`) — this is the entire grounding surface for relevance scoring;
the engine derives nothing about the target repo beyond that.

## Context Completeness
`codebase-intelligence`'s file list inherits whatever scan scope that
skill was run with (see [[12-known-limitations]] L2 for its own
root-level/parsing caveats). A file that genuinely exists in the repo but
wasn't captured by that scan cannot be recommended — it simply does not
appear, the same "can't recommend what wasn't scanned" boundary every
composing skill in this portfolio inherits from `codebase-intelligence`.

## Security Constraints
- Read-only. Never writes to the target repo or any file the caller
  doesn't explicitly direct output to.
- Never fetches anything over the network — no live tokenizer API, no
  embedding service; scoring is static, local computation only.
- Recommendations are always advisory (ADR-011/017/018 precedent) — the
  engine never loads or decides what actually gets read; only a human, via
  the agent's workflow, makes that call.

## Workflow
1. **Gather inputs** — confirm a `codebase-intelligence` report.json
   exists for the target repo; generate one first if not (hard
   precondition). Gather or write the task description to run against.
2. **Run the engine** — `python -m engine.cli <task> --ci-report <path> [--budget-lines N] --format both`.
3. **Agent walks the Context Optimization Checklist** (see
   [[05-evaluation-framework]]):
   ```
   1. Task scope stated (what is the agent about to actually do?)
   2. CORE tier reviewed for completeness — any obviously-needed file
      that keyword matching wouldn't catch (a semantic-gap check the
      engine cannot do itself)
   3. SUPPORTING tier reviewed for genuine value vs. noise
   4. Oversized-single-file flags reviewed — consider an excerpt/summary
      instead of full inclusion (the modularity callback)
   5. Budget honesty check — if a budget was applied, confirm nothing
      load-bearing was silently excluded
   6. Duplicate/redundant coverage check (two files recommended that
      cover the same ground)
   7. Explicit uncertainty flag — a low-but-nonzero relevance score still
      earns at least SUPPORTING, and this checklist item says so, never
      silently narrowing further
   ```

## Agent Responsibilities
Verify the recommended CORE/SUPPORTING set is actually sufficient for the
stated task before proceeding — add a file the engine's literal keyword
matching missed if the agent's own understanding of the task calls for
it; never treat `EXCLUDED` as proof a file is unimportant, only that the
supplied budget couldn't fit it; never claim `estimated_tokens` as an
exact number to a downstream process that needs real precision.

## Tool Permissions
Read-only filesystem access to the task text and CI report, and
(optionally) to write output report files. No network access, no write
access to the target repo.

## Human Checkpoints
A human (or the calling agent on the human's behalf) decides what to
actually read. This skill's output is a recommendation list only — it
never loads context into any real session itself.

## Outputs
`ContextOptimizationReport` (JSON and/or Markdown) — see `engine/models.py`.

## Verification
Every recommendation traces to a specific keyword match (or structural
boost) against real CI report data; run `pytest` in this skill's
directory (64 tests) to confirm deterministic behavior on the fixtures in
`tests/`.

## Evaluation
See `evaluations/context-optimizer/RESULTS.md`. Deterministic layer: unit
tests per engine module. Judgment layer: 8 hand-authored fixtures, scored
the same self-authored/single-rater way as every other judgment skill in
this project (L8) — disclosed as such, not overclaimed.

## Failure Conditions
Hard-fails (non-zero exit, `CiReportError`) on a missing or malformed
`codebase-intelligence` report, on a missing task file path, or on a
negative `--budget-lines` value — never proceeds on a guessed file list
or silently treats invalid input as valid.

## Known Limitations
- No semantic or embedding-based matching — relevance is literal,
  tokenized keyword matching against path/docstring/function/class/import
  metadata. A conceptually relevant file sharing no literal keyword with
  the task description will not be recommended, the same disclosed
  scope boundary every keyword-matching engine in this portfolio carries
  (L14/L19/L21 lineage).
- `estimated_tokens` is a crude, fixed tokens-per-line heuristic
  (`size_estimator.py`), not a real tokenizer — this project makes no
  network calls (ADR-006), so no `tiktoken`-class dependency is available.
  Treat it as order-of-magnitude only, never as an exact budget guarantee.
- `relevance_scorer.py` tokenizes on `_`, `/`, `.`, and `-` rather than
  using a `\b` word-boundary regex (unlike `location_resolver.py`, its
  closest sibling in Phase 12). This is a deliberate, disclosed
  precision/recall tradeoff, not an oversight: it lets a single-word
  keyword match one real component of a compound snake_case filename
  (e.g. "resolver" against `location_resolver.py`), but as a consequence
  a keyword can also match a filename where that word is only one
  component among several (e.g. "scanner" against
  `testability_scanner_utils.py`) even when that file isn't really about
  scanning. Appropriate here because this skill ranks many weighted
  candidates rather than resolving to one canonical location — see
  `engine/relevance_scorer.py`'s docstring for the full reasoning.
- No secondary noise-reduction cutoff above zero relevance — any file
  that scores above zero on real keyword matching earns at least
  `SUPPORTING`, by design (ADR-019's fail-OPEN discipline). A caller
  wanting a tighter, higher-precision list must filter `SUPPORTING`
  entries out itself; this skill will not do it silently.
- `CORE_THRESHOLD` (`budget_selector.py`) and the per-field scoring
  weights (`relevance_scorer.py`) are simple, disclosed fixed constants —
  not derived from the composed report's own score distribution, the same
  "fixed threshold, not percentile-based" choice `engineering-knowledge-
  capture`'s `priority_scorer.py` made for `HIGH_FAN_IN_THRESHOLD`.
- This is the FIFTH independent copy of a whole-token containment check
  built to avoid arbitrary mid-word substring collisions
  ([[12-known-limitations|L23]]/[[12-known-limitations|L24]] lineage) —
  and the SECOND built correct from day one, after Phase 12's
  `location_resolver.py`.
- At full-repository scale, keyword relevance floods with false-positive
  CORE recommendations when the task description is phrased in this
  project's own recurring vocabulary (shared documentation/evaluation-
  harness boilerplate across every skill) — a real dogfood run found 5 of
  17 CORE recommendations were unrelated files (four other skills'
  `run_evaluation.py` files plus one unrelated fixture), not
  `context-optimizer` files. Same mechanism class as
  `architecture-decision`'s L14/L19/L21, a new manifestation of it.
  Disclosed, not fixed — see [[12-known-limitations|L29]] and
  `examples/context-optimizer/example-run.md`.

## Examples
See `examples/context-optimizer/example-run.md` — a real dogfood run
against this project's own engineering history.

## Provenance
Built in Phase 13, composing on `codebase-intelligence` (Phase 1) per
ADR-010's established pattern, at the user's explicit direction — a
third, one-time exception to the mentor-review roadmap freeze (see
`project-memory-bank/active-context.md`, 2026-08-26), not because A2/A5
moved off `UNKNOWN`.

## Changelog
- 0.1.0 (2026-08-26): Initial release.
