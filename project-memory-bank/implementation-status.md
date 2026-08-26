# Implementation Status

Compressed "save state" — what code actually exists and works, right now.
Update this at the end of every major feature (user directive, Phase 1).
Replaced/updated in place, not appended to chronologically — see
[[07-current-state]] for the same discipline applied to the whole repo.

## Skills

| Skill | Maturity | Trust Status | Tests | Evaluation |
|---|---|---|---|---|
| codebase-intelligence | Level 2 — Evaluated | EXPERIMENTAL | 24/24 passing (was 23, +1 test added in Phase 9 for a real `*.egg-info`-exclusion fix found via `regression-hunter`'s own dogfood run, see [[12-known-limitations]] and `examples/regression-hunter/example-run.md`) | 4/4 fixtures passing, see `evaluations/codebase-intelligence/RESULTS.md` |
| adversarial-diff-reviewer | Level 2 — Evaluated | EXPERIMENTAL | 23/23 passing (was 19, +4 CLI tests added in Phase 3, see [[12-known-limitations]] L10) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored — see [[12-known-limitations]] L8); see `evaluations/adversarial-diff-reviewer/RESULTS.md` |
| acceptance-test-engineer | Level 2 — Evaluated | EXPERIMENTAL | 24/24 passing (was 20, +4 CLI tests added in Phase 4, see [[12-known-limitations]] L13) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, same caveat as above — see [[12-known-limitations]] L8); see `evaluations/acceptance-test-engineer/RESULTS.md` |
| feature-planner | Level 2 — Evaluated | EXPERIMENTAL | 21/21 passing | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, third time — see [[12-known-limitations]] L8); see `evaluations/feature-planner/RESULTS.md` |
| security-context-guard | Level 2 — Evaluated | EXPERIMENTAL | 58/58 passing (CLI test file written from the start, not discovered missing later) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, fourth time — see [[12-known-limitations]] L8); see `evaluations/security-context-guard/RESULTS.md` |
| root-cause-analyzer | Level 2 — Evaluated | EXPERIMENTAL | 32/32 passing (CLI test file written from the start, same discipline as Phase 5) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 7/8 fixtures perfect precision/recall, 1/8 (case-03) at 0.67/0.67 — first non-perfect score across five judgment-based skills, disclosed as-is (see [[12-known-limitations]] L8/L19); see `evaluations/root-cause-analyzer/RESULTS.md` |
| architecture-decision | Level 2 — Evaluated | EXPERIMENTAL | 34/34 passing (CLI test file written from the start, same discipline as Phases 5-6) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, sixth time — see [[12-known-limitations]] L8); see `evaluations/architecture-decision/RESULTS.md` |
| refactoring-safety | Level 2 — Evaluated | EXPERIMENTAL | 64/64 passing (CLI test file written from the start, same discipline as Phases 5-7; +2 tests 2026-08-26 fixing L23) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, seventh time — see [[12-known-limitations]] L8); see `evaluations/refactoring-safety/RESULTS.md` |
| regression-hunter | Level 2 — Evaluated | EXPERIMENTAL | 66/66 passing (CLI test file written from the start, same discipline as Phases 5-8; +2 tests 2026-08-26 fixing L23) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, eighth time — see [[12-known-limitations]] L8); see `evaluations/regression-hunter/RESULTS.md` |
| release-readiness | Level 2 — Evaluated | EXPERIMENTAL | 82/82 passing (CLI test file written from the start, same discipline as Phases 5-9; +4 tests 2026-08-26 partially fixing L24) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, ninth time — see [[12-known-limitations]] L8); see `evaluations/release-readiness/RESULTS.md` |
| dependency-supply-chain | Level 2 — Evaluated | EXPERIMENTAL | 46/46 passing (CLI test file written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, tenth time — see [[12-known-limitations]] L8); see `evaluations/dependency-supply-chain/RESULTS.md` |
| engineering-knowledge-capture | Level 2 — Evaluated | EXPERIMENTAL | 47/47 passing (CLI test file written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, eleventh time — see [[12-known-limitations]] L8); see `evaluations/engineering-knowledge-capture/RESULTS.md` |
| context-optimizer | Level 2 — Evaluated | EXPERIMENTAL | 64/64 passing (CLI test file written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, twelfth time — see [[12-known-limitations]] L8); real dogfood run found a new limitation (L29 — full-repository-scale keyword flooding); see `evaluations/context-optimizer/RESULTS.md` |
| workflow-composer | Level 2 — Evaluated | EXPERIMENTAL | 51/51 passing (CLI test file written from the start, plus one genuinely real subprocess-based integration test) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, thirteenth time — see [[12-known-limitations]] L8); real dogfood run found a new limitation (L30 — `feature-planner`'s scorer floods too, confirming the mechanism class is cross-skill); see `evaluations/workflow-composer/RESULTS.md` |

No other skill has any implementation yet. **636 total tests passing across
all fourteen skills** (24 + 23 + 24 + 21 + 58 + 32 + 34 + 64 + 66 + 82 + 46 + 47 + 64 + 51),
up from 585 after Phase 14 (`workflow-composer`, 2026-08-26) added the
fourteenth skill — started at the user's explicit direction, a FOURTH
one-time reopening of the mentor-review pass's roadmap freeze, and the
first to also directly override a named, phase-specific decision (A10's
"do not build Workflow Composer until Experiment B can be run"), now
deferred across four consecutive phase boundaries; A2/A5/A10 remain
UNKNOWN, this is not new external-validation evidence — see
`12-known-limitations.md`, `11-decisions.md` (ADR-020), and
`active-context.md`.

## codebase-intelligence — component status

| Component | Status |
|---|---|
| `engine/scanner.py` | Done, tested |
| `engine/python_parser.py` | Done, tested (includes AST-based main-guard fix, see [[12-known-limitations]] L1) |
| `engine/generic_parser.py` | Done, tested — heuristic only, see [[12-known-limitations]] L3 |
| `engine/graph.py` | Done, tested |
| `engine/external_deps.py` | Done, tested — root-only, see [[12-known-limitations]] L2 |
| `engine/report.py` | Done, tested |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, manually verified via dogfood run |
| `SKILL.md` contract | Done, all canonical template sections present |
| Evaluation harness (`run_evaluation.py`) | Done, 4 fixtures, all passing |
| Dogfood example (`examples/codebase-intelligence/`) | Done — surfaced and fixed L1 |

## adversarial-diff-reviewer — component status

| Component | Status |
|---|---|
| `engine/diff_parser.py` | Done, tested — unified diff -> structured hunks/files |
| `engine/risk_patterns.py` | Done, tested — 11 patterns (secrets, dangerous calls, broad except, SQL injection shapes, debug leftovers, TODO markers) |
| `engine/risk_scanner.py` | Done, tested — in-place secret redaction, fixed twice during dogfooding (L5, L6) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — 4 CLI tests added in Phase 3 (`tests/test_cli.py`) after dogfooding acceptance-test-engineer surfaced this had zero coverage, see [[12-known-limitations]] L10 |
| `SKILL.md` contract | Done, all canonical template sections present, includes the agent-driven Step 3/4 workflow |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/adversarial-diff-reviewer/actual/`) | Done — this session's agent's real review of each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/adversarial-diff-reviewer/`) | Done — real in-session diff, surfaced and fixed L6 |

## acceptance-test-engineer — component status

| Component | Status |
|---|---|
| `engine/requirement_parser.py` | Done, tested — free text -> structured sentences |
| `engine/patterns.py` | Done, tested — vague-term/weak-modal per-sentence patterns + 2 whole-document absence checks |
| `engine/testability_scanner.py` | Done, tested |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested |
| `engine/render_json.py` / `render_markdown.py` | Done, tested — Markdown includes Gherkin-ready structure |
| `engine/cli.py` | Done, tested — 4 CLI tests added in Phase 4 (`tests/test_cli.py`) after dogfooding feature-planner against a real task surfaced this had zero coverage, see [[12-known-limitations]] L13 |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007), includes agent-driven Step 3/4 workflow against the new acceptance-coverage checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/acceptance-test-engineer/actual/`) | Done — this session's agent's real derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/acceptance-test-engineer/`) | Done — real requirement (adversarial-diff-reviewer's actual CLI behavior), surfaced and fixed L10 |
| `project-memory-bank/17-experiment-viability-check.md` | Done — Experiment A/B viability assessment + 2 explicitly-labeled internal pilots (not the real experiments) |

## feature-planner — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — loads a codebase-intelligence report.json into a local, independent schema; missing/malformed report is a hard failure (ADR-010) |
| `engine/relevance_scorer.py` | Done, tested — keyword-overlap scoring of ci_report modules, annotated with fan_in/fan_out/hotspot blast-radius signal; known ranking limitation, see [[12-known-limitations]] L14 |
| `engine/planning_patterns.py` / `planning_scanner.py` | Done, tested — vague-scope/weak-goal-modal patterns + 2 whole-text absence checks (mirrors acceptance-test-engineer's scanner) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — requires `--ci-report` (required, not optional), exits non-zero with an actionable error if missing/malformed |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) + new ADR-010 (required composition), includes agent-driven Step 3/4 workflow against the new Plan Quality checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures (each pairing a task.txt with a synthetic ci_report.json), two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/feature-planner/actual/`) | Done — this session's agent's real plan derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/feature-planner/`) | Done — fresh codebase-intelligence report regenerated against this repo's current (4-skill) state, real task, surfaced and fixed L13 (acceptance-test-engineer CLI coverage gap) and documented L14 (relevance-ranking limitation, not fixed) |

## security-context-guard — component status

| Component | Status |
|---|---|
| `engine/secret_patterns.py` | Done, tested — 4 patterns (generic credential assignment, private key header, AWS access key ID, bearer token) |
| `engine/pii_patterns.py` | Done, tested — 4 patterns (email, phone, SSN-shaped, credit-card-shaped) |
| `engine/sensitive_paths.py` | Done, tested — filename/path convention table (.env, *.pem, id_rsa*, credentials.json, .aws/credentials, secrets.*) |
| `engine/action_patterns.py` | Done, tested — keyword table for the six high-risk action categories; verb+object categories matched by same-sentence co-occurrence, fixed after a real dogfood run found a fixed-window bug (L16) |
| `engine/scanner.py` | Done, tested — orchestrates matching + in-place redaction (every occurrence, not just the first) |
| `engine/classification.py` | Done, tested — deterministic sensitivity/suggested_verdict rollup, fails closed on inconclusive input |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — optional `--ci-report` hotspot enrichment; a missing/unreadable report is a warning, never a failure (unlike feature-planner's ADR-010) |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, not discovered missing via a later dogfood run |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a fourth time + new ADR-011 (engine classifies/recommends, never authorizes), includes agent-driven Step 3/4 workflow against the new Security Decision Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/security-context-guard/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/security-context-guard/`) | Done — real source file + a real pending git-push decision this session actually faced; surfaced and fixed L16; doubles as Pilot C toward A7 |

## root-cause-analyzer — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as feature-planner's loader (ADR-010, reused); own independent copy, no cross-package import |
| `engine/stack_trace_parser.py` | Done, tested — two shapes: Python tracebacks (`File "path", line N, in symbol`) and generic `path:line` |
| `engine/candidate_scorer.py` | Done, tested — two evidence tiers (stack-trace dominant flat bonus vs. keyword-overlap fallback, ADR-012); reuses relevance_scorer.py's weighting scheme for the keyword tier |
| `engine/symptom_patterns.py` / `symptom_scanner.py` | Done, tested — vague-symptom-language patterns + missing expected/actual, missing repro, missing error-signal absence checks (mirrors feature-planner's planning_patterns.py) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/ADR-012); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, same discipline Phase 5 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a fifth time + reuses ADR-010 a second time + new ADR-012 (tiered evidence scoring), includes agent-driven Step 3/4 workflow against the new Root Cause Investigation checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/root-cause-analyzer/actual/`) | Done — this session's agent's real investigation derivation for each fixture, not fabricated to match ground truth; one fixture (case-03) scored imperfectly, left as-is |
| Dogfood example (`examples/root-cause-analyzer/`) | Done — fresh codebase-intelligence report against this repo's current (6-skill) state + a real, retrospective symptom (Phase 5's own L16 defect, described without naming the file); correctly ranked the true root-cause file first out of 122 scored modules |

## architecture-decision — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as feature-planner's/root-cause-analyzer's loader (ADR-010, reused a third time); own independent copy, no cross-package import |
| `engine/option_parser.py` | Done, tested — three shapes: explicit `Option A:` markers, numbered/lettered lists, `vs`/`versus` single-line fallback; falls back to a single "proposed" option if none match |
| `engine/decision_patterns.py` / `decision_scanner.py` | Done, tested — vague-decision-language pattern + missing-alternatives/reversibility/tradeoff/security absence checks (mirrors root-cause-analyzer's symptom_patterns.py); tradeoff pattern extended post-dogfood to also catch the verb form "trades X for Y" (L20) |
| `engine/impact_scorer.py` | Done, tested — per-option blast-radius scoring: keyword-relevance rollup into a low/medium/high tier driven by real fan-in/hotspot data (ADR-013); shares feature-planner's/root-cause-analyzer's coincidental-substring limitation, sharpened at full-repo scale (L21, not fixed) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/ADR-013); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, same discipline Phases 5-6 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a sixth time + reuses ADR-010 a third time + new ADR-013 (per-option blast-radius tiering), includes agent-driven Step 3/4 workflow against the new Architecture Decision Record checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/architecture-decision/actual/`) | Done — this session's agent's real decision-record derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/architecture-decision/`) | Done — fresh codebase-intelligence report against this repo's current (7-skill) state + a real decision this phase's own build faced (required vs. optional composition); found and fixed L20, disclosed and left L21 |

## refactoring-safety — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as feature-planner's/root-cause-analyzer's/architecture-decision's loader (ADR-010, reused a fourth time); own independent copy, no cross-package import |
| `engine/operation_parser.py` | Done, tested — 8 fixed operation types (rename/delete/move/change-signature/split/merge/extract/inline) + generic "refactor" fallback; backtick/quote-first target extraction, bare-identifier fallback (underscore/dotted/internal-capital heuristic, excludes sentence-initial capitals) |
| `engine/target_resolver.py` | Done, tested — resolves each target against the codebase-intelligence report (module-stem, function-name, class-name matching); finds real callers via independent import-list substring scan (not the report's own `fan_in` — see L22) |
| `engine/test_coverage_scanner.py` | Done, tested — independent static heuristic: does a test-shaped module (`tests/` dir or `test_*`/`*_test` filename) import the target |
| `engine/safety_scorer.py` | Done, tested — per-target risk tier (ADR-014): boundary-changing operations scored against real fan-in, internal-only operations scored against hotspot status; raises a distinct `untested-blast-radius` flag rather than blending risk and coverage into one score |
| `engine/safety_patterns.py` / `safety_scanner.py` | Done, tested — vague-refactor-language pattern + missing-test-plan/rollback/caller-update/verification absence checks (mirrors architecture-decision's decision_patterns.py) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/ADR-014); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, same discipline Phases 5-7 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a seventh time + reuses ADR-010 a fourth time + new ADR-014 (per-target risk tier + independent test-coverage signal), includes agent-driven Step 3/4 workflow against the new Refactoring Safety Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/refactoring-safety/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/refactoring-safety/`) | Done — fresh codebase-intelligence report against this repo's current (8-skill) state + a real refactor this phase's own build produced (duplicated path-stem helper); disclosed, not fixed, a new cross-skill limitation (L22) |

## regression-hunter — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as feature-planner's/root-cause-analyzer's/architecture-decision's/refactoring-safety's loader (ADR-010, reused a fifth time); own independent copy, no cross-package import |
| `engine/diff_parser.py` | Done, tested — unified diff -> structured ChangedFile/Hunk/LineChange, independent copy of adversarial-diff-reviewer's parsing conventions |
| `engine/target_resolver.py` | Done, tested — resolves each changed file's effective path against the codebase-intelligence report (exact-path + module-stem matching); finds real callers via independent import-list substring scan (same pattern as refactoring-safety's, same L23 substring-collision limitation) |
| `engine/test_coverage_scanner.py` | Done, tested — independent static heuristic: does a test-shaped module import the resolved file, same pattern as refactoring-safety's |
| `engine/regression_patterns.py` / `regression_scanner.py` | Done, tested — 5 diff-pattern checks scanned directly against the diff's own hunks (removed exception handling, removed conditional guard, large unreplaced deletion, decreased test assertions, modified signature with no corresponding test-file change) — the genuinely new Axis 1 this phase introduces |
| `engine/risk_scorer.py` | Done, tested — combines Axis 1 (flags) + Axis 2 (structural tier) + Axis 3 (test coverage) into one `overall_risk_tier` per file via a documented rule table (ADR-015), while keeping all three axes visible as separate fields |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/ADR-015); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested — Markdown keeps all three axes visibly separate per file |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, same discipline Phases 5-8 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) an eighth time + reuses ADR-010 a fifth time + new ADR-015 (three-axis, non-blended regression-risk scoring), includes agent-driven Step 3/4 workflow against the new Regression Risk Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/regression-hunter/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/regression-hunter/`) | Done — fresh codebase-intelligence report against this repo's current (9-skill) state + a real `git diff` (a genuine, already-tested `codebase-intelligence` scanner fix this phase's own build produced); disclosed, not fixed, a new cross-skill limitation (L23) |

## release-readiness — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as every prior composing skill's loader (ADR-010, reused a sixth time); own independent copy, no cross-package import |
| `engine/diff_parser.py` | Done, tested — unified diff -> structured ChangedFile/Hunk/LineChange, independent copy of adversarial-diff-reviewer's/regression-hunter's parsing conventions |
| `engine/target_resolver.py` | Done, tested — resolves each changed file's effective path against the codebase-intelligence report; THIRD independent copy of the substring-matching pattern already disclosed as L23, now also shown to affect test-coverage matching (L24) |
| `engine/test_coverage_scanner.py` | Done, tested — independent static heuristic, same pattern as refactoring-safety's/regression-hunter's, shares L24's false-positive-coverage gap |
| `engine/blast_radius_scorer.py` | Done, tested — structural tier from real fan-in/hotspot data |
| `engine/hygiene_patterns.py` / `hygiene_scanner.py` | Done, tested — release-blocking anti-pattern table (debug leftovers, TODO-blocking markers, hardcoded-secret-shaped literals, merge-conflict markers), the genuinely new Axis 1 this phase introduces |
| `engine/regression_report_loader.py` / `security_report_loader.py` | Done, tested — OPTIONAL composition with regression-hunter's/security-context-guard's own reports (ADR-011 precedent, not ADR-010's mandatory rule); missing/malformed input is a warning, never a failure |
| `engine/readiness_scorer.py` | Done, tested — per-file readiness_tier from Axes 1-3 only (ADR-016's rule table), report-level overall_verdict rollup; Axis 4/5 evidence surfaced but deliberately not blended in |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/016); missing/malformed report is a hard failure; `--regression-report`/`--security-report` are optional |
| `engine/render_json.py` / `render_markdown.py` | Done, tested — Markdown keeps every axis visibly separate per file, and states the verdict is advisory in the document itself |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start this phase, same discipline Phases 5-9 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a ninth time + reuses ADR-010 a sixth time + new ADR-016 (Release Readiness Scorecard, three always-available axes + two optional surfaced-not-blended axes), includes agent-driven Step 4 workflow against the new Release Readiness Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/release-readiness/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/release-readiness/`) | Done — fresh codebase-intelligence report against this repo's current (10-skill) state + a real, staged-then-unstaged (never committed) `git diff` of this phase's own 78 new files; confirmed a predicted false-positive shape, disclosed a new cross-skill limitation (L24) |

## dependency-supply-chain — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as every prior composing skill's loader (ADR-010, reused a seventh time); own independent copy, extracts only `external_dependencies` |
| `engine/pin_checker.py` | Done, tested — classifies missing/wildcard/range/pinned across pip- and npm-style version specifiers |
| `engine/risk_patterns.py` | Done, tested — 5-entry curated known-risk-name table, each citing a real public incident; exact-name matching (not substring), verified against a `request`/`requests` false-positive case |
| `engine/duplicate_detector.py` | Done, tested — flags same dependency name declared with conflicting versions across manifests |
| `engine/surface_area.py` | Done, tested — total/unpinned-count/unpinned-% and per-manifest breakdown |
| `engine/scanner.py` | Done, tested — orchestrates pin/known-risk/duplicate detection; NOT implemented: license-risk detection (ADR-017, L26 — no per-dependency license data exists to detect from) |
| `engine/risk_scorer.py` | Done, tested — advisory-only `suggested_risk_level`, fails closed to REQUIRES_REVIEW on zero dependencies or CI warnings (ADR-011 precedent) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/017); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start, same discipline Phases 5-10 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a tenth time + reuses ADR-010 a seventh time + new ADR-017 (no live CVE/license-risk scope decisions, ADR-011 fail-closed reuse), includes agent-driven Step 3 workflow against the new Dependency Risk Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/dependency-supply-chain/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/dependency-supply-chain/`) | Done — real run against this repo's own root manifest; concretely confirmed the inherited L2 root-level-only scope gap (only 1 of the platform's real dependencies visible from repo root) |

## engineering-knowledge-capture — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as every prior composing skill's loader (ADR-010, reused an eighth time); own independent copy, extracts modules + dependency_graph |
| `engine/knowledge_patterns.py` | Done, tested — 16 patterns across 4 categories (decision/lesson/limitation/workaround), non-exhaustive |
| `engine/knowledge_scanner.py` | Done, tested — one candidate per match, not collapsed per pattern (a narrative can describe several distinct decisions/lessons) |
| `engine/location_resolver.py` | Done, tested — FOURTH independent copy of the word-boundary-aware containment check (L23/L24 lineage), first one built correct from the start rather than fixed after disclosure |
| `engine/priority_scorer.py` | Done, tested — fail-closed-to-MEDIUM discipline (ADR-011/017 reuse); LOW band defined but never assigned this version (see SKILL.md Known Limitations) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/018); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start, same discipline Phases 5-11 established |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) an eleventh time + reuses ADR-010 an eighth time + new ADR-018 (word-boundary-correct-from-day-one resolver, fail-upward priority default, first documentation-artifact-targeting skill), includes agent-driven Step 3 workflow against the new Knowledge Capture Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/engineering-knowledge-capture/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/engineering-knowledge-capture/`) | Done — real narrative built from verbatim excerpts of this project's own engineering history (the L23/L24 fix, Phase 11's dropped license-detection decision), composed with a fresh codebase-intelligence report; found and disclosed a new limitation (L28) rather than confirming a known one |

## context-optimizer — component status

| Component | Status |
|---|---|
| `engine/ci_report_loader.py` | Done, tested — same required-precondition pattern as every prior composing skill's loader (ADR-010, reused a ninth time); own independent copy, joins `files` (real line_count) with `modules` (structural metadata) by path |
| `engine/keyword_extractor.py` | Done, tested — stopword-filtered tokenizer, splits on `_`/`/`/`.`/`-`; shared by `relevance_scorer.py` for consistent tokenization on both sides of a match |
| `engine/relevance_scorer.py` | Done, tested — FIFTH independent copy of a whole-token containment check (L23/L24 lineage); tokenized (not `\b`-regex), a disclosed different precision/recall tradeoff than `location_resolver.py`'s |
| `engine/structural_booster.py` | Done, tested — hotspot/high-fan-in boost, ADR-013-style reuse |
| `engine/size_estimator.py` | Done, tested — crude, disclosed tokens-per-line heuristic, not a real tokenizer |
| `engine/budget_selector.py` | Done, tested — CORE/SUPPORTING/EXCLUDED tiering; fail-OPEN-toward-inclusion under uncertainty (ADR-019, inverts ADR-011/017/018's fail-closed convention) |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — `--ci-report` is required (ADR-010/019); missing/malformed report is a hard failure |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — CLI test file (`tests/test_cli.py`) written from the start, same discipline Phases 5-12 established; `--budget-lines` optional flag |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a twelfth time + reuses ADR-010 a ninth time + new ADR-019 (tokenized relevance scorer, fail-OPEN inversion, crude token-estimate disclosure), includes agent-driven Step 3 workflow against the new Context Optimization Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers |
| Judgment-layer actual findings (`evaluations/context-optimizer/actual/`) | Done — this session's agent's real checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/context-optimizer/`) | Done — real task description from this actual session, composed with a fresh codebase-intelligence report against this repo's current state; found and disclosed a new limitation (L29 — full-repository-scale keyword flooding) rather than confirming a known one |

## workflow-composer — component status

| Component | Status |
|---|---|
| `engine/models.py` | Done, tested — `WiringMode`/`StepStatus` enums, `WorkflowStep`/`WorkflowTemplate`/`StepResult`/`WorkflowRunReport`/`CompatibilityIssue` |
| `engine/workflow_registry.py` | Done, tested — 3 hardcoded templates, each reusing a composition already run for real in an earlier phase's dogfood (Phase 4, Phase 3's Pilot B, Phase 13) |
| `engine/skill_locator.py` | Done, tested — resolves a registry skill name to its real on-disk `engine/cli.py`; fails closed (`SkillNotFoundError`) if missing |
| `engine/compatibility_checker.py` | Done, tested — textual drift guard: confirms the upstream skill's name still appears in the downstream skill's real SKILL.md Preconditions/Required Context sections |
| `engine/step_runner.py` | Done, tested — owns the only `subprocess.run` call; builds each step's real CLI argv per its declared `WiringMode`; `TEXT_APPEND` mode reproduces Phase 3's real Pilot B composition (appends a CI excerpt into the requirement text, since `acceptance-test-engineer` has no `--ci-report`-style flag) |
| `engine/executor.py` | Done, tested — sequences steps; fails CLOSED (ADR-020): a compatibility issue blocks all real execution outright, and any step's failure marks every remaining step SKIPPED |
| `engine/stats.py` | Done, tested |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — `--dry-run` validates the plan with zero subprocess calls; `--list-templates` prints the registry |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a thirteenth time + reuses ADR-010 a tenth time + new ADR-020 (first skill executing other skills' real code, fail-closed execution default, hardcoded 3-template registry), includes agent-driven Step 4 workflow against the new Workflow Composition Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers; deterministic layer mixes real registry-template runs (against a bundled tiny fixture repo) with fixture fake-skill runs (for deterministic fail-closed-path coverage) |
| Judgment-layer actual findings (`evaluations/workflow-composer/actual/`) | Done — this session's agent's real Workflow Composition Checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/workflow-composer/`) | Done — real, non-dry-run execution of `understand-then-plan` against this repo's own current (fourteen-skill) state, using this session's own real task description; found and disclosed a new limitation (L30 — `feature-planner`'s own scorer floods too, confirming L14/L19/L21/L29's mechanism class is shared across skills, not specific to `context-optimizer`) |

## Documentation & public-facing artifacts (added after Phase 5, not a phase)

| Artifact | Status |
|---|---|
| `requirements.txt` (root) | Done — the one real dependency (`pytest>=7.0`), documented as intentional |
| `DEPENDENCIES.md` (root) | Done — explains the zero-runtime-dependency choice, ties to ADR-006 |
| `QuickStarterGuide.md` (root) | Done — first-run walkthrough, test/eval instructions, composition example, FAQ |
| `README.md` (root) | Rewritten — full production-grade rewrite (was a short pointer file); includes architecture diagrams, evaluation-honesty section, real-bug table |
| `blogs/` (5 posts + index) | Done — technical deep-dive series for external publication, verified against real code/data, not reconstructed from memory |
| `skills/*/README.md` (all five) | Updated — added a `**Status**` line (test counts, trust status, ADR references, relevant blog link) to each |

No code, tests, `SKILL.md` contracts, or evaluation harnesses changed in
this pass — test count and evaluation results are unchanged from the Phase
5 completion state (149/149 passing).

## Not yet built

- Every other skill in the portfolio ([[08-roadmap]]) — Phase 15
  (`engineering-memory`) onward, not started; the roadmap freeze from the
  2026-08-26 mentor-review pass still applies to any further phase beyond
  Phase 14 (see [[08-roadmap]]).
- A generic, arbitrary multi-skill chainer. `workflow-composer` (Phase 14)
  ships a real, execution-capable engine, but deliberately bounded to 3
  hardcoded, previously-dogfooded templates (ADR-020) — not a config-driven
  composer that can chain any two skills on demand.
- Any UI.
- Multi-runtime validation (only exercised via this session's agent so far).
- Independent-rater evaluation for any of the ten judgment-based skills
  (L8, now applying ten times) — needs a second, independent agent/session
  or real external usage.
- Experiment A and Experiment B at proper rigor (independent party, real
  task, real measurement) — only N=1 self-run pilots exist so far, see
  [[17-experiment-viability-check]]. Feature-planner's, root-cause-
  analyzer's, architecture-decision's, refactoring-safety's, regression-
  hunter's, and release-readiness's required-composition architecture
  (ADR-010, ADR-012, ADR-013, ADR-014, ADR-015, ADR-016) is real evidence
  composition executes correctly and is genuinely used, not evidence it
  outperforms the alternative — architecture-decision's dogfood run is
  evidence composition can execute correctly without being decisive on a
  real case (L21); refactoring-safety's, regression-hunter's, and
  release-readiness's dogfood runs are evidence composition can execute
  correctly while still depending on upstream data, or a shared resolution
  pattern, whose own internal consistency has gaps (L22, L23, L24). A7's
  real qualitative-user-feedback experiment also remains unrun — Pilot C
  (Phase 5) is a floor, not a substitute.
- A keyword-collision-at-scale fix for the blast-radius/relevance scorers
  (L21), a fan_in-undercounting fix for codebase-intelligence's
  dependency-graph builder (L22), and a substring-collision fix for the
  shared `target_resolver.py` caller-identification/test-coverage pattern
  (L23, L24 — now affecting three skills' independent copies) — all
  disclosed, not scheduled; would need real evidence of need before
  investing in a fix.

- A live CVE/vulnerability-database lookup and real per-dependency license
  detection for `dependency-supply-chain` (L25, L26) — both explicit scope
  decisions, not scheduled; would need real evidence of need (network
  access and installed-package-metadata inspection are both capabilities
  this project has deliberately not built).
- A paragraph-scoped (rather than single-line-scoped) resolution window for
  `engineering-knowledge-capture`'s `location_resolver.py` (L28) — disclosed
  via a real dogfood run, not scheduled; would need real evidence the
  recall gain is worth the precision risk before widening the window.
- A corpus-vocabulary down-weighting fix (TF-IDF-style, or a minimum
  keyword-specificity threshold) shared across `architecture-decision`'s
  `impact_scorer.py` (L21), `context-optimizer`'s `relevance_scorer.py`
  (L29), and `feature-planner`'s `relevance_scorer.py` (L30) — disclosed
  via three separate real dogfood runs now, not scheduled; the case for
  addressing the shared mechanism class strengthens with each new
  instance without yet being acted on.

## Last updated

2026-08-26 — end of Phase 14 (`workflow-composer`). Started at the user's
explicit direction, a FOURTH one-time reopening of the mentor-review
pass's roadmap freeze — the first to also directly override a named,
phase-specific decision (A10) rather than only the general freeze — now
deferred across four consecutive phase boundaries; 636 total tests
passing across fourteen skills (up from 585). A2/A5/A10 remain UNKNOWN —
this phase is not new external-validation evidence.
