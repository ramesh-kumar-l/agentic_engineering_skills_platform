# Feature Planner

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/feature-planner/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a free-text task description (this skill's
  core value is judgment — deriving a structured plan — not just deterministic
  tooling)

## Purpose
Turn a vague-to-moderately-specified engineering task into an explicit,
structured plan — scope, affected files, ordered steps, risk, rollback, test
hook, security touchpoints, dependencies, and assumptions — grounded in a
real structural map of the target repository, before implementation starts.

## Problem
Agents asked to "just implement X" tend to guess which files are affected
from filenames or intuition, silently resolve scope ambiguity in whatever way
is easiest, and skip stating a rollback or verification strategy unless asked.
This skill forces two things to happen before implementation: (1) affected
files are grounded in a real, already-computed structural map of the repo
(`codebase-intelligence`'s report — a **required** input, not an optional
nicety, see ADR-010) instead of guessed; (2) the plan is derived against a
fixed 10-category checklist that includes an explicit non-goals section and
an explicit assumption-flag category, so ambiguity surfaces before code is
written rather than after.

## When to Use
- Before implementing a new feature or non-trivial change, to turn a vague
  task description into a plan a human can review in under a minute.
- When you need to know which real files a change will touch — not a guess,
  but a relevance ranking grounded in actual imports/defs/dependency data.
- As the `PLAN` step after `codebase-intelligence` (UNDERSTAND) — composition
  with `codebase-intelligence` is **required** here, unlike the optional
  composition `adversarial-diff-reviewer` and `acceptance-test-engineer`
  offer (see ADR-010 in `project-memory-bank/11-decisions.md`).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill will refuse to run without one
  rather than silently guessing affected files.
- As a substitute for `acceptance-test-engineer` — this skill's "test hook"
  category states *that* verification is needed and roughly what it should
  check, not a full acceptance-criteria derivation.
- As proof a plan is "approved" — a structured plan existing is not the same
  as a human/stakeholder having reviewed and signed off on it.

## Preconditions
- Free-text task-description input available as a file or via stdin.
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a task-description text file, or `-` to read
  from stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The task description AND a `codebase-intelligence` report for the target
repo are both required — this is the first skill in this platform where
composition is a hard precondition rather than optional context (ADR-010).
Optional composed context: `acceptance-test-engineer`'s output, if available,
to ground the "test hook" category in real derived acceptance criteria
rather than a one-line guess.

## Context Completeness
The deterministic engine's output is a planning pre-processing aid: planning-
anti-pattern flags on the task text, and a relevance ranking of
`codebase-intelligence`'s modules against the task's keywords, annotated with
real fan-in/fan-out/hotspot blast-radius signal. It is not the structured
plan itself — relevance is keyword overlap, not semantic understanding (see
Known Limitations), and the actual plan authoring happens in Step 3,
performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the
  `codebase-intelligence` report it reads.
- No network access; no external calls.
- Task descriptions may describe security-sensitive changes (auth,
  permissions, data handling) — this skill's category 8 (security/permission
  touchpoint) exists specifically to surface that into an explicit plan item
  rather than letting it stay implicit.

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010).

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <task-file-or-'-'> --ci-report <report.json> --format both --out <output-dir>`
(from `skills/feature-planner/`).

### Step 3 — Derive the structured plan against the Plan Quality checklist
Go through each of these categories explicitly for this task (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's planning
flags and relevance report as leads, not the complete answer — most of these
categories cannot be regex-detected:
```
1. Scope statement (goal/deliverable)     6. Rollback/reversibility per risky step
2. Explicit non-goals / out-of-scope      7. Test/acceptance-criteria hook
3. Affected files — grounded in the       8. Security/permission touchpoints
   relevance report, not guessed          9. Dependencies & blockers
4. Ordered step sequence, each step      10. Explicit assumption flag (context
   independently verifiable                 silent → state it, don't guess)
5. Risk & blast-radius assessment
   (fan-in/fan-out/hotspot signal)
```
Category 10 is the honesty valve — same convention as
`acceptance-test-engineer`'s coverage checklist and
`adversarial-diff-reviewer`'s failure-first checklist. A relevance score of
zero for every module (see `report.warnings`) means affected files must be
stated as an assumption, not force-fit onto the least-irrelevant match. Not
every category applies to every task (e.g. category 7/8 may be N/A) — state
N/A explicitly rather than omitting the category silently.

### Step 4 — Produce the Feature Planning Report
Structure: `{scope, non_goals, steps: [{id, description, affected_files,
risk, rollback, verification}], assumptions, security_notes}`. Render as JSON
plus a Markdown plan a human can review quickly. Do not generate the actual
code change — this skill plans, it does not implement.

## Agent Responsibilities
- Never present an assumption as a derived fact — every place the task
  description was silent, category 10 must name the assumption explicitly.
- Never list a file as "affected" without grounding it in the relevance
  report's real keyword-overlap evidence or an explicitly disclosed
  assumption — a nonzero relevance score is not automatically in-scope
  either (see evaluation case-02: a file can score high and still be an
  explicit non-goal).
- Distinguish a planning-flag hit (mechanical pattern match) or a relevance
  score (mechanical keyword overlap) from an actual plan decision (the
  agent's own judgment) in the report.

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for both `codebase-intelligence`
  and `feature-planner`) — read-only usage only.
- Read/Grep (to read composed context, e.g. `acceptance-test-engineer`
  output, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce a plan. A human should still review and approve the
plan before implementation begins, especially for any step flagged
high-risk (category 5) or touching a security boundary (category 8) — this
skill's output is an input to that decision, not a substitute for it, same
discipline as `project-memory-bank/06-security-model.md` requires.

## Outputs
- `feature-planning-report.json` — deterministic pre-planning packet: stats,
  planning flags, relevance report (see `engine/models.py`:
  `FeaturePlanningReport`).
- `feature-planning-report.md` — condensed version of the same.
- The agent's own **Feature Planning Report** (Step 4), the actual structured
  plan, is a separate artifact this skill's workflow produces, not emitted by
  the engine itself.

## Verification
- `pytest` (21 unit/integration tests as of v0.1.0) — see `tests/`.
- `evaluations/feature-planner/run_evaluation.py` against 8 fixture tasks
  (deterministic planning-flag + relevance layer) plus this session's actual
  plan derivation for each (judgment layer) — see
  `evaluations/feature-planner/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/feature-planner/` for the full case set. Two layers scored
separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic planning-flags + relevance scoring (Correctness/Efficiency,
automated) and judgment-layer plan-category findings (Precision/Recall/False
Positives/False Negatives against hand-authored expected categories). The
judgment-layer ground truth, fixtures, and actual derivation were all
produced by this same session's agent — self-authored, single-rater
evidence, not an inter-rater-agreement experiment. This is the **third**
judgment-based skill evaluated this way; treat the resulting scores as proof
the workflow (including the required codebase-intelligence composition) is
executable and internally consistent, not as evidence of real-world planning
quality. See `project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md` A5/A10.

## Failure Conditions
- Task file does not exist or is unreadable → CLI exits non-zero with a
  clear stderr message.
- `--ci-report` path does not exist, is not valid JSON, or does not match
  the `CodebaseIntelligenceReport` schema → CLI exits non-zero with an
  actionable error naming the missing precondition (ADR-010) — this is a
  hard failure, not a degraded-but-working path.
- Empty task description → engine returns a report with a warning, not a
  hard error — the agent should flag this rather than deriving a plan from
  nothing.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the planning
anti-pattern list is not exhaustive (same shape as L7/L11); the relevance
scorer is keyword-overlap only, with no semantic understanding — it will
miss a genuinely relevant file that happens to use different vocabulary than
the task description, and can surface an irrelevant file that happens to
share vocabulary (case-02's excluded `import_cli.py` is a real example of
the latter, correctly excluded by agent judgment, not by the scorer); this
is the third judgment-based skill with single-rater, self-authored
evaluation evidence.

## Examples
See `examples/feature-planner/example-run.md` for a real run of this skill:
a freshly regenerated `codebase-intelligence` report against this
platform's current repository state, composed into a real planning task.

## Provenance
Built in Phase 4 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven workflow)
a third time, plus a new architectural decision (ADR-010) making composition
with `codebase-intelligence` a required precondition rather than optional
context — see `project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of `codebase-intelligence` itself); the judgment layer is the
invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition), keyword-overlap relevance
  scorer with blast-radius annotation, planning anti-pattern table (vague
  scope, weak goal modals, scope-boundary/verification absence checks),
  JSON/Markdown renderers, CLI, evaluation harness with 8 fixtures plus a
  real repo-wide dogfood example.
