# Architecture Decision

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/architecture-decision/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a free-text decision description (this skill's
  core value is judgment — weighing a decision — not just deterministic tooling)

## Purpose
Turn a free-text architecture-decision description — with or without
explicitly named alternatives — into a per-option blast-radius assessment
grounded in a real structural map of the target repository, plus an
explicit decision-record walk (context, alternatives, consequences,
reversibility, evidence) before the decision is treated as final.

## Problem
Agents asked to "decide how to build X" tend to reason about one path,
narrate plausible-sounding tradeoffs, and never check whether the change
actually touches a structurally consequential part of the codebase. This
skill forces three things to happen before a decision is treated as
recorded: (1) candidate alternatives are parsed out of the actual decision
text — explicit `Option A:` markers, a numbered/lettered list, or a
`vs`/`versus` split — rather than invented by the agent; (2) each option's
blast radius is scored against real `codebase-intelligence` structural data
(a **required** input, reusing `feature-planner`'s and
`root-cause-analyzer`'s ADR-010 pattern a third time — see ADR-013) instead
of guessed, so an option that touches a real hotspot is never presented
with the same confidence as one that touches nothing real; (3) the decision
is walked against a fixed 10-category Architecture Decision Record
checklist that includes an explicit reversibility category and an explicit
honesty-valve category, so gaps (missing tradeoffs, missing security
consideration, an ungrounded option) surface before the decision ships
rather than after.

## When to Use
- When two or more real alternatives are being weighed and you want each
  one's structural blast radius checked against real dependency data, not
  eyeballed.
- Before recording a decision as an ADR entry (this project's own
  `project-memory-bank/11-decisions.md` format, or any equivalent) — to
  surface missing tradeoffs, missing reversibility discussion, or an
  ungrounded option first.
- As a `DECIDE` step after `codebase-intelligence` (UNDERSTAND) —
  composition with `codebase-intelligence` is **required** here, same as
  `feature-planner` and `root-cause-analyzer` (see ADR-010 and ADR-013 in
  `project-memory-bank/11-decisions.md`).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill will refuse to run without one
  rather than silently guessing blast radius.
- As a substitute for actually making the decision — this skill's output is
  a pre-decision packet (option impacts + flags), not a verdict; nothing in
  the engine ever names a "chosen" or "recommended" option (see Failure
  Conditions and `tests/test_integration.py::test_report_never_fabricates_a_verdict`).
- As proof a high blast-radius score means "wrong" or a low one means
  "safe" — a zero-match option can mean genuinely low-impact, or it can
  mean the decision text never named its real target (see Known
  Limitations, and case-04/case-05 in `evaluations/architecture-decision/`
  for the contrast).
- On a decision whose text is itself about this project's own architecture
  at large — the keyword scorer's blast-radius signal degrades badly when
  the decision's vocabulary overlaps the whole repo's own vocabulary (see
  `examples/architecture-decision/example-run.md`).

## Preconditions
- Free-text decision description available as a file or via stdin
  (explicitly named alternatives are optional but strengthen the result).
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010/ADR-013; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a decision-description text file, or `-` to
  read from stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The decision description AND a `codebase-intelligence` report for the
target repo are both required — this is the third skill in this platform
where composition is a hard precondition rather than optional context
(ADR-010, reused a second time by `root-cause-analyzer`, a third time here
— see ADR-013). Optional composed context: an existing ADR log (this
project's `project-memory-bank/11-decisions.md` or an equivalent), if
available, so the agent's Step 3 walk can check for precedent rather than
treating every decision as unprecedented.

## Context Completeness
The deterministic engine's output is a pre-decision aid: decision-quality
anti-pattern flags on the description text, parsed options (explicit
markers, list items, or a vs-split fallback), and a per-option blast-radius
assessment against `codebase-intelligence`'s real fan-in/fan-out/hotspot
data. It is not the decision itself — a high blast-radius score tells you
an option touches structurally consequential code, not that the option is
wrong; a zero-match option tells you the scorer found nothing, not that the
option is safe (see Known Limitations). The actual decision happens in
Step 3, performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the
  `codebase-intelligence` report it reads.
- No network access; no external calls.
- Decision text may reference internal system names, module paths, or
  business context that is sensitive in some organizations. This skill
  does not scan or redact decision text — if a decision description may
  contain secrets/PII, run it through `security-context-guard` first
  (optional composition, not required here).

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010,
ADR-013).

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <decision-file-or-'-'> --ci-report <report.json> --format both --out <output-dir>`
(from `skills/architecture-decision/`).

### Step 3 — Walk the Architecture Decision Record checklist
Go through each of these categories explicitly for this decision (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's
decision flags and option-impact report as leads, not the complete answer —
most of these categories cannot be regex-detected:
```
1. Context stated precisely                6. Blast radius grounded in
2. Alternatives identified — real,             real structural data, not
   grounded in what was parsed, not             assumed
   invented                                  7. Security implications
3. Decision explicitly stated                   considered (or explicit
4. Consequences / tradeoffs stated,             N/A)
   per option, not one-sided               8. Evidence cited, not opinion
5. Reversibility assessed per option        9. Future evolution / revisit
                                                trigger stated
                                             10. Explicit assumption flag
                                                 (evidence silent → state
                                                 it, don't guess)
```
Category 10 is the honesty valve — same convention as every prior
judgment-based skill's checklist in this project. An option with zero
matched modules means the scorer found nothing, not that the option is
risk-free — say so explicitly (category 6) rather than reading silence as
safety, the same discipline `root-cause-analyzer`'s checklist applies to a
keyword-only candidate. Not every category applies to every decision (e.g.
category 7 is legitimately N/A for many decisions) — state N/A explicitly
rather than omitting the category silently.

### Step 4 — Produce the Architecture Decision Record
Structure: `{context, options: [{label, consequences, reversibility,
blast_radius_assessment}], decision, rationale, security_notes,
revisit_trigger, assumptions}`. Render as JSON plus a Markdown record a
human can review quickly. This skill does not choose the option for the
human — it produces the grounded material a human (or the invoking agent,
under human review) uses to record the actual choice.

## Agent Responsibilities
- Never present a high blast-radius option and a zero-match option as
  equally confident assessments — the report's `blast_radius_tier` and
  `impacted_modules` fields exist specifically so this distinction survives
  into the record (see evaluation case-04).
- Never read an empty `impacted_modules` list as "this option is safe" —
  distinguish "genuinely low-impact" (evaluation case-05) from "the
  decision text never named its real target" (evaluation case-04's Option
  B) explicitly, in every record.
- Never present an assumption as a derived fact — every place the decision
  text was silent (no stated tradeoff, no stated reversibility, no security
  mention), category 10 must name the gap explicitly.
- At full-repository scale, sanity-check a blast-radius score before
  trusting it — if a decision's own vocabulary overlaps the target repo's
  vocabulary broadly (e.g. a decision about this platform's own
  architecture), the keyword scorer's signal degrades (see Known
  Limitations and `examples/architecture-decision/example-run.md`).

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for both `codebase-intelligence`
  and `architecture-decision`) — read-only usage only.
- Read/Grep (to read composed context, e.g. an existing ADR log, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce a pre-decision report. A human should still
review and approve the recorded decision itself, especially when any
option's blast radius is HIGH (touches a hotspot) — this skill's output is
an input to that decision, not a substitute for it, same discipline as
`project-memory-bank/06-security-model.md` requires and `root-cause-analyzer`
applies to a suspected-hotspot fix location.

## Outputs
- `architecture-decision-report.json` — deterministic pre-decision packet:
  stats, decision flags, per-option impact report (see `engine/models.py`:
  `ArchitectureDecisionReport`).
- `architecture-decision-report.md` — condensed version of the same.
- The agent's own **Architecture Decision Record** (Step 4), the actual
  decision, is a separate artifact this skill's workflow produces, not
  emitted by the engine itself.

## Verification
- `pytest` (34 unit/integration/CLI tests as of v0.1.0, CLI test file
  written from the start — see `project-memory-bank/12-known-limitations.md`
  L10/L13) — see `tests/`.
- `evaluations/architecture-decision/run_evaluation.py` against 8 fixture
  decisions (deterministic decision-flag + option-impact layer) plus this
  session's actual decision-record derivation for each (judgment layer) —
  see `evaluations/architecture-decision/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/architecture-decision/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic decision-flag + blast-radius scoring (Correctness/Efficiency,
automated) and judgment-layer decision-record-category findings (Precision/
Recall/False Positives/False Negatives against hand-authored expected
categories). The judgment-layer ground truth, fixtures, and actual
derivation were all produced by this same session's agent — self-authored,
single-rater evidence, not an inter-rater-agreement experiment. This is the
**sixth** judgment-based skill evaluated this way; treat the resulting
scores as evidence the workflow (including the required
codebase-intelligence composition) is executable and internally consistent,
not as evidence of real-world decision quality. All 8 fixtures scored
perfect precision/recall — disclosed as-is, same as four of the five prior
skills; `root-cause-analyzer` remains the one exception (case-03,
0.67/0.67), and that is stated here rather than implied away. See
`project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md`.

## Failure Conditions
- Decision file does not exist or is unreadable → CLI exits non-zero with a
  clear stderr message.
- `--ci-report` path does not exist, is not valid JSON, or does not match
  the `CodebaseIntelligenceReport` schema → CLI exits non-zero with an
  actionable error naming the missing precondition (ADR-010/ADR-013) — this
  is a hard failure, not a degraded-but-working path.
- Empty decision description → engine returns a report with a warning, not
  a hard error — the agent should flag this rather than deriving a decision
  from nothing.
- No explicit alternatives parsed → the engine falls back to a single
  "proposed" option and adds an explicit warning; the agent must not treat
  this as a comparison that was actually made.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the decision
anti-pattern list is not exhaustive (same shape as L7/L11/L18); an option
with zero matched modules can mean genuinely low-impact OR that the
decision text never named a real target — the engine cannot distinguish
these, only the agent's Step 3 judgment can; the keyword-tier impact
scorer has the same coincidental-substring/shared-path-prefix limitation as
`feature-planner`'s relevance scorer (L14) and `root-cause-analyzer`'s
candidate scorer (L19) — demonstrated here by evaluation case-01/case-05
(a shared `engine/` path prefix inflates blast radius) and, far more
sharply, by the real dogfood run (`examples/architecture-decision/
example-run.md`), where a decision *about this platform's own
architecture* produced a nearly-uninformative blast-radius signal because
the decision text's vocabulary overlaps the whole repo's vocabulary; this
is the sixth judgment-based skill with single-rater, self-authored
evaluation evidence.

## Examples
See `examples/architecture-decision/example-run.md` for a real run of this
skill: a freshly regenerated `codebase-intelligence` report against this
platform's current (7-skill) repository state, composed into a real
decision this project's own Phase 7 build actually faced — including a
real bug the dogfood run found and fixed in the tool itself (a tradeoff-verb
phrasing gap) and a real, disclosed limitation it did not fix (blast-radius
noise at full-repo scale).

## Provenance
Built in Phase 7 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven
workflow) a sixth time, and reusing `feature-planner`'s/`root-cause-analyzer`'s
required-composition rule (ADR-010) a third time, plus a new architectural
decision (ADR-013) introducing per-option blast-radius scoring against real
dependency-graph data — see `project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of `codebase-intelligence` itself); the judgment layer is the
invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition), option parser (explicit
  markers, numbered/lettered lists, vs-split fallback), per-option
  blast-radius scorer (keyword relevance rolled up into a three-tier
  structural risk band using real fan-in/fan-out/hotspot data),
  decision-quality anti-pattern table (vague decision language, missing
  alternatives, missing reversibility, missing tradeoff, missing security
  signal), JSON/Markdown renderers, CLI with a CLI test file written from
  the start, evaluation harness with 8 fixtures plus a real dogfood example
  that found and fixed a real gap in the tradeoff-detection regex.
