# Implementation Status

Compressed "save state" — what code actually exists and works, right now.
Update this at the end of every major feature (user directive, Phase 1).
Replaced/updated in place, not appended to chronologically — see
[[07-current-state]] for the same discipline applied to the whole repo.

## Skills

| Skill | Maturity | Trust Status | Tests | Evaluation |
|---|---|---|---|---|
| codebase-intelligence | Level 2 — Evaluated | EXPERIMENTAL | 42/42 passing (was 23, +1 test Phase 9 `*.egg-info` fix; +18 tests ADR-022 Java/Kotlin support, see [[12-known-limitations]] L32/L33) | 4/4 fixtures passing, see `evaluations/codebase-intelligence/RESULTS.md` |
| adversarial-diff-reviewer | Level 2 — Evaluated | EXPERIMENTAL | 29/29 passing (was 19, +4 CLI tests Phase 3, see [[12-known-limitations]] L10; +6 tests ADR-022 JVM risk patterns) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored — see [[12-known-limitations]] L8); see `evaluations/adversarial-diff-reviewer/RESULTS.md` |
| acceptance-test-engineer | Level 2 — Evaluated | EXPERIMENTAL | 24/24 passing (was 20, +4 CLI tests added in Phase 4, see [[12-known-limitations]] L13) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, same caveat as above — see [[12-known-limitations]] L8); see `evaluations/acceptance-test-engineer/RESULTS.md` |
| feature-planner | Level 2 — Evaluated | EXPERIMENTAL | 21/21 passing | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, third time — see [[12-known-limitations]] L8); see `evaluations/feature-planner/RESULTS.md` |
| security-context-guard | Level 2 — Evaluated | EXPERIMENTAL | 58/58 passing (CLI test file written from the start, not discovered missing later) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, fourth time — see [[12-known-limitations]] L8); see `evaluations/security-context-guard/RESULTS.md` |
| root-cause-analyzer | Level 2 — Evaluated | EXPERIMENTAL | 32/32 passing (CLI test file written from the start, same discipline as Phase 5) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 7/8 fixtures perfect precision/recall, 1/8 (case-03) at 0.67/0.67 — first non-perfect score across five judgment-based skills, disclosed as-is (see [[12-known-limitations]] L8/L19); see `evaluations/root-cause-analyzer/RESULTS.md` |
| architecture-decision | Level 2 — Evaluated | EXPERIMENTAL | 34/34 passing (CLI test file written from the start, same discipline as Phases 5-6) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, sixth time — see [[12-known-limitations]] L8); see `evaluations/architecture-decision/RESULTS.md` |
| refactoring-safety | Level 2 — Evaluated | EXPERIMENTAL | 65/65 passing (CLI test file written from the start, same discipline as Phases 5-7; +2 tests 2026-08-26 fixing L23; +1 test ADR-022 JVM test-suffix convention) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, seventh time — see [[12-known-limitations]] L8); see `evaluations/refactoring-safety/RESULTS.md` |
| regression-hunter | Level 2 — Evaluated | EXPERIMENTAL | 70/70 passing (CLI test file written from the start, same discipline as Phases 5-8; +2 tests 2026-08-26 fixing L23; +4 tests ADR-022 JVM test-suffix convention + touches_def_line extension) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, eighth time — see [[12-known-limitations]] L8); see `evaluations/regression-hunter/RESULTS.md` |
| release-readiness | Level 2 — Evaluated | EXPERIMENTAL | 84/84 passing (CLI test file written from the start, same discipline as Phases 5-9; +4 tests 2026-08-26 partially fixing L24; +2 tests ADR-022 JVM test-suffix convention + debug-println pattern) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, ninth time — see [[12-known-limitations]] L8); see `evaluations/release-readiness/RESULTS.md` |
| dependency-supply-chain | Level 2 — Evaluated | EXPERIMENTAL | 55/55 passing (CLI test file written from the start; +9 tests ADR-022 Maven/Gradle-aware pin classification) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, tenth time — see [[12-known-limitations]] L8); see `evaluations/dependency-supply-chain/RESULTS.md` |
| engineering-knowledge-capture | Level 2 — Evaluated | EXPERIMENTAL | 47/47 passing (CLI test file written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, eleventh time — see [[12-known-limitations]] L8); see `evaluations/engineering-knowledge-capture/RESULTS.md` |
| context-optimizer | Level 2 — Evaluated | EXPERIMENTAL | 64/64 passing (CLI test file written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, twelfth time — see [[12-known-limitations]] L8); real dogfood run found a new limitation (L29 — full-repository-scale keyword flooding); see `evaluations/context-optimizer/RESULTS.md` |
| workflow-composer | Level 2 — Evaluated | EXPERIMENTAL | 51/51 passing (CLI test file written from the start, plus one genuinely real subprocess-based integration test) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, thirteenth time — see [[12-known-limitations]] L8); real dogfood run found a new limitation (L30 — `feature-planner`'s scorer floods too, confirming the mechanism class is cross-skill); see `evaluations/workflow-composer/RESULTS.md` |
| engineering-memory | Level 2 — Evaluated | EXPERIMENTAL | 57/57 passing (CLI test file and a real end-to-end integration test written from the start) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, fourteenth time — see [[12-known-limitations]] L8); real dogfood run against this project's own 50-record memory bank found a new limitation (L31 — basename-exact module resolution collapses distinct same-basename files across skills into one arbitrarily-chosen match); see `evaluations/engineering-memory/RESULTS.md` |

This completes the originally-scoped 15-skill portfolio named in
[[08-roadmap]]. **733 total tests passing across all fifteen skills**
(42 + 29 + 24 + 21 + 58 + 32 + 34 + 65 + 70 + 84 + 55 + 47 + 64 + 51 + 57),
up from 693 after ADR-022 (Java/Kotlin multi-language support, 2026-08-29)
added 40 new tests across 6 skills (`codebase-intelligence`,
`adversarial-diff-reviewer`, `dependency-supply-chain`,
`refactoring-safety`, `regression-hunter`, `release-readiness`) — this is
new, user-directed, cross-cutting scope, NOT a new roadmap phase: Phase 15
(`engineering-memory`, 2026-08-26) already completed the originally-scoped
15-skill portfolio and there is still no Phase 16 in [[08-roadmap]]. The
other 9 skills' test counts and this file's Phase-15-era narrative below
are otherwise unchanged — started at the
user's explicit direction, a FIFTH one-time reopening of the
mentor-review pass's roadmap freeze (unlike Phase 14, this one did not
override a named phase-specific decision — A8's own "design only when
reached" gate was satisfied by reaching Phase 15 in order); A2/A5/A8
remain UNKNOWN, this is not new external-validation evidence — see
`12-known-limitations.md`, `11-decisions.md` (ADR-021), and
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

## engineering-memory — component status

| Component | Status |
|---|---|
| `engine/models.py` | Done, tested — `RecordStatus` enum, `MemoryRecord`/`ModuleFlag`/`StalenessFlag`/`RelevanceMatch`/`MemoryQueryReport` |
| `engine/ci_report_loader.py` | Done, tested — required-composition precondition (ADR-010, eleventh reuse) |
| `engine/memory_bank_parser.py` | Done, tested — parses real `## ADR-NNN:` / `## LNN:` section headers; explicitly skips `## L8 update:` sub-entries; derives `RecordStatus` from a `(FIXED...)`/`(SUPERSEDED...)` title suffix |
| `engine/module_resolver.py` | Done, tested — basename-EQUALITY (not containment) resolution against the real CI report's module list; see L31 for the real, disclosed residual ambiguity when multiple real files share a basename |
| `engine/keyword_extractor.py` | Done, tested — independently duplicated tokenizer, same technique as `context-optimizer`'s (no cross-skill import) |
| `engine/relevance_scorer.py` | Done, tested — whole-token overlap, title-weighted higher than body, plus a module-overlap boost |
| `engine/staleness_classifier.py` | Done, tested — combines record status + module-existence into one always-attached staleness flag, operationalizing A8's own named risk |
| `engine/stats.py` | Done, tested |
| `engine/report.py` | Done, tested — orchestrates parse → resolve → score → classify → stats; fails closed toward precision (`_MIN_SCORE_THRESHOLD`) |
| `engine/render_json.py` / `render_markdown.py` | Done, tested |
| `engine/cli.py` | Done, tested — `--task`/`--ci-report`/`--decisions-path`/`--limitations-path` all required; `--top-n` truncates after full scoring |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007) a fourteenth time + reuses ADR-010 an eleventh time + new ADR-021 (first self-referential composition, day-one word-boundary matching, normal fail-closed-toward-caution staleness default), includes agent-driven Step 3 workflow against the new Engineering Memory Retrieval Checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment), all 8 perfect on both layers; deterministic layer covers clean-fit, no-fit, whole-token collision resistance, both staleness paths, top-n truncation, the missing-report hard failure, and corpus-header-drift |
| Judgment-layer actual findings (`evaluations/engineering-memory/actual/`) | Done — this session's agent's real Engineering Memory Retrieval Checklist derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/engineering-memory/`) | Done — real, non-fixture retrieval run against this project's own actual `11-decisions.md`/`12-known-limitations.md` (50 real records) and a freshly-generated real CI report; found and disclosed a new limitation (L31 — basename-exact resolution collapses distinct same-basename files across the portfolio into one arbitrarily-chosen match, confirmed via `ci_report_loader.py`'s real recurrence across most composing skills) |

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

## Test Engineering Platform pivot (new, 2026-09-06 — separate from the skill table above)

TEP Phase 0 (repo/memory audit), TEP Phase 1 (Product Contract,
[[18-test-engineering-platform-contract]]), TEP Phase 2 (Evidence
Foundation), TEP Phase 3 (Project Intelligence extensions), TEP Phase 4
(Test Environment Discovery, Android/JVM specifically), TEP Phase 5a
(Test Strategy Engine), TEP Phase 5b's Scenario Planner sub-initiative,
TEP Phase 5c's Test Generation & Independent Validation sub-initiative,
and TEP Phase 5d's Security/Production Hardening sub-initiative are
complete; see [[11-decisions|ADR-023]], [[11-decisions|ADR-024]],
[[11-decisions|ADR-025]], [[11-decisions|ADR-026]], [[11-decisions|ADR-027]],
[[11-decisions|ADR-028]], [[11-decisions|ADR-029]], [[11-decisions|ADR-030]],
and `active-context.md`'s "What TEP Phase 1/2/3/4/5a/5b/5c/5d built".

TEP Phase 2 shipped one new, independently-packaged component:

- **`evidence/`** — run-provenance capture for existing skills.
  `schema.py` (49 lines), `git_info.py` (53), `skill_info.py` (42),
  `capture.py` (77), `store.py` (26), `cli.py` (51) — all under the
  300-line limit. 16 tests, all passing. Schema documented in
  [[19-evidence-provenance-schema]]. Demonstrated on a real run of
  `codebase-intelligence` against this repo (`examples/evidence/`), not a
  fixture. Own CI job added to `.github/workflows/tests.yml`, mirroring
  the existing per-skill matrix pattern.
- No existing skill's code was touched. The 15-skill portfolio's test
  count (733) is unchanged; `evidence/`'s 16 tests are a new, separate
  suite.

TEP Phase 3 shipped one new, independently-packaged component:

- **`project_intelligence/`** — derives a `TestEnvironmentProfile`
  (language, build system, test/mock/coverage tooling) from an existing
  `codebase-intelligence` report.json. `models.py` (52 lines),
  `ci_report_loader.py` (75), `signatures.py` (64), `detect.py` (68),
  `profile_builder.py` (70), `cli.py` (52) — all under the 300-line limit.
  20 tests, all passing. Schema documented in
  [[20-test-environment-profile-schema]]. Demonstrated on a real run
  against `skills/codebase-intelligence` itself (`examples/project-
  intelligence/`), not a fixture — the run also surfaced a real,
  previously-undocumented gap in `external_deps.py` (PEP 621 optional
  dependencies aren't parsed), now logged as [[12-known-limitations|L34]].
  Own CI job added. Also fixed a packaging defect shared with `evidence/`
  (flat module layout broke a clean `pip install -e`) — see
  [[11-decisions|ADR-025]].
- No existing skill's code was touched. Test counts: 733 (skills) + 16
  (evidence) unaffected; `project_intelligence/`'s 20 tests are a new,
  separate suite.

TEP Phase 4 extended the same `project_intelligence/` package (no new
package):

- Added Android-specific test-framework detection: `ANDROID_TEST_FRAMEWORK_
  SIGNATURES` (`signatures.py`), `detect_android_test_frameworks`
  (`detect.py`), and two new `TestEnvironmentProfile` fields —
  `android_test_frameworks: list[Finding]` and `android_frameworks_absent:
  list[str]` (explicit, individually-named absence for the JUnit/
  Robolectric/Espresso trio, never a guess). Module sizes after this
  change: `models.py` (61), `signatures.py` (85), `detect.py` (73),
  `profile_builder.py` (81), `ci_report_loader.py` (75, unchanged),
  `cli.py` (52, unchanged) — 428 lines total, still all under the 300-line
  limit. 25 tests total (5 new in `test_android_detection.py`, 5
  pre-existing ones updated for the new category's effect on
  `unavailable`), all passing.
- Demonstrated on a real Android repo (`android/architecture-samples`,
  `views` branch, `app/` module) — `examples/project-intelligence/
  android-example/`. The honest real result is "unavailable" for all three
  frameworks despite genuine source declarations, because every
  declaration uses Gradle variable interpolation, which the existing
  Gradle parser (L33) can't resolve — surfacing a new real finding, now
  logged as [[12-known-limitations|L35]]: this is the near-universal
  real-world convention on Android repos, not an edge case. See
  [[11-decisions|ADR-026]].
- No existing skill's code was touched, and `external_deps.py` was not
  modified (extending existing dependency output only, per the exit
  criteria). Test counts: 733 (skills) + 16 (evidence) unaffected;
  `project_intelligence/` grew from 20 to 25 tests.

TEP Phase 5a shipped one new, independently-packaged component:

- **`test_strategy/`** — decides which changed files (from a
  regression-hunter report) need a regression test, cross-checked against
  a project_intelligence TestEnvironmentProfile for the same repo.
  `models.py` (67 lines), `regression_report_loader.py` (71),
  `profile_loader.py` (53), `strategy_builder.py` (104), `cli.py` (70) —
  all under the 300-line limit (760 lines total including tests). 26
  tests, all passing. Schema documented in
  [[21-test-strategy-report-schema]]. Computes no risk score of its own —
  priority is copied directly from regression-hunter's `overall_risk_tier`,
  per the contract's "do not build a second, competing risk scorer"
  mandate.
- Demonstrated on a real diff (the historical commit that added
  `evidence/cli.py`, which genuinely still has no dedicated test file
  today) against a freshly-generated, full-repository `codebase-
  intelligence` report — `examples/test-strategy/`. The honest real result
  is zero targets flagged, because regression-hunter's own test-coverage
  scanner falsely reports the file as "covered" by unrelated skills'
  identically-stemmed `test_cli.py` files — an inherited instance of the
  already-disclosed L24 gap, now logged separately as
  [[12-known-limitations|L36]]. The positive "flagged" path is proven via 8
  of the 26 unit tests using synthetic fixtures. See
  [[11-decisions|ADR-027]].
- No existing skill's code was touched, and neither `regression-hunter`
  nor `project_intelligence` was modified — this package only reads their
  existing JSON outputs. Test counts: 733 (skills) + 16 (evidence) + 25
  (project_intelligence) unaffected; `test_strategy/`'s 26 tests are a new,
  separate suite.

TEP Phase 5b's Scenario Planner sub-initiative shipped one new,
independently-packaged component:

- **`scenario_planner/`** — composes a real `test_strategy` report's
  flagged targets with the real `regression-hunter` flags and
  `codebase-intelligence` structural listing they were derived from,
  proposing candidate test scenarios per target. `models.py` (82 lines),
  `strategy_targets_loader.py` (67), `regression_flags_loader.py` (71),
  `ci_module_loader.py` (57), `plan_builder.py` (150), `cli.py` (83) — all
  under the 300-line limit (517 engine lines total). 26 tests, all
  passing. Schema documented in [[22-scenario-plan-report-schema]].
  Computes no risk score and no line-level diff attribution — priority/
  feasibility/framework are copied verbatim from the input test_strategy
  target; every scenario cites either a regression-hunter flag's own
  description or a named function/class from codebase-intelligence's
  structural listing, per the contract's "do not build a second, competing
  risk scorer" mandate.
- Demonstrated by reusing the exact real, committed inputs from TEP Phase
  5a's own dogfood run — `examples/scenario-planner/`. The honest real
  result is zero plans, because the upstream test_strategy report already
  had zero targets (Phase 5a's own [[12-known-limitations|L36]] finding,
  surfacing one level further downstream by design — no new limitation
  entry needed). The positive "candidate scenarios" path is proven via 7 of
  the 26 unit tests using synthetic fixtures. See [[11-decisions|ADR-028]].
- No existing skill's code was touched, and neither `test_strategy`,
  `regression-hunter`, nor `codebase-intelligence` was modified — this
  package only reads their existing JSON outputs. Test counts: 733
  (skills) + 16 (evidence) + 25 (project_intelligence) + 26 (test_strategy)
  unaffected; `scenario_planner/`'s 26 tests are a new, separate suite.

TEP Phase 5c's Test Generation & Independent Validation sub-initiative
shipped two new, independently-packaged components:

- **`test_generation/`** — turns a real `scenario_planner` candidate list
  into a deterministic plan (real source excerpt, inferred/overridden
  naming convention, 1 positive + 4 negative slot requests) for an agent
  to author actual test files from. `models.py` (95 lines),
  `scenario_loader.py` (86), `source_excerpt_reader.py` (48),
  `naming_convention.py` (101), `generation_planner.py` (106), `cli.py`
  (81) — all under the 300-line limit (521 engine lines total). 30 tests,
  all passing. Schema documented in [[23-generation-plan-report-schema]].
  Never authors test code itself, per this phase's core design decision:
  codebase-intelligence's name-only structural listing can't support
  deriving real negative conditions, so that reasoning is left to the
  AI-judgment half of the deterministic-engine-plus-agent-judgment split.
- **`test_validation/`** — executes agent-authored test files against the
  target repo via subprocess and records real pass/fail evidence.
  `models.py` (61), `generated_tests_loader.py` (37),
  `environment_loader.py` (52), `validation_runner.py` (109),
  `report_builder.py` (49), `cli.py` (78) — all under the 300-line limit
  (386 engine lines total). 24 tests, all passing (6 real, non-mocked
  subprocess-execution tests, not just unit tests against stubs). Schema
  documented in [[24-validation-report-schema]]. This platform's first
  execution capability — every prior skill and TEP package is pure static
  analysis; disclosed explicitly, no filesystem/network sandboxing beyond
  a strict per-file timeout.
- Demonstrated twice, both real (`examples/test-generation/`,
  `examples/test-validation/`): once reusing TEP Phase 5b's exact real
  zero-candidate output, honestly reproducing that same inherited zero
  result; once against a synthetic-but-real scenario-plan-report.json
  naming an actual symbol in this repo, producing a real plan, a real
  agent-authored 5-test file (1 positive + 4 negative), and a real
  subprocess execution that actually passed. That real run found and
  fixed two real bugs — a relative-path resolution error in
  `validation_runner.py`, and an unfiltered `.pytest_cache` artifact being
  reported as a generated test in `generated_tests_loader.py` — that the
  51 unit tests written before it (all using absolute `tmp_path` fixtures)
  did not catch; both fixed with new regression tests. See
  [[11-decisions|ADR-029]].
- No existing skill's code was touched, and neither `scenario_planner` nor
  `project_intelligence` was modified — these packages only read their
  existing JSON outputs. Test counts: 733 (skills) + 16 (evidence) + 25
  (project_intelligence) + 26 (test_strategy) + 26 (scenario_planner)
  unaffected; `test_generation/`'s 30 tests and `test_validation/`'s 24
  tests are new, separate suites (148 total across every TEP package).

TEP Phase 5d's Security/Production Hardening sub-initiative modified five
existing files across five existing packages — no new package:

- **Path containment**: `test_validation/generated_tests_loader.py`'s
  `_is_real_candidate` and `evidence/skill_info.py`'s `resolve_skill_dir`
  now resolve+contain candidate paths, rejecting symlink- and
  traversal-based escapes accepted with no check before (48 and 51 lines
  respectively, up from 37 and 42).
- **Bounded subprocess capture**: `test_validation/validation_runner.py`
  redirects stdout/stderr to disk-backed `tempfile.TemporaryFile()`
  instead of in-memory `capture_output=True` (130 lines, up from 109) —
  bounds parent-process memory against a runaway test's unbounded output.
- **Resource caps**: `test_validation/report_builder.py` (77 lines, up
  from 49) and `cli.py` (92 lines, up from 79) add `--max-test-files`/
  `--max-test-file-bytes` (defaults 200 / 1 MB), skip + warn rather than
  hard-fail.
- **JSON loader type validation**: `test_strategy/profile_loader.py` (70,
  up from 53), `test_validation/environment_loader.py` (69, up from 52),
  `scenario_planner/ci_module_loader.py` (68, up from 57),
  `project_intelligence/ci_report_loader.py` (96, up from 75), and
  `test_generation/scenario_loader.py` (98, up from 86) now reject a
  wrong-type top-level container with their own typed error.
- **`pytest` runtime dependency**: `test_validation/pyproject.toml` moves
  `pytest>=7.0` to `dependencies`, paired with an `ensure_pytest_available()`
  precondition check in `validation_runner.py`.
- No new capability, no sandboxing claim added — every change narrows an
  already-existing risk surface. See [[11-decisions|ADR-030]].
- 20 new regression tests across 10 test files (2 of 3 new symlink tests
  skip gracefully on this Windows environment's unprivileged
  symlink-creation restriction). Test counts: 148 pre-existing + 20 new =
  166 passed, 3 skipped across the combined TEP suite. The real
  `test_validation` demo (`examples/test-validation/`) was re-run
  end-to-end post-hardening with the same clean result as before
  (`exit_code: 0`, `5 passed`), confirming no regression.

TEP Phase 5e and beyond is not started and needs its own explicit approval.

## Not yet built

- **No further skill is next by default.** Phase 15 (`engineering-memory`)
  completes the originally-scoped 15-skill portfolio named in
  [[08-roadmap]] — there is no Phase 16 in that list. Any further skill
  work is a newly-proposed scope, not "the next phase," and the roadmap
  freeze from the 2026-08-26 mentor-review pass still applies to it (see
  [[08-roadmap]]).
- A generic markdown indexer for `engineering-memory`'s corpus.
  `sprint-history/*.md`'s Lessons Learned sections are not parsed this
  pass — a real, disclosed corpus gap (see `SKILL.md` Known Limitations),
  not scheduled.
- A basename-disambiguation fix for `engineering-memory`'s
  `module_resolver.py` (L31) — disclosed via a real dogfood run, not
  scheduled; would need real evidence of need (a wrong `matched_modules`
  attribution actually misleading an agent) before investing in a fix.
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

2026-09-06 — TEP Phase 5d's Security/Production Hardening sub-initiative
for the Test Engineering Platform pivot ([[11-decisions|ADR-030]]). No new
package — five existing files hardened, each narrowing an already-existing
risk surface: path containment against symlink/traversal escapes in
`test_validation/generated_tests_loader.py` and `evidence/skill_info.py`;
bounded (disk-backed, not in-memory) subprocess stdout/stderr capture in
`validation_runner.py`; file-count/file-size resource caps in
`report_builder.py`/`cli.py`; wrong-type-container rejection in five JSON
loaders across `test_strategy`, `test_validation`, `scenario_planner`,
`project_intelligence`, and `test_generation`; and `pytest` declared as a
real runtime dependency of `test_validation`. No sandboxing claim
added — ADR-029's disclosure stands unchanged. 20 new regression tests
(166 passed, 3 skipped — Windows symlink-creation permission, confirmed via
`pytest -rs`, not a failure); the real `test_validation` demo was re-run
end-to-end post-hardening with the same clean result as before.

2026-09-06 — TEP Phase 5c's Test Generation & Independent Validation
sub-initiative for the Test Engineering Platform pivot
([[11-decisions|ADR-029]], [[23-generation-plan-report-schema]],
[[24-validation-report-schema]]). Two new packages: `test_generation/`
produces a deterministic plan (real source excerpt, naming convention, 1
positive + 4 negative slot requests) for an agent to author test files
from — it never authors code itself; `test_validation/` executes those
files via subprocess with a strict timeout, this platform's first
execution capability, with no filesystem/network sandboxing beyond that
timeout disclosed explicitly. 30 + 24 = 54 new tests, all passing (148
total across every TEP package). Demonstrated twice: an honest zero-result
run inheriting TEP Phase 5b's own L36 chain, and a real positive run
against an actual symbol in this repo that produced a real, agent-authored,
actually-executed, actually-passing test file — which itself found and
fixed two real bugs (a relative-path resolution error, an unfiltered
`.pytest_cache` artifact reported as a generated test) that the unit tests
written beforehand did not catch. TEP Phase 5d and beyond not started —
requires its own explicit approval.

2026-09-06 — TEP Phase 5b's Scenario Planner sub-initiative for the Test
Engineering Platform pivot ([[11-decisions|ADR-028]],
[[22-scenario-plan-report-schema]]). New `scenario_planner/` package
composes a real `test_strategy` report's flagged targets with the real
`regression-hunter` flags and `codebase-intelligence` structural listing
they came from, proposing candidate test scenarios, computing no risk
score and no line-level diff attribution; 26 tests, all passing.
Demonstrated by reusing TEP Phase 5a's own real, committed dogfood inputs;
the honest result — zero plans — is an inherited instance of Phase 5a's own
[[12-known-limitations|L36]] finding, surfacing one level further
downstream by design (no new limitation entry needed). No existing skill's
code changed, no change to test_strategy, regression-hunter, or
codebase-intelligence. TEP Phase 5c and beyond not started — requires its
own explicit approval.

2026-09-06 — TEP Phase 5a (Test Strategy Engine) for the Test Engineering
Platform pivot ([[11-decisions|ADR-027]], [[21-test-strategy-report-schema]]).
New `test_strategy/` package combines a real regression-hunter report with
a real project_intelligence TestEnvironmentProfile to decide which changed
files need a test, computing no risk score of its own; 26 tests, all
passing. Demonstrated on a real diff (the historical addition of
`evidence/cli.py`, still genuinely untested today) against a fresh,
full-repository codebase-intelligence report; the honest result — zero
targets flagged — surfaced a new finding (reusing regression-hunter's
test-coverage signal inherits its already-disclosed cross-skill
identical-stem false-positive gap, L24), logged as
[[12-known-limitations|L36]]. No existing skill's code changed, no change
to regression-hunter or project_intelligence. TEP Phase 5b and beyond not
started — requires its own explicit approval.

2026-09-06 — TEP Phase 4 (Test Environment Discovery, Android/JVM
specifically) for the Test Engineering Platform pivot
([[11-decisions|ADR-026]], [[20-test-environment-profile-schema]]).
Extended `project_intelligence` with Android JUnit/Robolectric/Espresso
detection; 20 → 25 tests. Demonstrated on a real Android repo
(`android/architecture-samples`); the honest result surfaced a new finding
(Gradle variable-versioned dependencies are near-universal on real Android
repos and the existing parser can't resolve them), logged as
[[12-known-limitations|L35]]. No existing skill's code changed, no change
to `external_deps.py`. TEP Phase 5 and beyond requires separate explicit
approval before any build starts.

2026-09-06 — TEP Phase 3 (Project Intelligence extensions) for the Test
Engineering Platform pivot ([[11-decisions|ADR-025]],
[[20-test-environment-profile-schema]]). New `project_intelligence`
package + 20 tests; no existing skill's code changed. Also fixed a
packaging defect in both `evidence/` and `project_intelligence/` (flat
module layout broke `pip install -e` on a clean checkout). TEP Phase 4
requires separate explicit approval before any build starts.

2026-09-06 — TEP Phase 2 (Evidence Foundation) for the Test Engineering
Platform pivot ([[11-decisions|ADR-024]], [[19-evidence-provenance-schema]]).
New `evidence/` package + 16 tests; no existing skill's code changed, 733
existing tests unaffected. See the updated section above. TEP Phase 3
requires separate explicit approval before any build starts.

2026-09-06 — TEP Phase 1 (Product Contract) for the newly-proposed Test
Engineering Platform pivot ([[11-decisions|ADR-023]],
[[18-test-engineering-platform-contract]]). No code, skill, or test count
changed.

2026-08-29 — ADR-022: Java/Kotlin multi-language support. User-directed,
cross-cutting scope (touching `codebase-intelligence` and 5 downstream
skills), NOT a new roadmap phase — the originally-scoped 15-skill
portfolio was already completed by Phase 15 (`engineering-memory`,
2026-08-26; see below) and there is still no Phase 16 in [[08-roadmap]].
733 total tests passing across fifteen skills (up from 693); the other 9
skills' counts are unchanged, confirmed via a full platform re-run (zero
regressions). A real dogfood run against a synthetic Java+Kotlin+Gradle
project confirmed the full pipeline end to end. See [[11-decisions]]
ADR-022 and [[12-known-limitations]] L32/L33.

2026-08-26 — end of Phase 15 (`engineering-memory`). Started at the
user's explicit direction, a FIFTH one-time reopening of the
mentor-review pass's roadmap freeze — unlike Phase 14, this reopening did
not override a named phase-specific decision (A8's own "design only when
reached" gate was satisfied by reaching Phase 15 in order) — now
deferred across five consecutive phase boundaries; 693 total tests
passing across fifteen skills (up from 636). A2/A5/A8 remain UNKNOWN —
this phase is not new external-validation evidence. This completes the
originally-scoped 15-skill portfolio named in [[08-roadmap]]; no Phase 16
exists in that list.
