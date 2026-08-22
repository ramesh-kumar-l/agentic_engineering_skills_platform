# Adversarial Diff Reviewer

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/adversarial-diff-reviewer/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over code (this skill's core value is judgment, not
  just deterministic tooling)

## Purpose
Adversarially review a code diff — actively look for reasons the change is
wrong, not just confirm it looks plausible — and produce a structured list of
findings: obvious bugs, subtle bugs, concurrency issues, security issues,
performance regressions, and missing/incorrect requirements.

## Problem
Agents asked to "review this diff" tend to default to summarizing what changed
and confirming it looks reasonable — the same failure mode as an unmotivated
human reviewer skimming a PR. A convincing summary is not a review. This skill
forces an adversarial posture: assume the diff has a defect and go looking for
it against a fixed checklist, backed by a deterministic layer that catches the
mechanically-detectable cases so the agent's reasoning budget goes to the
cases regex cannot catch.

## When to Use
- Before approving/merging a diff, or when asked to review one.
- When a diff touches security-sensitive code (auth, secrets, deserialization,
  shell/SQL construction) — the risk-flag layer is tuned for exactly these.
- As a second pass after `codebase-intelligence` (optional, not required) when
  the diff's blast radius across the repo is unclear.

## When NOT to Use
- As a substitute for running the actual test suite or type checker — this
  skill does not execute code (see Known Limitations).
- On a diff the agent authored itself in the same turn without a fresh,
  skeptical read — self-review immediately after writing code is weak evidence.
- As the sole gate before a production change — see
  `project-memory-bank/06-security-model.md`: high-risk actions still require
  human approval regardless of this skill's verdict.

## Preconditions
- A unified diff (e.g. `git diff` output) available as a file or via stdin.
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a unified diff file, or `-` to read from stdin.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The diff itself is required. Read access to the touched files' surrounding
code (via Read/Grep) is strongly recommended for Step 2 — a diff without
surrounding context increases false negatives (see Known Limitations,
`missing-context` failure category).

## Context Completeness
The deterministic engine's output is a structural pre-processing aid — parsed
hunks, objective stats, and a fixed table of regex-detected risk flags. It is
not the review itself. The actual adversarial judgment happens in Step 3,
performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes the reviewed
  repository.
- Secret-shaped content matched in **added** lines (API keys, tokens,
  passwords) is redacted to `<redacted>` in both the risk flag and the raw
  line content before it reaches any report output — see `engine/risk_scanner.py`.
  Verified by test (`tests/test_integration.py::test_secret_value_never_leaks_into_json_or_markdown`).
- The agent must not copy an unredacted secret value out of the diff into the
  review report, commit message, or any external communication, even though
  the agent's own Read/Grep tools can see the real diff content directly.
- No network access; no external calls.

## Workflow
### Step 1 — Invoke the engine
Run via Bash: `python -m engine.cli <diff-file-or-'-'> --format both --out <output-dir>`
(from `skills/adversarial-diff-reviewer/`).

### Step 2 — Read touched files for context
For each file in the diff, read enough surrounding code (Read/Grep) to
understand what the changed lines actually do — do not review a hunk in
isolation from its function/class. Note explicitly what context was NOT
available (e.g. the diff references a function not shown) rather than
guessing.

### Step 3 — Adversarially review against the failure-first checklist
Go through each of these categories explicitly for this diff (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's risk
flags as leads, not as the complete list — most of these categories cannot be
regex-detected:
```
1. Obvious bug          6. Correct but unusual code
2. Subtle bug           7. Large noisy diff (real issue hidden in volume)
3. Concurrency bug      8. Missing context (can't verify without more info)
4. Security issue       9. Misleading implementation (does what it says, not what's needed)
5. Performance regression   10. Incorrect requirement (right code, wrong ask)
```

### Step 4 — Produce the Diff Review Report
For each finding: `{category, severity, file, line_range, description,
confidence}`. Include an overall risk verdict and an explicit "not checked"
section (no runtime execution, no test run, no cross-repo semantic
verification).

## Agent Responsibilities
- Never restate an unredacted secret value from the diff in the review output.
- Distinguish a risk-flag hit (mechanical pattern match) from an actual
  adversarial finding (the agent's own judgment) in the report — do not
  present regex output as if it were reasoning.
- State explicitly which of the 10 categories were considered and found clean
  vs. not considered due to missing context — silence is not the same as "no
  issue found."

## Tool Permissions
- Bash (to invoke `python -m engine.cli`) — read-only usage only.
- Read/Grep (to read touched files and surrounding context).
No write, network, or credential-accessing permissions are required or granted.

## Human Checkpoints
None required to produce a review. Per
`project-memory-bank/06-security-model.md`, a human must still approve before
any high-risk action (merge to a protected branch, production deploy) — this
skill's output is an input to that decision, not a substitute for it.

## Outputs
- `diff-report.json` — deterministic pre-processing packet: stats, risk flags,
  parsed file/hunk structure (see `engine/models.py`: `DiffIntelligenceReport`).
- `diff-report.md` — condensed version of the same.
- The agent's own **Diff Review Report** (Step 4) is a separate artifact this
  skill's workflow produces, not emitted by the engine itself.

## Verification
- `pytest` (19 unit/integration tests as of v0.1.0) — see `tests/`.
- `evaluations/adversarial-diff-reviewer/run_evaluation.py` against 8 fixture
  diffs (deterministic risk-flag layer) plus this session's actual adversarial
  review of each fixture (judgment layer) — see
  `evaluations/adversarial-diff-reviewer/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/adversarial-diff-reviewer/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic risk-flags (Correctness/Completeness, automated) and judgment
findings (Precision/Recall/False Positives/False Negatives against
hand-authored ground truth). The judgment-layer ground truth, fixtures, and
actual review were all produced by this same session's agent — self-authored,
single-rater evidence, not an inter-rater-agreement experiment; treat the
resulting scores as proof the workflow is executable and internally
consistent, not as evidence of real-world review quality. See
`project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md` A5.

## Failure Conditions
- Diff file does not exist or is unreadable → CLI exits non-zero with a clear
  stderr message.
- Malformed hunk header encountered before any file header → recorded in
  `warnings`, parsing continues for the rest of the diff (not a hard failure).
- A diff with no recognizable unified-diff structure → engine returns an empty
  report (`files: []`), not an error — the agent should flag this to the user
  rather than proceeding as if a review happened.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: risk-flag regexes
only catch mechanically-shaped issues and will both over-flag (e.g. a
legitimate `except Exception:` with proper logging) and under-flag (any bug
not matching a known pattern — most subtle/concurrency/logic bugs); no runtime
execution or test running; judgment-layer evaluation so far is single-rater
(this session's agent), not independently verified; a diff without full
surrounding file context increases false negatives.

## Examples
See `examples/adversarial-diff-reviewer/example-run.md` for a real run of this
skill against the actual historical diff from Phase 1's `has_main_guard` bugfix.

## Provenance
Built in Phase 2 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`, ADR-007/008 in
`project-memory-bank/11-decisions.md`). Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies); the judgment layer
is the invoking agent's own reasoning, not code.

## Changelog
- 0.1.0 — Initial implementation: diff parser, risk pattern table (secrets,
  dangerous calls, broad except, SQL injection shapes, debug leftovers, TODO
  markers) with in-place secret redaction, diff stats, JSON/Markdown
  renderers, CLI, evaluation harness with 8 fixtures plus a real-diff dogfood
  example.
