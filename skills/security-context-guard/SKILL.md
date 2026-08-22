# Security Context Guard

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/security-context-guard/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access and Python
  3.10+ (this skill's core value is judgment — recommending whether an action
  needs human approval — not just deterministic tooling)

## Purpose
Classify content that is about to be exposed to a tool, an agent's context
window, or an external system; minimize and sanitize (redact) any secret/PII
matches found; and produce a recommendation — never a self-executed decision
— on whether the associated action needs human approval before it proceeds.
Implements `project-memory-bank/06-security-model.md`'s
`Classify → Minimize → Sanitize → Authorize → Execute → Audit` workflow as a
runnable skill, rather than a principle every other skill follows only
informally.

## Problem
Agents routinely handle content and take actions (reading files, pushing
code, calling external services) without a consistent, explicit pass that
asks: does this content contain something sensitive, and does this action
match one of the high-risk categories that always require a human
checkpoint? Without that pass, the decision is made implicitly, inconsistently,
and without an audit trail. This skill forces the pass to happen explicitly
and produces a durable, auditable classification — but it does not, and must
never, replace the human checkpoint itself (see Security Constraints below).

## When to Use
- Before content (a file, a diff, a context blob) is passed to another tool,
  logged, displayed, or sent outside the current session.
- Before taking an action that might match one of the six high-risk
  categories in `project-memory-bank/06-security-model.md`: Production
  modifications, Destructive operations, Credentials, Security controls,
  Database migrations, Publishing, External communications.
- As a general-purpose gate usable standalone — composition with
  `codebase-intelligence` is **optional** here (unlike `feature-planner`'s
  ADR-010), only enriching an optional hotspot-touch note when a
  `--ci-report` is supplied.

## When NOT to Use
- As a substitute for the actual human approval step — the engine's
  `suggested_verdict` is advisory. A human must still make and record the
  real authorization decision for anything flagged
  `REQUIRES_HUMAN_APPROVAL` (see Security Constraints).
- As proof that content contains no sensitive data — the secret/PII/action
  pattern tables are heuristic leads with a real false-negative rate (see
  Known Limitations), not a guarantee.
- As a way to reason about the *actual* value of a detected secret — the
  engine never returns the raw matched value to any caller (ADR-008/ADR-011).

## Preconditions
- Content text (or a file path) to classify, available as a file or via
  stdin.
- Python 3.10+ available in the execution environment.
- No `codebase-intelligence` report is required — it is entirely optional.

## Inputs
- `path` (required): path to a content file to classify, or `-` to read
  from stdin.
- `--action` (optional): free-text description of the action about to be
  taken with this content. An empty/omitted action is itself meaningful —
  see Workflow Step 3, category 7.
- `--paths` (optional): paths involved in the action, checked against
  sensitive-path conventions (`.env`, `*.pem`, `id_rsa*`, etc.).
- `--ci-report` (optional): a `codebase-intelligence` `report.json` — used
  only to annotate whether a given path is a known hotspot; a missing or
  unreadable report is a warning, never a failure.
- `--format` / `--out`: same as every other skill in this platform.

## Required Context
None required beyond the content/action/paths given directly as arguments —
this skill does not depend on the agent's existing conversation context, and
composition with `codebase-intelligence` is optional enrichment only.

## Context Completeness
The deterministic engine's output is a classify/sanitize pre-processing aid:
secret/PII/sensitive-path/action-category matches, redacted content, and a
`suggested_verdict`. It is not the final authorization decision — the actual
Security Decision Checklist walk (Step 3) and the human approval step happen
outside the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`.
- No network access; no external calls.
- **The engine never authorizes anything.** `classification.suggested_verdict`
  is advisory — a lead for the agent's Step 3 recommendation to a human, not
  an executed gate. This skill cannot self-authorize a production deploy,
  database migration, or any other high-risk action any more than any other
  tool can (`project-memory-bank/06-security-model.md` Human Approval
  principle; ADR-011).
- Every secret/PII match is redacted (`<redacted>`, every occurrence, not
  just the first) before it reaches any model field, JSON, or Markdown
  output — verified by test (`tests/test_integration.py`).
- Defaults toward `REQUIRES_HUMAN_APPROVAL` whenever evidence is
  inconclusive (no action description given) — fail closed, not fail open.

## Workflow
### Step 1 — Gather inputs
Identify the content to be exposed, the action about to be taken with it,
and any paths involved.

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <content-file-or-'-'> --action "<text>" --paths <path...> [--ci-report <report.json>] --format both --out <output-dir>`
(from `skills/security-context-guard/`).

### Step 3 — Walk the Security Decision Checklist
Go through each of these categories explicitly (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's matches
and `suggested_verdict` as leads, not the complete answer — this checklist
is shaped differently from this platform's other three (a decision-gate
workflow, not a coverage-enumeration list):
```
1. Data classification (none/low/medium/high, with evidence)
2. Minimization opportunity (can less be exposed and still work?)
3. Sanitization applied (secrets/PII redacted, never raw, in every output)
4. Authorization requirement (does this match a high-risk action category?)
5. Recommendation (AUTHORIZE / REQUIRES_HUMAN_APPROVAL) + rationale —
   framed as advice to a human, never a self-executed gate
6. Audit entry (what/why/when, durable-log-shaped)
7. Explicit uncertainty flag — if evidence is inconclusive, say so and
   default toward REQUIRES_HUMAN_APPROVAL; never silently AUTHORIZE
```
Category 7 is this checklist's version of the honesty-valve convention
shared with the other three checklists — adapted to "fail closed under
uncertainty" rather than "state the assumption," because this skill's job
is deciding whether to proceed, not enumerating coverage.

### Step 4 — Produce the Security Guard Report
Structure: the engine's `SecurityGuardReport` (JSON/Markdown) plus the
agent's own Step 3 checklist walk as a separate artifact. If the
recommendation is `REQUIRES_HUMAN_APPROVAL`, surface that clearly to the
human and wait for their decision before proceeding with the action — do
not proceed on the agent's own authority.

## Agent Responsibilities
- Never present `suggested_verdict` as a final decision — it is always a
  recommendation to a human, stated as such.
- Never omit category 7 when the action description is empty or genuinely
  ambiguous — silently defaulting to AUTHORIZE on inconclusive input is
  exactly the failure mode this checklist exists to prevent.
- Distinguish a pattern match (mechanical) from the actual classification
  judgment (the agent's own reasoning) in the report.

## Tool Permissions
- Bash (to invoke `python -m engine.cli`) — read-only usage only.
- Read/Grep (to gather the content/paths being classified).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
Any `REQUIRES_HUMAN_APPROVAL` recommendation requires an actual human
decision before the associated action proceeds — this is not optional, and
is the same discipline `project-memory-bank/06-security-model.md` already
requires for the six named high-risk action categories regardless of
whether this skill is used.

## Outputs
- `security-guard-report.json` — full deterministic packet: stats, secret/
  PII/sensitive-path/action-flag matches (all redacted), classification (see
  `engine/models.py`: `SecurityGuardReport`).
- `security-guard-report.md` — condensed version of the same.
- The agent's own **Security Decision Checklist** walk (Step 3) is a
  separate artifact this skill's workflow produces, not emitted by the
  engine itself.

## Verification
- `pytest` (58 unit/integration tests as of v0.1.0, including a CLI test
  file added from the start — see Known Limitations for why) — see `tests/`.
- `evaluations/security-context-guard/run_evaluation.py` against 8 fixtures
  (deterministic classification layer) plus this session's actual checklist
  derivation for each (judgment layer) — see
  `evaluations/security-context-guard/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/security-context-guard/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic secret/PII/path/action matching plus the sensitivity/
suggested_verdict rollup (Correctness/Efficiency, automated) and judgment-
layer checklist findings (Precision/Recall/False Positives/False Negatives
against hand-authored expected categories). The judgment-layer ground truth,
fixtures, and actual derivation were all produced by this same session's
agent — self-authored, single-rater evidence, not an inter-rater-agreement
experiment. This is the **fourth** judgment-based skill evaluated this way;
treat the resulting scores as proof the workflow is executable and
internally consistent, not as evidence of real-world security-judgment
quality. See `project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md` A5/A7.

## Failure Conditions
- Content file does not exist or is unreadable → CLI exits non-zero with a
  clear stderr message.
- Empty content, action, and paths all together → engine returns a report
  with a warning, not a hard error.
- `--ci-report` path does not exist, is not valid JSON, or lacks the
  expected fields → a warning is added to the report, never a failure —
  composition here is optional, unlike `feature-planner`'s ADR-010.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the secret/PII/
sensitive-path/action-category tables are heuristic, leads-not-verdicts
pattern matches with a real false-positive/negative rate, not exhaustive;
a real dogfood run found and fixed a same-sentence-vs-fixed-window matching
bug in the action classifier (L16); this is the fourth judgment-based skill
with single-rater, self-authored evaluation evidence (L8).

## Examples
See `examples/security-context-guard/example-run.md` for a real run of this
skill against this platform's own real source and a real pending git-push
decision — including the real bug it surfaced and fixed (L16), and Pilot C,
the first internal pilot toward A7 (does security handling increase trust).

## Provenance
Built in Phase 5 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven workflow)
a fourth time, plus a new architectural decision (ADR-011) extending
ADR-008's redact-not-exclude discipline from diff-content secrets to a
general classify/minimize/sanitize engine, and establishing that this
engine's `suggested_verdict` is always advisory, never self-executed. See
`project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies); the judgment
layer is the invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: secret/PII/sensitive-path/action-category
  pattern tables with redact-before-output discipline, deterministic
  sensitivity/suggested_verdict rollup (fail-closed on uncertainty),
  optional codebase-intelligence hotspot enrichment, JSON/Markdown
  renderers, CLI, evaluation harness with 8 fixtures plus a real dogfood
  run against this platform's own repository and a real pending decision.
