# Acceptance Test Engineer

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/acceptance-test-engineer/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over natural-language requirements (this skill's
  core value is judgment — deriving acceptance criteria — not just deterministic
  tooling)

## Purpose
Turn a vague-to-moderately-specified requirement or feature description into
an explicit, structured set of acceptance test cases that define what
"correct" means — before implementation, so correctness is a target, not an
afterthought.

## Problem
Agents (and engineers) asked to "build X" tend to silently resolve every
ambiguity in the requirement themselves, in whatever way is easiest to
implement, then present the result as if it were the only reasonable reading.
This skill forces the ambiguity to surface *before* implementation: flag
requirement text that is mechanically detectable as untestable (vague
adjectives, weak modal verbs, total silence on error/boundary behavior), then
have the agent derive acceptance test cases against a fixed 10-category
coverage checklist — explicitly stating an assumption wherever the
requirement is silent, rather than guessing quietly.

## When to Use
- Before implementing a new feature or fixing a bug, to pin down what
  "correct" means first.
- When a requirement/ticket/spec reads as plausible but you cannot yet state
  how you'd verify it's satisfied.
- As the `DEFINE CORRECTNESS` step after `codebase-intelligence` (UNDERSTAND)
  and/or `adversarial-diff-reviewer` (VERIFY) — composition is optional, not
  required.

## When NOT to Use
- As a substitute for actually writing/running executable tests — this skill
  produces Gherkin-style acceptance criteria and JSON test-case specs, not
  generated pytest/step-definition code (see Known Limitations: it does not
  know the real implementation's API).
- On a requirement the agent wrote itself in the same turn without a fresh,
  skeptical read — self-review immediately after writing the requirement is
  weak evidence, same caveat as `adversarial-diff-reviewer`.
- As proof a feature is "done" — acceptance criteria existing is not the same
  as a human/stakeholder having approved them.

## Preconditions
- Free-text requirement/feature-description input available as a file or via
  stdin.
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a requirement text file, or `-` to read from stdin.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The requirement text itself is required. Optional composed context: a
`codebase-intelligence` report of the affected code area, if the requirement
concerns an existing system — helps Step 3 ground acceptance cases in real
entities instead of guessing at them.

## Context Completeness
The deterministic engine's output is a testability pre-processing aid —
parsed sentences, objective stats, and a fixed table of regex-detected
testability anti-patterns. It is not the acceptance-test derivation itself.
The actual coverage-checklist reasoning happens in Step 3, performed by the
agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file except
  its own report output under `--out`.
- No network access; no external calls.
- Requirement text may itself describe security-sensitive behavior (auth,
  permissions, data handling) — this skill's Category 8 (authorization
  boundary) exists specifically to surface that into an explicit acceptance
  case rather than letting it stay implicit.

## Workflow
### Step 1 — Invoke the engine
Run via Bash: `python -m engine.cli <requirement-file-or-'-'> --format both --out <output-dir>`
(from `skills/acceptance-test-engineer/`).

### Step 2 — Read composed context (optional)
If the requirement concerns existing code, read a `codebase-intelligence`
report or the relevant files directly (Read/Grep) to ground acceptance cases
in real function/module names rather than inventing plausible-sounding ones.
Note explicitly when no such context was available.

### Step 3 — Derive acceptance test cases against the coverage checklist
Go through each of these categories explicitly for this requirement (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's
testability flags as leads to what's likely to be under-specified, not as the
complete list — most of these categories cannot be regex-detected:
```
1. Happy path / primary success        6. Duplicate / repeat / idempotency
2. Boundary / edge values              7. Concurrent access (if applicable)
3. Invalid input / error handling      8. Authorization boundary (if applicable)
4. Explicit negative case (must-not)   9. Stated non-functional constraint
5. Empty / missing / null state       10. Explicit assumption flag (requirement
                                          silent → state the assumption, don't
                                          guess silently)
```
Not every category applies to every requirement (e.g. category 7/8 may be
N/A) — state N/A explicitly rather than omitting the category silently.

### Step 4 — Produce the Acceptance Test Report
For each test case: `{id, category, given, when, then, priority,
assumptions}`. Render as JSON test-case specs plus a Markdown block using real
Gherkin syntax (`Feature:`/`Scenario:`/`Given`/`When`/`Then`) — a genuine,
tool-consumable test artifact. Do not generate pytest/step-definition code:
this skill has not read the real implementation, and generated glue code
would fabricate false precision about a system it doesn't know.

## Agent Responsibilities
- Never present an assumption as a derived fact — every place the requirement
  was silent, category 10 must name the assumption explicitly.
- Distinguish a testability-flag hit (mechanical pattern match) from an actual
  acceptance case (the agent's own judgment) in the report — do not present
  regex output as if it were the test case itself.
- State explicitly which of the 10 categories were considered, which were
  N/A, and which could not be resolved without more context — silence is not
  the same as "not applicable."

## Tool Permissions
- Bash (to invoke `python -m engine.cli`) — read-only usage only.
- Read/Grep (to read composed context, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce acceptance criteria. A human (or the requirement's
actual stakeholder) should still review and approve the derived criteria
before they're treated as the definition of "done" — this skill's output is
an input to that decision, not a substitute for it, same discipline as
`project-memory-bank/06-security-model.md` requires for any consequential
decision.

## Outputs
- `acceptance-testability-report.json` — deterministic pre-processing packet:
  stats, testability flags, parsed sentences (see `engine/models.py`:
  `AcceptanceTestabilityReport`).
- `acceptance-testability-report.md` — condensed version of the same.
- The agent's own **Acceptance Test Report** (Step 4), including the Gherkin
  block, is a separate artifact this skill's workflow produces, not emitted
  by the engine itself.

## Verification
- `pytest` (20 unit/integration tests as of v0.1.0) — see `tests/`.
- `evaluations/acceptance-test-engineer/run_evaluation.py` against 8 fixture
  requirements (deterministic testability-flag layer) plus this session's
  actual acceptance-case derivation for each (judgment layer) — see
  `evaluations/acceptance-test-engineer/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/acceptance-test-engineer/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic testability-flags (Correctness/Completeness, automated) and
judgment-layer coverage-category findings (Precision/Recall/False
Positives/False Negatives against hand-authored expected categories). The
judgment-layer ground truth, fixtures, and actual derivation were all
produced by this same session's agent — self-authored, single-rater evidence,
not an inter-rater-agreement experiment; treat the resulting scores as proof
the workflow is executable and internally consistent, not as evidence of
real-world acceptance-criteria quality. See
`project-memory-bank/12-known-limitations.md` L8 (established in Phase 2,
applies identically here) and
`project-memory-bank/16-assumptions-and-validation.md` A5.

## Failure Conditions
- Requirement file does not exist or is unreadable → CLI exits non-zero with
  a clear stderr message.
- Empty or unparseable requirement text → engine returns an empty report
  (`sentences: []`) with a warning, not a hard error — the agent should flag
  this to the user rather than deriving acceptance cases from nothing.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the testability
anti-pattern list is not exhaustive and will both over-flag (a legitimately
precise use of "should" as an RFC-2119-style non-mandatory clause) and
under-flag (any ambiguity not matching a known vague-term/weak-modal shape);
the sentence splitter is naive (over-splits on abbreviations like "e.g.");
no executable test code is generated, Gherkin text only; judgment-layer
evaluation so far is single-rater (this session's agent), not independently
verified.

## Examples
See `examples/acceptance-test-engineer/example-run.md` for a real run of this
skill against the actual `--format`/`--out` CLI behavior implemented in
`skills/adversarial-diff-reviewer/engine/cli.py`.

## Provenance
Built in Phase 3 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven workflow)
without a new base-pattern ADR — see `project-memory-bank/03-architecture.md`.
Stdlib-only Python engine for the deterministic layer (no runtime third-party
dependencies); the judgment layer is the invoking agent's own reasoning, not
code.

## Changelog
- 0.1.0 — Initial implementation: requirement parser, testability pattern
  table (vague terms, weak modal verbs, error/boundary-signal absence
  checks), requirement stats, JSON/Markdown renderers (Markdown includes a
  Gherkin block), CLI, evaluation harness with 8 fixtures plus a real-
  requirement dogfood example.
