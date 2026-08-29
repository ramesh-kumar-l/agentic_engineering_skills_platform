# Release Readiness

## Metadata
- Version: 0.2.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/release-readiness/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a per-file, multi-axis readiness scorecard
  (this skill's core value is judgment — weighing which flagged/structural/
  uncovered/regression/security signal actually matters for THIS release —
  not just deterministic tooling)

## Purpose
Given a git diff, a real `codebase-intelligence` report, and (optionally)
pre-computed `regression-hunter`/`security-context-guard` reports for the
same change, produce an explicit, non-blended **Release Readiness
Scorecard** — a per-file `readiness_tier` and one overall `overall_verdict`
— that helps a human decide whether a body of work (not just one diff) is
actually ready to ship. This is the capstone/aggregator skill in the
Engineering Lifecycle group: the final skill in that group, and the first to
compose optionally with two OTHER skills' own outputs, not just
`codebase-intelligence`'s.

## Problem
Nine prior skills each answer a narrower question well (does this diff
introduce a new defect, is this refactor safe, does this diff risk an
existing regression, is this content/action safe to authorize) — but none
of them answers the question a human actually asks right before merging:
"is this body of work ready to ship, considering everything I know about
it?" Answering that by eyeballing several separate reports, or by
collapsing them into one blended score, both fail: eyeballing is
inconsistent and slow; blending hides exactly the distinction that matters
(a file with zero diff-hygiene issues but no test coverage on a real
hotspot is a fundamentally different risk than a file with a leftover
`print()` statement in an otherwise low-risk change — see ADR-016).

## When to Use
- As the final gate before merging or tagging a release, to see per-file
  diff-hygiene flags, real structural blast radius, real test coverage, and
  (if available) regression-risk and security-posture evidence from other
  skills in this portfolio, all kept as explicitly separate fields — never
  as one opaque "ready/not ready" number with no explanation.
- As a genuine composition point for this portfolio: if `regression-hunter`
  and/or `security-context-guard` have already been run against the same
  diff, hand their `report.json` outputs to this skill via
  `--regression-report`/`--security-report` so their findings are surfaced,
  not silently ignored or (worse) re-derived and possibly contradicted.
- As a companion to, not a replacement for, an actual PR review — this
  skill's output is a pre-decision scorecard, never an executed release
  gate (see Security Constraints).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill refuses to run without one rather
  than silently guessing blast radius (ADR-010, reused a sixth time).
- As a substitute for actually reviewing the diff, running the real test
  suite, or getting a second engineer's sign-off — nothing in the engine
  ever asserts a release is "authorized," "approved," or "safe to ship"
  (see Failure Conditions and `tests/test_report.py::
  test_report_never_fabricates_an_authorization_claim`).
- As proof `--regression-report`/`--security-report` were checked for
  freshness — this engine surfaces whatever those reports say verbatim; a
  stale regression-hunter report generated against an earlier version of the
  diff is surfaced as-is, not re-validated against the current diff.
- As proof an unresolved changed file means the diff touches nothing real —
  a file can fail to resolve because it's genuinely new, a rename target, or
  outside the scanned repo; the engine cannot tell these apart on its own.
- As proof "no diff-hygiene flag fired" means the diff is release-ready —
  the hygiene pattern table is a fixed, non-exhaustive set of mechanically-
  detectable shapes (see Known Limitations); most real release-blocking
  issues (a genuine logic error, a missing migration step, an
  undocumented breaking change) are invisible to regex, exactly why the
  agent's Step 3 judgment layer exists.

## Preconditions
- Unified diff text (git-style or plain) available as a file or via stdin.
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010, reused a sixth time; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a unified-diff text file, or `-` to read from
  stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--regression-report` (optional): path to a `regression-hunter`
  `report.json` for this same diff. Missing is simply absent evidence, not
  a failure (ADR-011 precedent, not ADR-010's mandatory-composition rule).
- `--security-report` (optional): path to a `security-context-guard`
  `report.json`. Missing is simply absent evidence, not a failure.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The diff AND a `codebase-intelligence` report for the target repo are both
required — this is the SIXTH skill in this platform where composition with
`codebase-intelligence` is a hard precondition rather than optional context
(ADR-010, reused by `root-cause-analyzer`, `architecture-decision`,
`refactoring-safety`, and `regression-hunter` before this — stated here
explicitly as a **reuse**, not a new decision; the exit criteria's "first
skill composing on top of Codebase Intelligence's output" is not literally
true of this skill either, same honest framing as Phases 6-9). A
`regression-hunter` and/or `security-context-guard` report for the same
diff are OPTIONAL composed context — when present, their own findings are
surfaced verbatim as distinct fields (Axis 4/5), never re-derived; when
absent, the report says so explicitly rather than silently proceeding as if
those axes don't exist.

## Context Completeness
The deterministic engine's output is a pre-decision aid: per-file
diff-hygiene flags, a real structural blast-radius assessment, an
independently-computed test-coverage signal, and (when supplied) surfaced
regression/security evidence — five fields, never blended into one number
(ADR-016). It is not the release decision itself: `overall_verdict ==
"NOT_READY"` means at least one file's readiness tier crossed the
documented rule-table's blocking threshold, not that a human has reviewed
and rejected the release; `overall_verdict == "READY"` means none of the
always-available axes fired for any file, not that the release is provably
safe. The actual judgment happens in Step 3, performed by the agent, not
the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the diff
  or any of the composed reports it reads.
- No network access; no external calls.
- **`overall_verdict` is ALWAYS a recommendation for a human to review,
  NEVER an autonomous release gate.** This skill's output must never be
  wired into an automated merge/deploy/tag action without an explicit human
  approval step in between — per `project-memory-bank/06-security-
  model.md`'s Human Approval principle, and the same "advisory only, never
  self-executed" discipline ADR-011 established for `security-context-
  guard`'s `suggested_verdict`. A "release verdict" is exactly the kind of
  high-stakes recommendation that rule exists for.
- Diff content may contain secrets/PII added or removed as part of the
  change. This skill does not scan or redact diff content beyond the small,
  independent hygiene-pattern table in `engine/hygiene_patterns.py` — if a
  diff may contain sensitive material, run it through `security-context-
  guard` first and compose its report via `--security-report`.

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010).

### Step 2 — (Optional) Run regression-hunter and/or security-context-guard against the same diff
If either skill has already been run against this diff, keep their
`report.json` output — pass it via `--regression-report`/`--security-report`
in Step 3. If neither has been run and time allows, running them first
produces a materially richer scorecard; if not, this skill still produces a
complete scorecard from Axes 1-3 alone.

### Step 3 — Invoke the engine
Run via Bash: `python -m engine.cli <diff-file-or-'-'> --ci-report <report.json> [--regression-report <report.json>] [--security-report <report.json>] --format both --out <output-dir>`
(from `skills/release-readiness/`).

### Step 4 — Walk the Release Readiness Checklist
Go through each of these categories explicitly for this body of work (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's
per-file scorecard as leads, not the complete answer — most of these
categories cannot be regex-detected:
```
1. Scope stated precisely (what is       6. Overall verdict explained via
   actually being released, not just         the documented rule table,
   "this diff")                              not asserted
2. Diff-hygiene blockers reviewed as     7. False-positive check (is a
   absolute, not leads — a hygiene           flagged pattern actually
   flag means blocked, full stop            safe here, e.g. a print() in
3. Structural blast radius grounded         a CLI tool's own output path)
   in real fan-in/hotspot data, not      8. Evidence cited, not opinion
   guessed                              9. Explicit assumption flag
4. Test coverage distinguished per          (evidence silent → state it,
   file — covered vs. genuinely             don't guess)
   untested, not conflated
5. Regression/security evidence
   surfaced-not-re-derived when
   present, explicitly marked
   ABSENT (not assumed clean) when
   not supplied — 10. Verdict framed as
   advisory/human-checkpoint, NEVER
   an auto-gate
```
Category 9 is the honesty valve — same convention as every prior
judgment-based skill's checklist in this project. Category 10 is this
skill's non-negotiable framing requirement (see Security Constraints): the
walk must explicitly state the verdict is a recommendation, never assert it
as an executed decision.

### Step 5 — Produce the Release Readiness Record
Structure: `{files: [{path, hygiene_flags, structural_tier, test_coverage,
regression_evidence, readiness_tier, agent_assessment}], overall_verdict,
security_evidence, recommendation, assumptions}`. Render as JSON plus a
Markdown record a human can review quickly. This skill does not decide
release/no-release for the human — it produces the grounded material a
human (or the invoking agent, under human review) uses to record the actual
call.

## Agent Responsibilities
- Never present a `readiness_tier == "blocked"` file and a `readiness_tier
  == "clear"` file as equally releasable — the report's `readiness_tier`,
  `structural.structural_tier`, and `test_coverage.has_coverage` fields
  exist specifically so this distinction survives into the record.
- Never treat a fired diff-hygiene flag as a soft signal — per ADR-016's
  rule table, a hygiene flag is an ABSOLUTE blocker regardless of every
  other axis; do not let a low structural tier or full test coverage
  "outvote" a genuine hygiene finding.
- Never read "no `--regression-report`/`--security-report` supplied" as
  "this diff has no regression risk / no security concerns" — it means
  those axes were never checked for this run; say so explicitly (category 5
  of the checklist) rather than reading absence as a clean bill of health.
- Never re-derive a verdict a composed report already computed — if
  `regression_evidence.overall_risk_tier == "high"`, surface that fact
  as-is; do not recompute regression risk from the diff yourself when a
  real regression-hunter report already did.
- Never present `overall_verdict` as an executed decision — every mention
  of it, in any output surface, must be framed as a recommendation for a
  human to review (Security Constraints).
- Do not trust `structural.fan_in` as the complete caller picture without
  also checking `structural.caller_modules` — the two can diverge (same
  class of gap disclosed as L23 for `refactoring-safety`'s and
  `regression-hunter`'s identical `target_resolver.py` pattern, reused here
  a third time — see Known Limitations).

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for `codebase-intelligence`,
  optionally `regression-hunter`/`security-context-guard`, and
  `release-readiness`) — read-only usage only.
- Read/Grep (to read composed context, e.g. an existing `regression-hunter`
  or `security-context-guard` report, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
A human MUST review and approve the actual release/merge/tag action,
especially when `overall_verdict` is `NOT_READY` or `READY_WITH_CONDITIONS`
— this skill's output is an input to that review, never a substitute for
it, and never wired to an automated action on its own (Security
Constraints). This is the same discipline every prior judgment-based skill
in this project applies to its own highest-risk signal, stated here with
extra emphasis because "release readiness" is the single highest-stakes
recommendation this portfolio produces.

## Outputs
- `release-readiness-report.json` — deterministic pre-decision packet:
  stats, per-file diff-hygiene flags, structural assessment, test-coverage
  status, optional regression evidence, optional report-level security
  evidence, overall verdict (see `engine/models.py`:
  `ReleaseReadinessReport`).
- `release-readiness-report.md` — condensed version of the same, with every
  axis kept visibly separate per file.
- The agent's own **Release Readiness Record** (Step 5), the actual
  release-readiness judgment, is a separate artifact this skill's workflow
  produces, not emitted by the engine itself.

## Verification
- `pytest` (78 unit/integration/CLI tests as of v0.1.0, CLI test file
  written from the start — same discipline every prior phase since Phase 5
  established) — see `tests/`.
- `evaluations/release-readiness/run_evaluation.py` against 8 fixture
  diffs (deterministic hygiene/structural/coverage/verdict layer) plus this
  session's actual checklist derivation for each (judgment layer) — see
  `evaluations/release-readiness/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/release-readiness/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic hygiene-flag + structural-tier + coverage-status +
readiness-tier + overall-verdict scoring (Correctness/Efficiency,
automated) and judgment-layer checklist-category findings (Precision/
Recall/False Positives/False Negatives against hand-authored expected
categories). The judgment-layer ground truth, fixtures, and actual
derivation were all produced by this same session's agent — self-authored,
single-rater evidence, not an inter-rater-agreement experiment. This is the
**ninth** judgment-based skill evaluated this way; treat the resulting
scores as evidence the workflow (including the required
codebase-intelligence composition and the optional regression/security
composition) is executable and internally consistent, not as evidence of
real-world release-readiness judgment quality. See
`project-memory-bank/12-known-limitations.md` L8 and
`project-memory-bank/16-assumptions-and-validation.md` for the actual
per-fixture scores, reported as computed rather than adjusted.

## Failure Conditions
- Diff file does not exist or is unreadable → CLI exits non-zero with a
  clear stderr message.
- `--ci-report` path does not exist, is not valid JSON, or does not match
  the `CodebaseIntelligenceReport` schema → CLI exits non-zero with an
  actionable error naming the missing precondition (ADR-010) — this is a
  hard failure, not a degraded-but-working path.
- `--regression-report`/`--security-report` path does not exist, is not
  valid JSON, or is missing expected fields → NOT a hard failure; the
  engine adds an explicit warning and proceeds with that evidence marked
  absent (ADR-011 precedent).
- Empty diff → engine returns a report with a warning and zero files, not
  a hard error — `overall_verdict` is explicitly noted as not meaningful
  for an empty diff.
- No changed file resolves against the codebase-intelligence report → the
  engine adds an explicit warning; the agent must not treat this as
  evidence the diff is release-ready, only as evidence nothing could be
  structurally assessed.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the
diff-hygiene table (`engine/hygiene_patterns.py`) is a fixed, small set of
mechanically-detectable shapes — it can both over-flag (e.g. a legitimate
`print()` call in a CLI tool's own intended stdout output) and under-flag
(any release-blocking issue not matching a known pattern, which is most
real ones — same boundary every prior Pattern 2 skill's anti-pattern table
has). `target_resolver.py`'s caller-identification is a THIRD independent
copy of the exact substring-matching limitation already disclosed as **L23**
(`refactoring-safety`'s and `regression-hunter`'s identical
`target_resolver.py` pattern) — this is the same underlying issue in a
third skill, not a new finding, and is documented here as a cross-reference
rather than a new L-number. `--regression-report`/`--security-report`
evidence is surfaced verbatim with no freshness check against the current
diff — a stale composed report is not detected as stale. This is the ninth
judgment-based skill with single-rater, self-authored evaluation evidence.

## Examples
See `examples/release-readiness/example-run.md` for a real run of this
skill: a freshly regenerated `codebase-intelligence` report against this
platform's current (10-skill) repository state, composed into a real git
diff produced during this phase's own build.

## Provenance
Built in Phase 10 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven
workflow) a ninth time, and reusing `feature-planner`'s/`root-cause-
analyzer`'s/`architecture-decision`'s/`refactoring-safety`'s/`regression-
hunter`'s required-composition rule (ADR-010) a sixth time, plus a new
architectural decision (ADR-016) introducing the Release Readiness
Scorecard: five explicitly separate, non-blended readiness signals (three
always-available — diff-hygiene, structural blast radius, test coverage —
combined into a per-file `readiness_tier` via a documented rule table; two
optional — regression evidence, security evidence — surfaced but not
blended in) rolled up into one advisory `overall_verdict`. See
`project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of any other skill in this portfolio); the judgment layer is the
invoking agent's own reasoning, not code.

## Changelog
- 0.2.0 — JVM support (ADR-022, user-directed cross-cutting scope, not a
  new roadmap phase): `test_coverage_scanner.py` recognizes the JVM
  `*Test`/`*Tests`/`*Spec` suffix convention; `hygiene_patterns.py` gains
  a `System.out/err.println()` debug-leftover pattern. 2 new tests (82 → 84).
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition, sixth reuse of ADR-010),
  unified-diff parser (independent copy of regression-hunter's/
  adversarial-diff-reviewer's parsing conventions), target resolver
  (exact-path + module-stem resolution, real caller lookup via import scan,
  third independent copy of the L23 substring-matching limitation),
  test-coverage scanner (static import-based heuristic, independent copy),
  diff-hygiene scanner (debug leftovers, merge-conflict markers,
  hardcoded-secret-shaped literals, TODO-blocking markers), optional
  regression-hunter/security-context-guard report loaders (ADR-011
  precedent — absent evidence, not a failure, on missing/malformed input),
  readiness scorer combining the three always-available axes into a per-file
  `readiness_tier` and rolling per-file tiers into one advisory
  `overall_verdict` via a documented rule table (ADR-016), JSON/Markdown
  renderers keeping every axis visibly separate, CLI with a CLI test file
  written from the start, evaluation harness with 8 fixtures plus a real
  dogfood example.
