---
name: test-case-generator
description: Generates positive and negative test cases for staged (git add) or diffed source changes by running this platform's codebase-intelligence -> regression-hunter -> project-intelligence -> test-strategy -> scenario-planner -> test-generation pipeline in one call, then authors and validates the test files via the target project's own build tool. Use when asked to "generate test cases for staged changes", "write tests for this diff", or similar.
---

# Test Case Generator

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 1 — New Skill (no evaluation run yet)
- Compatible Runtimes: Claude Code (native skill — see Provenance). Any other
  agent runtime with Bash/shell tool access and Python 3.10+ can still call
  `engine/cli.py` directly; only the auto-load-on-prompt behavior is
  Claude-Code-specific.

## Purpose
Turn "generate test cases for the staged changes" into one command: run the
existing 6-stage TEP pipeline (`codebase-intelligence`, `regression-hunter`,
`project_intelligence`, `test_strategy`, `scenario_planner`,
`test_generation`) against a repo's `git diff --staged`, author the resulting
test file(s) with 1 positive + 5 negative cases per flagged target, then run
the project's own build tool and self-fix on failure (max 2 retries).

## Problem
Today those 6 stages must be run as 6 separate manual commands, each
threading the previous stage's `--out` path into the next by hand (see
`AndroidGuide.md` §3.3) — accurate, but not a one-shot "generate tests for
what I just staged" experience, and nothing in this platform authors the
actual test file, runs it, or retries on failure. This skill closes that gap
at the *agentic* layer (this skill's own instructions), not by rewriting the
deterministic engines.

## When to Use
- After `git add`-ing a real code change, when you want tests generated for
  exactly what you staged.
- On a legacy repo with no other test-authoring workflow in place — this
  works from a diff, not from prior test conventions.

## When NOT to Use
- Whole-codebase "generate full coverage" requests — this is diff-driven;
  with nothing staged, there is nothing to plan (see Failure Conditions).
- As a substitute for real code review — the generated tests are grounded in
  a source excerpt and a deterministic plan, not a correctness guarantee.

## Preconditions
- A local git repo with a non-empty `git diff --staged`.
- Python 3.10+ available in the execution environment.
- `TEP_PLATFORM_ROOT` set to this platform's checkout, when this skill is
  installed into a repo other than this one (see Provenance → Install).
  Falls back to this file's own checkout location when unset.
- The target repo's own build tool (e.g. Gradle) available on PATH, for the
  build/retry step — this skill does not install or invoke Gradle itself
  beyond what Claude runs via Bash at authoring time.

## Inputs
- `repo_path` (required, positional to `engine/cli.py`): path to the target
  repo.
- `--diff-file` (optional): use a specific diff file instead of
  `git diff --staged`.
- `--out` (required): directory to write all 6 stages' outputs into.

## Required Context
None beyond the target repo path — this skill re-derives everything from the
pipeline's own outputs, matching `codebase-intelligence`'s existing
"reduce reliance on prior conversation context" design.

## Context Completeness
`engine/cli.py` produces a deterministic `generation-plan-report.json`: which
file/symbol to test, a source excerpt, a naming convention, and 1 positive +
5 negative slot instructions per target (`test_generation`'s fixed
`NEGATIVE_SLOT_COUNT`). Everything past that point — authoring the actual
test file, running the build, and fixing failures — is Claude's own runtime
judgment, not deterministic output.

## Security Constraints
- `engine/cli.py` itself is read-only against the target repo (it only runs
  the existing read-only pipeline stages) — it writes only under `--out`.
- The build/retry step (Step 4 below) does modify the target repo: it
  authors new test file(s) and may edit them again during a retry. It never
  edits the source under test unless a retry attempt explicitly determines
  the failure is a plan/instruction error, not a real regression — and even
  then, this is Claude's judgment call, not a scripted rule.
- No network access; no external calls anywhere in `engine/`.

## Workflow
### Step 1 — Confirm there is something to test
Run `git diff --staged` in the target repo. If empty, tell the user and stop
— do not fall back to an unstaged or historical diff silently.

### Step 2 — Run the orchestrator
```
python -m engine.cli <repo> --out <tmp-out-dir>
```
(from `skills/test-case-generator/`, or from wherever this skill was
installed — see Provenance → Install). This runs all 6 stages for real and
writes `generation-plan-report.json` under `<tmp-out-dir>/tg/`.

### Step 3 — Author the test file(s)
For each `TargetGenerationSpec` in the report: write one test file covering
the `positive_slot` and all 5 `negative_slots`, following `naming_convention`
and grounded only in `source_excerpt` — never fabricate beyond what the
excerpt supports (the plan's own instruction text says this explicitly). If
the real source excerpt cannot support 5 genuinely distinct negative
conditions, author fewer and say so rather than duplicate a case — the
plan's own instructions already say this per slot.

### Step 4 — Build, test, and self-fix
Run the target project's real build/test task via Bash (e.g. `./gradlew
test`, or a module-specific task detected from `build.gradle`; `pytest` for a
Python target). On failure: read the failure output, fix the authored test
(or note plainly when the failure looks like a real regression rather than a
bad test), and retry. **Maximum 2 total attempts** — stop and report clearly
if still failing after that.

### Step 5 — Report
Summarize pass/fail per target, and explicitly flag any target whose
`source_excerpt_available` was `false`, or whose upstream
`test-environment-profile.json` carried a framework-detection warning (see
Known Limitations, L35).

## Agent Responsibilities
- Never claim a generated test "proves" correctness — it proves the plan's
  scenario passed against the current code, nothing more.
- Stop at 2 retry attempts even if still failing — do not silently continue
  past the stated limit.

## Tool Permissions
- Bash (to invoke `python -m engine.cli`, and to run the target project's
  build/test tool).
- Read/Edit (to read the generation plan and author/fix the test file(s)).
No network or credential-accessing permissions are required or granted. 

## Human Checkpoints
None required to generate and locally run tests. Committing or pushing the
authored test file(s) is a separate, explicit user decision — this skill
never commits on its own.

## Outputs
- `<out>/tg/generation-plan-report.json` — the deterministic plan (unchanged
  schema from `test_generation.models.GenerationPlanReport`).
- The authored `.kt`/`.java`/`.py` test file(s) in the target repo (written
  by Claude, not by `engine/`).
- A local build/test result per target, from the real build tool.

## Verification
- `pytest` (`tests/test_pipeline_integration.py`) — builds a real, minimal
  git repo with one staged change and runs `engine.cli` against it
  end-to-end, asserting a valid, non-empty `generation-plan-report.json`
  comes out the other side. This proves the orchestrator's wiring; it cannot
  and does not test Step 3–5's agentic behavior (see Known Limitations).

## Evaluation
Not yet run through this platform's evaluation framework
(`project-memory-bank/05-evaluation-framework.md`) — Maturity is capped at
Level 1 pending a real dogfood run against one of the target Android repos.

## Failure Conditions
- No staged diff → `engine/cli.py` exits non-zero with a clear stderr
  message; the skill must not substitute an unstaged diff silently.
- Any of the 6 subprocess stages exits non-zero → the whole call fails with
  that stage's real stderr surfaced (`PipelineStageError`), not swallowed.
- Build/retry failure after 2 attempts → reported as failing, not retried
  further and not silently marked passing.

## Known Limitations
- **Diff-driven, not whole-app coverage** — same limitation as the rest of
  the TEP pipeline. No staged diff means no plan.
- **Gradle-based test-framework detection under-reports** on real Android
  repos (known limitation L35, `project-memory-bank/12-known-limitations.md`)
  — Step 5's framework-detection-warning flag exists because of this; do not
  treat "framework unavailable" as ground truth for a real Android target.
- **No automated check exists, or can exist, for whether Claude actually
  followed Steps 3–5 correctly** — that part is verified by manual dry run
  only (see Verification), same as this platform's other agent-judgment
  boundaries (ADR-005/007).

## Examples
See `AndroidGuide.md` §3.3/3.5 for the equivalent 6 manual commands this
skill's `engine/cli.py` now runs in one call.

## Provenance
Built as the platform's **first native Claude Code skill** — every other
`SKILL.md` in this portfolio is deliberately frontmatter-free, portable
Markdown (ADR-002), not yet proven machine-parseable
(`project-memory-bank/16-assumptions-and-validation.md`). This file's YAML
frontmatter is a documented, deliberate exception to that stance, made at
explicit user request, not a silent departure from the convention.

`project_intelligence/`, `test_strategy/`, `scenario_planner/`,
`skills/codebase-intelligence/`, and `skills/regression-hunter/` are
untouched — this skill only adds a new orchestrator that calls their
existing CLIs as subprocesses. `test_generation/generation_planner.py`'s
`NEGATIVE_SLOT_COUNT` was changed from its original fixed value of 4 to 5,
at explicit user request, so the deterministic plan itself now requests the
full 5 negative slots — no agent-side top-up is needed.

### Install (into a repo other than this platform's own)
```bash
git clone <this-platform-repo-url> ~/tools/agentic_engineering_skills_platform
export TEP_PLATFORM_ROOT=~/tools/agentic_engineering_skills_platform   # add to shell profile, once
mkdir -p ~/.claude/skills
cp -r "$TEP_PLATFORM_ROOT/skills/test-case-generator" ~/.claude/skills/
```
User-level `~/.claude/skills/` is recommended when reusing this across
multiple target repos (e.g. 3 separate Android projects) that all share one
platform checkout. In the target repo: `git add <files>`, then ask Claude
Code "Generate test cases for the staged changes."

## Changelog
- 0.1.0 — Initial implementation: `engine/pipeline.py` (6-stage subprocess
  chain), `engine/staged_diff.py` (git diff --staged resolution),
  `engine/cli.py`, and a real end-to-end integration test.
