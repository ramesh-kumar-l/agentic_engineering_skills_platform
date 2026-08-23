# Refactoring Safety

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/refactoring-safety/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a free-text refactoring description (this
  skill's core value is judgment — weighing whether a refactor is safe —
  not just deterministic tooling)

## Purpose
Turn a free-text refactoring description — a rename, move, extract, inline,
delete, split, merge, or signature change — into a per-target risk
assessment grounded in a real structural map of the target repository: who
actually calls this, is it a real hotspot, and is it actually covered by a
real test, before the refactor is treated as safe to proceed.

## Problem
Agents asked to "refactor X" tend to narrate plausible-sounding safety
("this is a simple rename, shouldn't break anything") without checking who
actually depends on the thing being changed or whether a test would catch a
regression. This skill forces three things to happen before a refactor is
treated as safe: (1) the operation type and its real targets are parsed out
of the actual refactor text — quoted/backticked identifiers first, a
bare-identifier fallback second — rather than assumed; (2) each resolved
target's structural risk is scored against real `codebase-intelligence`
fan-in/hotspot data (a **required** input, reusing `feature-planner`'s,
`root-cause-analyzer`'s, and `architecture-decision`'s ADR-010 pattern a
fourth time — see ADR-014) instead of guessed, so a target with real callers
is never presented with the same confidence as one nobody depends on; (3) a
distinct, independently-computed test-coverage signal is checked against
that risk — a structurally risky target with no real covering test module
is flagged (`untested-blast-radius`) as unverified, not silently assumed
safe because the text sounds confident.

## When to Use
- Before executing a rename, move, extract, inline, delete, split, merge, or
  signature-change refactor, to check the real blast radius (real callers,
  hotspot status) and real test coverage against structural data, not
  eyeballed.
- Before recording a refactor as reviewed/approved — to surface a missing
  rollback plan, missing verification step, or an untested high-risk target
  first.
- As a safety gate after `codebase-intelligence` (UNDERSTAND) and before
  actually making the change (IMPLEMENT) — composition with
  `codebase-intelligence` is **required** here, same as `feature-planner`,
  `root-cause-analyzer`, and `architecture-decision` (see ADR-010 and
  ADR-014 in `project-memory-bank/11-decisions.md`).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill will refuse to run without one
  rather than silently guessing blast radius.
- As a substitute for actually performing or reviewing the refactor — this
  skill's output is a pre-decision packet (target risk + flags), not a
  verdict; nothing in the engine ever asserts the refactor is "safe" or
  "approved" (see Failure Conditions and
  `tests/test_report.py::test_report_never_fabricates_a_verdict`).
- As proof an unresolved target means the refactor names something fake —
  a target can fail to resolve because it's the **new** name in a rename
  (which legitimately doesn't exist yet, see evaluation case-01) or because
  the refactor genuinely names nothing real in the repository (case-06);
  the engine cannot tell these apart on its own.
- As proof a target's real `fan_in` count is the complete caller picture —
  see Known Limitations (L22): `codebase-intelligence`'s own dependency
  graph can undercount a real caller relative to this engine's own
  `caller_modules` scan when the caller uses an absolute-style cross-package
  import rather than a relative one (see
  `examples/refactoring-safety/example-run.md`).

## Preconditions
- Free-text refactoring description available as a file or via stdin
  (quoted/backticked target names are optional but resolve with higher
  confidence than the bare-identifier fallback).
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010/ADR-014; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a refactor-description text file, or `-` to
  read from stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The refactor description AND a `codebase-intelligence` report for the
target repo are both required — this is the fourth skill in this platform
where composition is a hard precondition rather than optional context
(ADR-010, reused by `root-cause-analyzer` a second time and
`architecture-decision` a third time, a fourth time here — see ADR-014).
Optional composed context: an existing test-run/CI log, if available, so the
agent's Step 3 walk can check real, current test-pass status rather than
only static test-file presence (this engine only checks whether a test
module imports the target, not whether that test currently passes).

## Context Completeness
The deterministic engine's output is a pre-decision aid: safety-quality
anti-pattern flags on the description text, a parsed operation type and
target list, and a per-target risk assessment against
`codebase-intelligence`'s real fan-in/hotspot data plus an independently-
computed test-coverage signal. It is not the safety verdict itself — a HIGH
risk tier tells you a target is structurally consequential, not that the
refactor is wrong; test coverage found tells you a module is imported by
something test-shaped, not that the test currently passes or exercises the
changed behavior (see Known Limitations). The actual safety judgment
happens in Step 3, performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the
  `codebase-intelligence` report it reads.
- No network access; no external calls.
- Refactor text may reference internal system names, module paths, or
  business context that is sensitive in some organizations. This skill
  does not scan or redact refactor text — if a refactor description may
  contain secrets/PII, run it through `security-context-guard` first
  (optional composition, not required here).

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010,
ADR-014).

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <refactor-file-or-'-'> --ci-report <report.json> --format both --out <output-dir>`
(from `skills/refactoring-safety/`).

### Step 3 — Walk the Refactoring Safety Checklist
Go through each of these categories explicitly for this refactor (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's safety
flags and per-target risk report as leads, not the complete answer — most of
these categories cannot be regex-detected:
```
1. Operation type stated precisely     6. Verification step stated (how
   (not a vague "refactor")               success will be confirmed)
2. Targets identified — real,          7. Behavioral equivalence / scope
   resolved against the report,           explicitly asserted (does this
   not invented                           refactor also change behavior,
3. Callers / blast radius assessed        or only structure?)
   from real fan-in data, not          8. Security implications
   guessed                                considered (or explicit N/A)
4. Test coverage verified per          9. Evidence cited, not opinion
   target — covered vs. genuinely     10. Explicit assumption flag
   untested distinguished, not            (evidence silent → state it,
   conflated                              don't guess)
5. Rollback / reversibility plan
   stated
```
Category 10 is the honesty valve — same convention as every prior
judgment-based skill's checklist in this project. An unresolved target
means the scorer found nothing to ground a risk assessment against, not
that the refactor is risk-free — say so explicitly (category 2/3) rather
than reading silence as safety, and distinguish "this is the expected-empty
new name in a rename" from "this names nothing real" (see evaluation
case-01 vs. case-06). Not every category applies to every refactor (e.g.
category 8 is legitimately N/A for many refactors) — state N/A explicitly
rather than omitting the category silently.

### Step 4 — Produce the Refactoring Safety Record
Structure: `{operation_type, targets: [{name, resolved_path,
risk_tier, callers, test_coverage, rollback_plan, verification_plan}],
scope_assertion, security_notes, go_no_go, assumptions}`. Render as JSON
plus a Markdown record a human can review quickly. This skill does not
decide go/no-go for the human — it produces the grounded material a human
(or the invoking agent, under human review) uses to record the actual call.

## Agent Responsibilities
- Never present a HIGH-risk, untested target and a LOW-risk, well-covered
  target as equally safe to proceed — the report's `risk_tier` and
  `test_coverage_modules` fields exist specifically so this distinction
  survives into the record (see evaluation case-02 vs. case-05).
- Never read "no test-plan mention in the text" as equivalent to "this
  target has no real test coverage" — these are independent signals that
  can and do diverge (see evaluation case-03, where the text never mentions
  tests but the codebase genuinely has real coverage).
- Never present an assumption as a derived fact — every place the refactor
  text was silent (no stated rollback, no stated verification), category 10
  must name the gap explicitly.
- Distinguish an unresolved target that is the **expected-absent new name**
  in a rename/move from one that names nothing real in the repository at
  all — the engine reports `resolved_module_path: null` identically either
  way; only the agent's Step 3 judgment, informed by `operation_type`, can
  tell them apart (see evaluation case-01 vs. case-06).
- Do not trust a target's `fan_in` number as the complete caller picture
  without also checking `caller_modules` — the two can diverge when
  `codebase-intelligence`'s own dependency graph misses an absolute-style
  cross-package import edge that this engine's own caller scan still finds
  (see Known Limitations L22).

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for both `codebase-intelligence`
  and `refactoring-safety`) — read-only usage only.
- Read/Grep (to read composed context, e.g. a CI log, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce a pre-decision report. A human should still
review and approve the actual refactor, especially when any target's risk
tier is HIGH or when `untested-blast-radius` fires — this skill's output is
an input to that review, not a substitute for it, same discipline as
`project-memory-bank/06-security-model.md` requires and every prior
judgment-based skill in this project applies to its own highest-risk
signal.

## Outputs
- `refactoring-safety-report.json` — deterministic pre-decision packet:
  stats, safety flags, per-target risk assessment (see `engine/models.py`:
  `RefactoringSafetyReport`).
- `refactoring-safety-report.md` — condensed version of the same.
- The agent's own **Refactoring Safety Record** (Step 4), the actual
  go/no-go judgment, is a separate artifact this skill's workflow produces,
  not emitted by the engine itself.

## Verification
- `pytest` (62 unit/integration/CLI tests as of v0.1.0, CLI test file
  written from the start — see `project-memory-bank/12-known-limitations.md`
  L10/L13) — see `tests/`.
- `evaluations/refactoring-safety/run_evaluation.py` against 8 fixture
  refactors (deterministic safety-flag + target-risk layer) plus this
  session's actual checklist derivation for each (judgment layer) — see
  `evaluations/refactoring-safety/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/refactoring-safety/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic safety-flag + risk-tier scoring (Correctness/Efficiency,
automated) and judgment-layer checklist-category findings (Precision/
Recall/False Positives/False Negatives against hand-authored expected
categories). The judgment-layer ground truth, fixtures, and actual
derivation were all produced by this same session's agent — self-authored,
single-rater evidence, not an inter-rater-agreement experiment. This is the
**seventh** judgment-based skill evaluated this way; treat the resulting
scores as evidence the workflow (including the required
codebase-intelligence composition) is executable and internally consistent,
not as evidence of real-world refactoring-safety judgment quality. All 8
fixtures scored perfect precision/recall — disclosed as-is, same as five of
the six prior judgment-based skills; `root-cause-analyzer` remains the one
exception (case-03, 0.67/0.67), and that is stated here rather than implied
away. See `project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md`.

## Failure Conditions
- Refactor description file does not exist or is unreadable → CLI exits
  non-zero with a clear stderr message.
- `--ci-report` path does not exist, is not valid JSON, or does not match
  the `CodebaseIntelligenceReport` schema → CLI exits non-zero with an
  actionable error naming the missing precondition (ADR-010/ADR-014) — this
  is a hard failure, not a degraded-but-working path.
- Empty refactor description → engine returns a report with a warning, not
  a hard error — the agent should flag this rather than assessing a
  refactor from nothing.
- No target identifiers parsed → the engine adds an explicit warning; the
  agent must not treat this as evidence the refactor is safe, only as
  evidence nothing could be structurally assessed.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the safety
anti-pattern list is not exhaustive (same shape as L7/L11/L18); an
unresolved target can mean "this is the expected-absent new name in a
rename" OR "the refactor text never named a real target" — the engine
cannot distinguish these, only the agent's Step 3 judgment can (evaluation
case-01 vs. case-06); test-coverage detection is a static-import heuristic
(a test module imports the target), not proof the test currently passes or
exercises the changed code path; and the real dogfood run
(`examples/refactoring-safety/example-run.md`) found and disclosed (without
fixing, since it originates in a different skill) L22 — `codebase-
intelligence`'s own `fan_in` count can undercount a real caller relative to
this engine's own `caller_modules` list, when that caller uses an
absolute-style cross-package import that `codebase-intelligence`'s
dependency-graph builder does not recognize as an edge. This is the seventh
judgment-based skill with single-rater, self-authored evaluation evidence.

## Examples
See `examples/refactoring-safety/example-run.md` for a real run of this
skill: a freshly regenerated `codebase-intelligence` report against this
platform's current (8-skill) repository state, composed into a real
refactor this project's own Phase 8 build actually produced (a duplicated
path-stem helper across two of this skill's own engine modules) — including
a real, disclosed cross-skill limitation (L22) it did not fix.

## Provenance
Built in Phase 8 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven
workflow) a seventh time, and reusing `feature-planner`'s/
`root-cause-analyzer`'s/`architecture-decision`'s required-composition rule
(ADR-010) a fourth time, plus a new architectural decision (ADR-014)
introducing per-target risk tiering that combines real fan-in/hotspot data
with an independently-computed test-coverage signal, kept as two distinct
fields rather than blended into one score — see
`project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of `codebase-intelligence` itself); the judgment layer is the
invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition), operation/target parser
  (backtick/quote-first, bare-identifier fallback, 8 fixed operation
  types), target resolver (module-stem, function-name, class-name
  matching, real caller lookup via import scan), test-coverage scanner
  (static import-based heuristic), per-target risk scorer (boundary-
  changing vs. internal-only operation bands, fan-in/hotspot-driven,
  distinct `untested-blast-radius` flag rather than a blended score),
  safety-quality anti-pattern table (vague refactor language, missing test
  plan, missing rollback, missing caller-update mention, missing
  verification step), JSON/Markdown renderers, CLI with a CLI test file
  written from the start, evaluation harness with 8 fixtures plus a real
  dogfood example that disclosed a real cross-skill limitation (L22)
  without fixing it.
