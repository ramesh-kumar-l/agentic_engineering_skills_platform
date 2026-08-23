# Implementation Status

Compressed "save state" — what code actually exists and works, right now.
Update this at the end of every major feature (user directive, Phase 1).
Replaced/updated in place, not appended to chronologically — see
[[07-current-state]] for the same discipline applied to the whole repo.

## Skills

| Skill | Maturity | Trust Status | Tests | Evaluation |
|---|---|---|---|---|
| codebase-intelligence | Level 2 — Evaluated | EXPERIMENTAL | 23/23 passing | 4/4 fixtures passing, see `evaluations/codebase-intelligence/RESULTS.md` |
| adversarial-diff-reviewer | Level 2 — Evaluated | EXPERIMENTAL | 23/23 passing (was 19, +4 CLI tests added in Phase 3, see [[12-known-limitations]] L10) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored — see [[12-known-limitations]] L8); see `evaluations/adversarial-diff-reviewer/RESULTS.md` |
| acceptance-test-engineer | Level 2 — Evaluated | EXPERIMENTAL | 24/24 passing (was 20, +4 CLI tests added in Phase 4, see [[12-known-limitations]] L13) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, same caveat as above — see [[12-known-limitations]] L8); see `evaluations/acceptance-test-engineer/RESULTS.md` |
| feature-planner | Level 2 — Evaluated | EXPERIMENTAL | 21/21 passing | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, third time — see [[12-known-limitations]] L8); see `evaluations/feature-planner/RESULTS.md` |
| security-context-guard | Level 2 — Evaluated | EXPERIMENTAL | 58/58 passing (CLI test file written from the start, not discovered missing later) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, fourth time — see [[12-known-limitations]] L8); see `evaluations/security-context-guard/RESULTS.md` |
| root-cause-analyzer | Level 2 — Evaluated | EXPERIMENTAL | 32/32 passing (CLI test file written from the start, same discipline as Phase 5) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 7/8 fixtures perfect precision/recall, 1/8 (case-03) at 0.67/0.67 — first non-perfect score across five judgment-based skills, disclosed as-is (see [[12-known-limitations]] L8/L19); see `evaluations/root-cause-analyzer/RESULTS.md` |
| architecture-decision | Level 2 — Evaluated | EXPERIMENTAL | 34/34 passing (CLI test file written from the start, same discipline as Phases 5-6) | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall on all 8 fixtures (single-rater/self-authored, sixth time — see [[12-known-limitations]] L8); see `evaluations/architecture-decision/RESULTS.md` |

No other skill has any implementation yet. **215 total tests passing across
all seven skills.**

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

- Every other skill in the portfolio ([[08-roadmap]]) — Phase 8 onward, not
  started (Phase 8 is now Refactoring Safety — see [[08-roadmap]]'s Phase 7
  reordering note).
- Any reusable composed-workflow infrastructure across skills
  (feature-planner, root-cause-analyzer, and architecture-decision all make
  composition with codebase-intelligence mandatory at the single-skill
  level, ADR-010/ADR-012/ADR-013 — this is not the same as a multi-skill
  workflow engine, Phase 14).
- Any UI.
- Multi-runtime validation (only exercised via this session's agent so far).
- Independent-rater evaluation for any of the six judgment-based skills
  (L8, now applying six times) — needs a second, independent agent/session
  or real external usage.
- Experiment A and Experiment B at proper rigor (independent party, real
  task, real measurement) — only N=1 self-run pilots exist so far, see
  [[17-experiment-viability-check]]. Feature-planner's, root-cause-
  analyzer's, and architecture-decision's required-composition architecture
  (ADR-010, ADR-012, ADR-013) is real evidence composition executes
  correctly and is genuinely used, not evidence it outperforms the
  alternative — architecture-decision's own dogfood run is, if anything,
  evidence composition can execute correctly without being decisive on a
  real case (L21). A7's real qualitative-user-feedback experiment also
  remains unrun — Pilot C (Phase 5) is a floor, not a substitute.
- A keyword-collision-at-scale fix for the blast-radius/relevance scorers
  (L21) — disclosed, not scheduled; would need real evidence of need before
  investing in TF-IDF-style down-weighting or similar.

## Last updated

2026-08-23 — end of Phase 7.
