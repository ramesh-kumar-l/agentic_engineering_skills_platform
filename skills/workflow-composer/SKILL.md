# Workflow Composer

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/workflow-composer/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to judge whether a task actually fits one of the 3
  registered templates, and whether a real run's chain of results is
  actually sound — not just whether it completed (this skill's core value
  is judgment about composition fit and trustworthiness, not just
  execution)

## Purpose
Given a **template name**, a target repo, and a free-text task
description, sequence and actually **execute** a small, hardcoded chain of
this portfolio's own real skill CLIs — the first skill in the portfolio
whose deliverable is composed execution, not analysis. Produces a
`WorkflowRunReport`: per-step status/duration/output path, any
compatibility drift found before running, and a plain reminder that this
is a real pilot, not the rigorous Experiment B comparison the roadmap
still calls for. This is the fourteenth skill in the portfolio, and the
tenth to compose on a required `codebase-intelligence` report (ADR-010) —
every registered template's first step is that report.

## Problem
Every prior skill in this portfolio analyzes one artifact in isolation.
Nothing actually **ran** two or more of them together for a real task
except by hand, one CLI invocation at a time, with a human manually
copying a file path from one skill's `--out` directory into the next
skill's input flag — exactly what Phase 3's Pilot B and Phase 4's real
dogfood run both did manually. This skill mechanizes that same, already-
proven manual pattern into a real, re-runnable chain, without inventing
new, unvalidated compositions.

## When to Use
- When a task genuinely fits one of the 3 registered templates (see
  `--list-templates`) and the caller wants the underlying skill chain
  actually run, not just planned by hand.
- To validate a template/task pairing cheaply first via `--dry-run` (plan
  compilation + compatibility check, zero subprocess calls) before
  committing to a real, timed run.
- As a genuine, mandatory composition point on `codebase-intelligence` —
  every template's step 1 is that report; there is no template that skips
  it.

## When NOT to Use
- **As a generic, arbitrary skill chainer.** The registry ships with
  exactly 3 hardcoded templates, each reusing a composition this project
  already ran for real in an earlier phase's dogfood. A new composition
  requires a code change and a real dogfood run, not a config edit — see
  Known Limitations.
- **As proof this satisfies Experiment B.** ADR-009 warns explicitly
  against mistaking an internal pilot for the real, independently-
  baselined validation experiment `16-assumptions-and-validation.md` (A10)
  still calls for. Every real run this skill produces is disclosed
  timing evidence, never cited as resolving A10's `UNKNOWN` status.
- **As a mutator of the target repo.** Every composed skill is read-only
  and advisory; this executor only ever writes report files under
  `--out-dir`.
- On a task that doesn't cleanly fit any of the 3 templates — forcing one
  anyway produces a mechanically valid but practically useless chain (see
  Known Limitations: the engine cannot judge fit for itself).

## Preconditions
- The target skills named in the chosen template (always including
  `codebase-intelligence`) must exist under this platform's `skills/`
  directory with a real, runnable `engine/cli.py` (**hard precondition**
  — `skill_locator.py` fails closed if one is missing).
- Python 3.10+ available in the execution environment (all composed
  skills are stdlib-only, per ADR-006 — no install step is required
  beyond the repo already being checked out).

## Inputs
- `<template-name>` (required, positional): one of `understand-then-plan`,
  `understand-then-test-plan`, `understand-then-optimize-context` (see
  `--list-templates`).
- `--repo-path <dir>` (required): the repository the workflow analyzes.
- `--task "<text>"` (required unless `--dry-run`): free-text task
  description passed to downstream steps.
- `--out-dir <dir>` (required): directory to write per-step outputs and
  the run report into.
- `--dry-run` (optional): validate the plan without spawning any
  subprocess.
- `--list-templates` (optional): print the registry and exit.

## Required Context
The real, on-disk `engine/cli.py` of every skill named in the chosen
template, and that skill's `SKILL.md` Preconditions/Required Context
sections (used by the compatibility checker to confirm the declared
wiring still matches the real contract before any real execution runs).

## Context Completeness
The compatibility checker is a **textual** drift guard — it confirms the
upstream skill's name still appears in the downstream skill's
Preconditions/Required Context sections, not a real schema/type check. A
SKILL.md edit that changes wording without removing the marker string, or
a real CLI flag change that isn't reflected in SKILL.md at all, can pass
this check while still being broken. See Known Limitations.

## Security Constraints
- Every composed skill stays read-only/advisory against the target repo —
  this executor never mutates it, only writes report files under
  `--out-dir`.
- Never fetches anything over the network — every subprocess call is a
  local Python invocation of another skill's own stdlib-only engine.
- Fails CLOSED on execution uncertainty (ADR-020) — a compatibility issue
  blocks all real execution outright; any step's failure stops the chain,
  and no downstream step ever runs on stale or absent upstream data.

## Workflow
1. **Choose a template** — confirm the task genuinely fits one of the 3
   registered templates (`--list-templates`); do not force a poor fit.
2. **Dry-run first** (recommended) — `python -m engine.cli <template>
   --repo-path <dir> --dry-run --out-dir <dir>` to validate the plan and
   surface any compatibility drift before spending real time on a full
   run.
3. **Run for real** — drop `--dry-run`, add `--task "<description>"`.
4. **Agent walks the Workflow Composition Checklist** (see
   [[05-evaluation-framework]]):
   ```
   1. Task actually fits one of the 3 registered templates (not forced)
   2. Compatibility check result reviewed — any flagged drift
      investigated before trusting real execution
   3. Each step's own Human Checkpoints (from its SKILL.md) still apply —
      composition doesn't imply full autonomy
   4. Chain-failure handling reviewed if any step returned
      FAILED/SKIPPED
   5. Real run timing/output sanity-checked, not assumed correct because
      the chain completed
   6. Explicit reminder: this pilot's timing data is not Experiment B
      (ADR-009) — never cite it as validating A10
   ```

## Agent Responsibilities
Judge whether the task actually fits the chosen template before running
it — the engine has no template-selection logic of its own and will
mechanically "succeed" at compiling a plan for a poor fit. Investigate any
`compatibility_issues` before trusting a real run's wiring. Never treat a
fully `OK` chain as proof the *content* it produced is correct — each
composed skill's own Human Checkpoints still apply downstream of this
skill's own report.

## Tool Permissions
Read-only filesystem access to the target repo and every composed skill's
source; write access limited to `--out-dir`. Spawns local Python
subprocesses for each real step (no network access, no shell/eval of
caller-supplied strings — every subprocess argv is built from typed
`WorkflowStep` fields, never string-interpolated from free text).

## Human Checkpoints
A human (or the calling agent on the human's behalf) decides whether to
run a template for real, reviews any compatibility drift before trusting
a run, and still exercises every composed skill's own Human Checkpoints
downstream — this skill running end-to-end does not imply full autonomy
over the underlying skills' own advisory outputs.

## Outputs
`WorkflowRunReport` (JSON and/or Markdown) — see `engine/models.py`.

## Verification
Every step result traces to a real subprocess exit code and a real
output file (or an explicit `SKIPPED`/`FAILED` reason); run `pytest` in
this skill's directory (51 tests, including one genuinely real
subprocess-based integration test) to confirm deterministic behavior on
the fixtures in `tests/`.

## Evaluation
See `evaluations/workflow-composer/RESULTS.md`. Deterministic layer: real
registry templates run against a bundled tiny fixture repo, plus
fail-closed paths exercised against fixture fake skills for determinism.
Judgment layer: 8 hand-authored fixtures, scored the same self-authored/
single-rater way as every other judgment skill in this project (L8) —
disclosed as such, not overclaimed.

## Failure Conditions
Hard-fails (non-zero exit) on an unknown template name, a missing/invalid
`--repo-path`, a missing `--task` without `--dry-run`, a target skill
directory that doesn't exist (`SkillNotFoundError`), or a flagged
compatibility issue during real (non-dry-run) execution — never proceeds
on a guessed wiring or silently treats a failed step's absence as success.

## Known Limitations
- The registry is a small, **hardcoded** set of exactly 3 templates, each
  reusing a composition already run for real in an earlier phase's
  dogfood — deliberately not a generic arbitrary-skill chainer (ADR-020).
  A new composition requires a code change and a real dogfood run, not a
  config edit.
- The compatibility checker (`compatibility_checker.py`) is a **textual**
  drift guard, not real schema/type validation — it confirms the upstream
  skill's name still appears in the downstream skill's Preconditions/
  Required Context sections. It cannot catch a wiring-*mode* error (e.g.
  a template declaring `CLI_FLAG` for a skill whose CLI has no such flag)
  if the marker string itself is still present — that would only surface
  as a real subprocess failure at run time, which the fail-closed
  executor does catch, just later than the pre-execution gate would.
- The zero-install assumption (every composed skill is stdlib-only per
  ADR-006, so subprocess execution needs no separate install step) breaks
  silently if a future skill ever gains an external dependency — this
  skill has no mechanism to detect that in advance.
- `step_runner.py`'s subprocess timeout (120s default) is a disclosed,
  fixed constant, not tuned against real large-repository timing beyond
  what this session's own dogfood run observed.
- The engine has **no template-fit judgment of its own** — given a task
  that doesn't suit any of the 3 templates, it will still mechanically
  compile and (if run for real) execute the named template, producing a
  chain that completes without error while being practically useless.
  Judging fit is entirely the agent's responsibility (Checklist item 1).
- This pilot's real execution timing is explicitly **not** Experiment B
  (ADR-009) — see `project-memory-bank/16-assumptions-and-validation.md`
  A10, which still reads `UNKNOWN` after this phase.
- **Composed skills' own known limitations pass through unfiltered.**
  This skill never re-ranks, filters, or otherwise improves a composed
  skill's own output. A real dogfood run found `feature-planner`'s
  relevance scorer (used inside `understand-then-plan`) ranked a test
  file above every real implementation file relevant to the task — the
  same corpus-vocabulary-flooding mechanism `architecture-decision`
  (L14/L19/L21) and `context-optimizer` (L29) already disclosed, now
  observed for the first time inside `feature-planner` itself. See
  [[12-known-limitations|L30]] and
  `examples/workflow-composer/example-run.md`.

## Examples
See `examples/workflow-composer/example-run.md` — a real dogfood run
against this project's own current, fourteen-skill state.

## Provenance
Built in Phase 14, composing on `codebase-intelligence` (Phase 1) and
orchestrating `feature-planner` (Phase 4), `acceptance-test-engineer`
(Phase 3), and `context-optimizer` (Phase 13), at the user's explicit
direction — a fourth, one-time exception to the mentor-review roadmap
freeze, and the first to override a phase-specific decision on record
(`16-assumptions-and-validation.md` A10 — "do not build Workflow Composer
until Experiment B can be run") rather than only the general freeze (see
`project-memory-bank/active-context.md`, 2026-08-26). Not because A2/A5/A10
moved off `UNKNOWN`.

## Changelog
- 0.1.0 (2026-08-26): Initial release.
