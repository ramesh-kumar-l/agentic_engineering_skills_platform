# Regression Hunter

## Metadata
- Version: 0.2.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/regression-hunter/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to reason over a per-file, three-axis risk report (this
  skill's core value is judgment — weighing which flagged/structural/
  uncovered signal actually matters for this diff — not just deterministic
  tooling)

## Purpose
Given a git diff and a real `codebase-intelligence` report, identify which
existing behavior is at risk of regressing from that diff — surfaced as
three explicitly separate, non-blended signals per changed file (mechanical
diff-pattern flags, structural blast radius, test coverage status), rather
than one opaque risk score.

## Problem
Agents (and humans) reviewing a diff tend to eyeball "does this look safe"
without checking three things a diff itself can partially answer
mechanically: (1) does the diff's own shape contain a pattern correlated
with real regressions (removed exception handling, a removed conditional
guard with no replacement, a large unreplaced deletion, decreased test
assertions in a changed test file, a changed function signature with no
corresponding test-file change)? (2) does the changed file have real
structural blast radius — real callers, hotspot status — grounded in a real
dependency graph, not guessed? (3) is the changed file actually covered by
a real test module? Blending these three into one score would hide exactly
the distinction that matters: a flagged-but-covered file is a different
risk than an unflagged-but-uncovered hotspot, and neither should be
collapsed into a single number that looks the same either way (ADR-015).

## When to Use
- Before merging or approving a diff, to see per-file diff-pattern flags,
  real blast radius, and real test coverage as three separate signals, not
  eyeballed.
- As a regression-focused companion to `adversarial-diff-reviewer` (which
  reviews a diff for NEW defects it introduces) — this skill instead asks
  "what EXISTING behavior might this diff have broken," using a real
  dependency graph and test-coverage signal `adversarial-diff-reviewer`
  does not compose with.
- As a safety gate after `codebase-intelligence` (UNDERSTAND) and before
  merging (IMPLEMENT/VERIFY) — composition with `codebase-intelligence` is
  **required** here, the same as `feature-planner`, `root-cause-analyzer`,
  `architecture-decision`, and `refactoring-safety` (ADR-010, reused a
  fifth time here).

## When NOT to Use
- On a repository with no `codebase-intelligence` report yet — run that
  skill first (Step 1 below); this skill refuses to run without one rather
  than silently guessing blast radius.
- As a substitute for actually reviewing the diff, or for running the real
  test suite — this skill's output is a pre-decision packet (per-file flags
  + structural + coverage), not a verdict; nothing in the engine ever
  asserts the diff is "safe to merge" (see Failure Conditions and
  `tests/test_report.py::test_report_never_fabricates_a_verdict`).
- As proof an unresolved changed file means the diff touches nothing real —
  a file can fail to resolve because it's genuinely new (not yet in the
  composed report), a rename target, or outside the scanned repo; the
  engine cannot tell these apart on its own.
- As proof "no diff-pattern flag fired" means the diff is regression-free —
  the pattern table is a fixed, non-exhaustive set of mechanically-
  detectable shapes (see Known Limitations); most real regressions are
  logic errors invisible to regex, exactly why the agent's Step 3 judgment
  layer exists.
- As proof test coverage found means the covering test currently passes or
  exercises the changed behavior — this is a static-import heuristic (does
  a test module import the file), not a test-run result.

## Preconditions
- Unified diff text (git-style or plain) available as a file or via stdin.
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — see ADR-010, reused a fifth time; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first if one doesn't exist).
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to a unified-diff text file, or `-` to read from
  stdin.
- `--ci-report` (required): path to a `codebase-intelligence` `report.json`
  for the target repo.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
The diff AND a `codebase-intelligence` report for the target repo are both
required — this is the fifth skill in this platform where composition is a
hard precondition rather than optional context (ADR-010, reused by
`root-cause-analyzer`, `architecture-decision`, and `refactoring-safety`
before this — stated here explicitly as a **reuse**, not a new decision).
Optional composed context: an existing test-run/CI log, if available, so
the agent's Step 3 walk can check real, current test-pass status rather
than only static test-file presence (this engine only checks whether a
test module imports the changed file, not whether that test currently
passes); an `adversarial-diff-reviewer` report for the same diff, if
available, since that skill's new-defect findings and this skill's
existing-behavior-at-risk findings are complementary, not overlapping.

## Context Completeness
The deterministic engine's output is a pre-decision aid: per-file
mechanically-detected diff-pattern flags, a real structural blast-radius
assessment against `codebase-intelligence`'s fan-in/hotspot data, and an
independently-computed test-coverage signal — three fields, never blended
into one number (ADR-015). It is not the regression verdict itself: a HIGH
overall tier means the combination of these three signals crossed the
documented rule-table threshold, not that a regression definitely exists;
a LOW tier means none of the three signals fired for this file, not that
the file is provably regression-free. The actual judgment happens in Step
3, performed by the agent, not the engine.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes any file
  except its own report output under `--out`, and never modifies the diff
  or the `codebase-intelligence` report it reads.
- No network access; no external calls.
- This skill never blocks or authorizes a merge — its output is a
  read-only risk-flagging report for a human/agent to weigh, per
  `project-memory-bank/06-security-model.md`'s Human Approval principle;
  same posture as `refactoring-safety`'s `Failure Conditions` and
  `security-context-guard`'s advisory-only design (ADR-011).
- Diff content may contain secrets/PII added or removed as part of the
  change. This skill does not scan or redact diff content — if a diff may
  contain sensitive material, run it through `adversarial-diff-reviewer`
  (which does redact secret-shaped matches) or `security-context-guard`
  first (optional composition, not required here).

## Workflow
### Step 1 — Ensure a codebase-intelligence report exists
If the target repo has not already been scanned in this session, run
`python -m engine.cli <path> --format json --out <dir>` from
`skills/codebase-intelligence/` first. This skill will not run without a
valid report (see Failure Conditions) — that is deliberate (ADR-010).

### Step 2 — Invoke the engine
Run via Bash: `python -m engine.cli <diff-file-or-'-'> --ci-report <report.json> --format both --out <output-dir>`
(from `skills/regression-hunter/`).

### Step 3 — Walk the Regression Risk Checklist
Go through each of these categories explicitly for this diff (from
`project-memory-bank/05-evaluation-framework.md`); use the engine's
per-file flags/structural/coverage report as leads, not the complete
answer — most of these categories cannot be regex-detected:
```
1. Existing behavior at risk stated       6. False-positive check (is a
   precisely per file, not just              flagged pattern actually
   "this diff looks risky"                   safe here, e.g. exception
2. Diff-pattern flags reviewed —              re-raised elsewhere)
   distinguished from real evidence,       7. Missing-coverage files
   not treated as proof                       explicitly named, not
3. Structural blast radius grounded           silently accepted
   in real fan-in/hotspot data, not       8. Security implications
   guessed                                    considered (or explicit N/A)
4. Test coverage verified per file —      9. Evidence cited, not opinion
   covered vs. genuinely untested        10. Explicit assumption flag
   distinguished, not conflated               (evidence silent → state it,
5. Overall risk tier explained via the        don't guess)
   documented rule table, not asserted
```
Category 10 is the honesty valve — same convention as every prior
judgment-based skill's checklist in this project. An unresolved file means
the resolver found nothing to ground a structural assessment against, not
that the file is risk-free — say so explicitly (category 3) rather than
reading silence as safety.

### Step 4 — Produce the Regression Risk Record
Structure: `{files: [{path, diff_pattern_flags, structural_tier, callers,
test_coverage, overall_risk_tier, agent_assessment}], diff_summary,
security_notes, recommendation, assumptions}`. Render as JSON plus a
Markdown record a human can review quickly. This skill does not decide
merge/no-merge for the human — it produces the grounded material a human
(or the invoking agent, under human review) uses to record the actual call.

## Agent Responsibilities
- Never present a HIGH-risk, unflagged-but-uncovered file and a LOW-risk,
  covered file as equally safe to merge — the report's `overall_risk_tier`,
  `structural.structural_tier`, and `test_coverage.has_coverage` fields
  exist specifically so this distinction survives into the record.
- Never treat a fired diff-pattern flag as proof of a real regression, or
  its absence as proof of no regression — the pattern table is a fixed,
  non-exhaustive lead generator (ADR-007), not a verdict.
- Never read "no diff-pattern flag" as equivalent to "this file has no real
  structural risk" — these are independent axes that can and do diverge
  (a hotspot file with zero flagged lines is still structurally risky; see
  evaluation case-05).
- Never present an assumption as a derived fact — every place the engine's
  signals were silent or the diff gave no signal, category 10 must name the
  gap explicitly.
- Do not trust `structural.fan_in` as the complete caller picture without
  also checking `structural.caller_modules` — the two can diverge when
  `codebase-intelligence`'s own dependency graph misses an absolute-style
  cross-package import edge that this engine's own caller scan still finds
  (same class of gap as `refactoring-safety`'s L22).

## Tool Permissions
- Bash (to invoke `python -m engine.cli` for both `codebase-intelligence`
  and `regression-hunter`) — read-only usage only.
- Read/Grep (to read composed context, e.g. a CI log or an
  `adversarial-diff-reviewer` report, if used).
No write, network, or credential-accessing permissions are required or
granted, beyond writing this skill's own report output.

## Human Checkpoints
None required to produce a pre-decision report. A human should still
review and approve the actual merge, especially when any file's overall
risk tier is HIGH — this skill's output is an input to that review, not a
substitute for it, same discipline as `project-memory-bank/06-security-
model.md` requires and every prior judgment-based skill in this project
applies to its own highest-risk signal.

## Outputs
- `regression-hunter-report.json` — deterministic pre-decision packet:
  stats, per-file diff-pattern flags, structural assessment, test-coverage
  status, overall risk tier (see `engine/models.py`:
  `RegressionHunterReport`).
- `regression-hunter-report.md` — condensed version of the same, with the
  three axes kept visibly separate per file.
- The agent's own **Regression Risk Record** (Step 4), the actual
  merge-readiness judgment, is a separate artifact this skill's workflow
  produces, not emitted by the engine itself.

## Verification
- `pytest` (64 unit/integration/CLI tests as of v0.1.0, CLI test file
  written from the start — same discipline every prior phase since Phase 5
  established) — see `tests/`.
- `evaluations/regression-hunter/run_evaluation.py` against 8 fixture
  diffs (deterministic diff-pattern/structural/coverage layer) plus this
  session's actual checklist derivation for each (judgment layer) — see
  `evaluations/regression-hunter/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/regression-hunter/` for the full case set. Two layers
scored separately, per `project-memory-bank/05-evaluation-framework.md`:
deterministic diff-pattern-flag + structural-tier + coverage-status scoring
(Correctness/Efficiency, automated) and judgment-layer checklist-category
findings (Precision/Recall/False Positives/False Negatives against
hand-authored expected categories). The judgment-layer ground truth,
fixtures, and actual derivation were all produced by this same session's
agent — self-authored, single-rater evidence, not an inter-rater-agreement
experiment. This is the **eighth** judgment-based skill evaluated this
way; treat the resulting scores as evidence the workflow (including the
required codebase-intelligence composition) is executable and internally
consistent, not as evidence of real-world regression-detection quality. See
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
- Empty diff → engine returns a report with a warning and zero files, not
  a hard error — the agent should flag this rather than assessing a diff
  from nothing.
- No changed file resolves against the codebase-intelligence report → the
  engine adds an explicit warning; the agent must not treat this as
  evidence the diff is risk-free, only as evidence nothing could be
  structurally assessed.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: the
diff-pattern table (`engine/regression_patterns.py`) is a fixed set of five
mechanically-detectable shapes — it can both over-flag (e.g. an `except`
block removed because the surrounding `try` was also removed, i.e.
genuinely dead code) and under-flag (any regression shape not matching a
known pattern, which is most real regressions — same boundary every prior
Pattern 2 skill's anti-pattern table has, L7/L11/L15/L17/L18); a file that
fails to resolve against the composed report can mean "genuinely new,"
"the report predates this change," or "outside the scanned repo" — the
engine cannot distinguish these; test-coverage detection is a
static-import heuristic (a test module imports the file), not proof the
test currently passes or exercises the changed code path; and the
`modified-signature-no-test-change` pattern's "test file also changed"
check is a filename-convention match against files present in the SAME
diff, not a check against the full repository's test suite, so a
signature change covered by an existing, unmodified test will still be
flagged (a known, deliberate false-positive-leaning bias, same "leads not
verdicts" discipline as every other flag in this table). This is the
eighth judgment-based skill with single-rater, self-authored evaluation
evidence.

## Examples
See `examples/regression-hunter/example-run.md` for a real run of this
skill: a freshly regenerated `codebase-intelligence` report against this
platform's current (9-skill) repository state, composed into a real git
diff produced during this phase's own build.

## Provenance
Built in Phase 9 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`), reusing the Pattern 2 architecture
established by ADR-007 (deterministic pre-processor + agent-driven
workflow) an eighth time, and reusing `feature-planner`'s/
`root-cause-analyzer`'s/`architecture-decision`'s/`refactoring-safety`'s
required-composition rule (ADR-010) a fifth time, plus a new architectural
decision (ADR-015) introducing three explicitly separate, non-blended
regression signals per changed file (diff-pattern flags, structural blast
radius, test coverage), combined into one overall tier via a documented
rule table rather than a blended score — see
`project-memory-bank/03-architecture.md` and
`project-memory-bank/11-decisions.md`. Stdlib-only Python engine for the
deterministic layer (no runtime third-party dependencies, no cross-package
import of `codebase-intelligence` or `adversarial-diff-reviewer`); the
judgment layer is the invoking agent's own reasoning, not code.

## Changelog
- 0.2.0 — JVM support (ADR-022, user-directed cross-cutting scope, not a
  new roadmap phase): `test_coverage_scanner.py` and `is_test_shaped_path`
  both recognize the JVM `*Test`/`*Tests`/`*Spec` suffix convention;
  `touches_def_line` extended with real Java-method/Kotlin-`fun` line
  regexes. 4 new tests (66 → 70).
- 0.1.0 — Initial implementation: codebase-intelligence report loader
  (independent schema, required precondition, fifth reuse of ADR-010),
  unified-diff parser (independent copy of adversarial-diff-reviewer's
  parsing conventions), target resolver (exact-path + module-stem
  resolution against the composed report, real caller lookup via import
  scan), test-coverage scanner (static import-based heuristic, independent
  copy of refactoring-safety's pattern), diff-pattern regression scanner
  (removed exception handling, removed conditional guard, large unreplaced
  deletion, decreased test assertions, modified signature with no
  corresponding test-file change), risk scorer combining the three axes
  into an overall tier via a documented rule table (ADR-015), JSON/Markdown
  renderers keeping all three axes visibly separate, CLI with a CLI test
  file written from the start, evaluation harness with 8 fixtures plus a
  real dogfood example.
