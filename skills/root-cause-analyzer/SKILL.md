# Root Cause Analyzer

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/root-cause-analyzer/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a free-text symptom description (this skill's
  core value is judgment — diagnosing a failure — not just deterministic
  tooling)

## Purpose
Turn a bug report or failure description — with or without a stack trace —
into a ranked set of candidate root-cause locations grounded in a real
structural map of the target repository, plus an explicit investigation
(evidence tier, blast radius, ruled-out candidates, a confirmation step, and
fix risk) before any fix is proposed.

## Problem
Agents asked to "fix this bug" tend to jump straight to the file that
happens to look related, propose a fix, and never state how confident that
location actually is or how it was confirmed. This skill forces three things
to happen before a fix is proposed: (1) candidate locations are grounded in
a real, already-computed structural map of the repo (`codebase-
intelligence`'s report — a **required** input, reusing `feature-planner`'s
ADR-010 pattern a second time, see ADR-012) instead of guessed; (2) a real
stack trace, when present, is parsed and given a dominant, distinct evidence
tier over a mere keyword match, so a coincidental vocabulary overlap is
never presented with the same confidence as a runtime-confirmed location;
(3) the diagnosis is derived against a fixed 10-category checklist that
includes an explicit ruled-out-candidates category and an explicit
assumption-flag category, so uncertainty surfaces before a fix is written
rather than after.

## When to Use
- After a bug report, failure log, or stack trace arrives and before any fix
  is attempted — to turn a raw symptom into a short, reviewable list of
  candidate locations and an investigation plan.
- When a stack trace is available and you want the parsed frames checked
  against real repo structure, not eyeballed.
- As a `DIAGNOSE` step after `codebase-intelligence` (UNDERSTAND) —
  composition with `codebase-intelligence` is **required** here, same as
  `feature-planner` (see ADR-010 and ADR-012 in
  `project-memory-bank/11-decisions.md`).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill will refuse to run without one
  rather than silently guessing candidate locations.
- As a substitute for actually fixing the bug — this skill's output is an
  investigation packet (candidates + checklist), not a patch; `Confirm the
  root cause` (checklist category 8) must happen before any code change.
- As proof the named candidate *is* the root cause — a high-scoring
  candidate, even a stack-trace hit, is still a lead the top frame of a
  trace is often where the failure *surfaced*, not where the defect *is*
  (see Known Limitations).

## Preconditions
- Free-text symptom description available as a file or via stdin (a stack
  trace embedded in the text is optional but strengthens the result).
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010/ADR-012; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a symptom-description text file, or `-` to read
  from stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The symptom description AND a `codebase-intelligence` report for the target
repo are both required — this is the second skill in this platform where
composition is a hard precondition rather than optional context (ADR-010,
reused; see ADR-012). Optional composed context: recent diff/commit history
or release notes, if available, to ground the recent-change-correlation
category (6) in real evidence rather than the symptom text's own claims.

## Context Completeness
The deterministic engine's output is an investigation pre-processing aid:
symptom-quality flags on the description text, parsed stack-trace frames (if
any), and a candidate-location ranking of `codebase-intelligence`'s modules
against both stack-trace evidence and the symptom's keywords, annotated with
real fan-in/fan-out/hotspot blast-radius signal. It is not the diagnosis
itself — a stack-trace hit tells you where the failure surfaced, not
necessarily where the defect is, and keyword overlap is not semantic
understanding (see Known Limitations). The actual investigation happens in
Step 3, performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the
  `codebase-intelligence` report it reads.
- No network access; no external calls.
- Symptom text and stack traces may contain sensitive data pasted from logs
  (paths, usernames, occasionally tokens/PII if a log line included them).
  This skill does not scan or redact symptom text — if a symptom
  description may contain secrets/PII, run it through
  `security-context-guard` first (optional composition, not required here).

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010,
ADR-012).

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <symptom-file-or-'-'> --ci-report <report.json> --format both --out <output-dir>`
(from `skills/root-cause-analyzer/`).

### Step 3 — Investigate against the Root Cause Investigation checklist
Go through each of these categories explicitly for this symptom (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's symptom
flags and candidate report as leads, not the complete answer — most of these
categories cannot be regex-detected:
```
1. Symptom restated precisely             6. Recent-change correlation
2. Reproduction context (if stated)          (deploy/release timing)
3. Candidate locations — grounded in       7. Ruled-out candidates and why
   the candidate report, not guessed       8. Confirmation step before a fix
4. Evidence tier distinguished            9. Fix-risk note (hotspot/fan-in)
   (stack-trace vs. keyword)              10. Explicit assumption flag
5. Blast-radius / hotspot context             (evidence silent → state it,
                                               don't guess)
```
Category 10 is the honesty valve — same convention as
`feature-planner`'s Plan Quality checklist and
`acceptance-test-engineer`'s coverage checklist. A candidate report with
only keyword-tier matches (no stack-trace hit) means the location is a
lead, not a confirmed diagnosis — say so explicitly (category 4) rather
than presenting it with stack-trace-level confidence. Not every category
applies to every symptom (e.g. category 6 is N/A without a recent-change
signal) — state N/A explicitly rather than omitting the category silently.

### Step 4 — Produce the Root Cause Investigation Report
Structure: `{symptom, candidates: [{path, evidence_tier, rationale}],
ruled_out: [{path, reason}], confirmation_step, fix_risk_notes,
assumptions}`. Render as JSON plus a Markdown investigation packet a human
can review quickly. Do not apply the actual fix — this skill diagnoses, it
does not implement (that is `feature-planner`'s and the implementing
agent's job, downstream of this skill's output).

## Agent Responsibilities
- Never present a keyword-tier candidate with the same confidence language
  as a stack-trace-tier one — the report's `evidence_tier` field exists
  specifically so this distinction survives into the investigation.
- Never present an assumption as a derived fact — every place the evidence
  was silent or ambiguous, category 10 must name the assumption explicitly
  (see evaluation case-06: two candidates share the mechanism, and the
  report explicitly cannot narrow further without more evidence).
- Explicitly rule out a candidate that scores nonzero but does not fit the
  symptom's actual mechanism (see evaluation case-03 and case-06) — a
  nonzero score is not automatically a real lead.
- Distinguish a symptom-flag hit or a candidate score (mechanical pattern
  match) from an actual diagnosis (the agent's own judgment) in the report.

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for both `codebase-intelligence`
  and `root-cause-analyzer`) — read-only usage only.
- Read/Grep (to read composed context, e.g. recent commit history, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce an investigation report. A human should still
review and approve the proposed confirmation step and any resulting fix
before it ships, especially when the suspected location is a hotspot
(category 9) — this skill's output is an input to that decision, not a
substitute for it, same discipline as
`project-memory-bank/06-security-model.md` requires.

## Outputs
- `root-cause-report.json` — deterministic pre-investigation packet: stats,
  symptom flags, candidate report (see `engine/models.py`:
  `RootCauseReport`).
- `root-cause-report.md` — condensed version of the same.
- The agent's own **Root Cause Investigation Report** (Step 4), the actual
  diagnosis, is a separate artifact this skill's workflow produces, not
  emitted by the engine itself.

## Verification
- `pytest` (32 unit/integration/CLI tests as of v0.1.0, CLI test file
  written from the start — see `project-memory-bank/12-known-limitations.md`
  L10/L13) — see `tests/`.
- `evaluations/root-cause-analyzer/run_evaluation.py` against 8 fixture
  symptoms (deterministic symptom-flag + candidate layer) plus this
  session's actual investigation derivation for each (judgment layer) — see
  `evaluations/root-cause-analyzer/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/root-cause-analyzer/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic symptom-flags + candidate scoring (Correctness/Efficiency,
automated) and judgment-layer investigation-category findings (Precision/
Recall/False Positives/False Negatives against hand-authored expected
categories). The judgment-layer ground truth, fixtures, and actual
derivation were all produced by this same session's agent — self-authored,
single-rater evidence, not an inter-rater-agreement experiment. This is the
**fifth** judgment-based skill evaluated this way; treat the resulting
scores as evidence the workflow (including the required
codebase-intelligence composition) is executable and internally consistent,
not as evidence of real-world diagnostic quality. Unlike the four prior
skills, this one did **not** score perfect precision/recall on every
fixture (case-03 scored 0.67/0.67) — disclosed as-is, not adjusted to look
better. See `project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md`.

## Failure Conditions
- Symptom file does not exist or is unreadable → CLI exits non-zero with a
  clear stderr message.
- `--ci-report` path does not exist, is not valid JSON, or does not match
  the `CodebaseIntelligenceReport` schema → CLI exits non-zero with an
  actionable error naming the missing precondition (ADR-010/ADR-012) — this
  is a hard failure, not a degraded-but-working path.
- Empty symptom description → engine returns a report with a warning, not a
  hard error — the agent should flag this rather than deriving a diagnosis
  from nothing.
- A parsed stack-trace frame whose path matches no module in the report →
  the engine still returns keyword-tier candidates and adds an explicit
  warning; the agent must not treat this as if the trace had confirmed a
  location.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the symptom
anti-pattern list is not exhaustive (same shape as L7/L11); the stack-trace
parser covers two fixed shapes (Python tracebacks, generic `path:line`) and
will miss other languages' formats; a stack-trace hit confirms *where the
failure surfaced*, not necessarily *where the defect is* — the true root
cause is sometimes upstream of the top frame; the keyword-tier scorer has
the same coincidental-substring limitation as `feature-planner`'s relevance
scorer (see case-03's `app`/`worker` false leads, a real example of this,
correctly flagged as unreliable by agent judgment, not filtered by the
scorer); this is the fifth judgment-based skill with single-rater,
self-authored evaluation evidence, and the first of the five whose judgment
layer did not score perfectly on every fixture.

## Examples
See `examples/root-cause-analyzer/example-run.md` for a real run of this
skill: a freshly regenerated `codebase-intelligence` report against this
platform's current repository state, composed into a real symptom drawn
from this project's own dogfooding history.

## Provenance
Built in Phase 6 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven
workflow) a fifth time, and reusing `feature-planner`'s required-composition
rule (ADR-010) a second time, plus a new architectural decision (ADR-012)
introducing tiered evidence scoring (stack-trace confirmed vs. keyword
inferred) — see `project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of `codebase-intelligence` itself); the judgment layer is the
invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition), stack-trace parser (Python
  traceback + generic path:line shapes), tiered candidate-location scorer
  (stack-trace evidence dominant over keyword overlap, blast-radius
  annotation), symptom-quality anti-pattern table (vague symptom language,
  missing expected/actual, missing repro, missing error signal),
  JSON/Markdown renderers, CLI with a CLI test file written from the start,
  evaluation harness with 8 fixtures plus a real dogfood example.
