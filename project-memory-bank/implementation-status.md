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
| acceptance-test-engineer | Level 2 — Evaluated | EXPERIMENTAL | 20/20 passing | 8/8 fixtures: deterministic layer 100% correct, judgment layer 100% precision/recall (single-rater/self-authored, same caveat as above — see [[12-known-limitations]] L8); see `evaluations/acceptance-test-engineer/RESULTS.md` |

No other skill has any implementation yet.

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
| `engine/cli.py` | Done, manually verified |
| `SKILL.md` contract | Done, all canonical template sections present, reuses Pattern 2 (ADR-007), includes agent-driven Step 3/4 workflow against the new acceptance-coverage checklist |
| Evaluation harness (`run_evaluation.py`) | Done, 8 fixtures, two-layer scoring (deterministic + judgment) |
| Judgment-layer actual findings (`evaluations/acceptance-test-engineer/actual/`) | Done — this session's agent's real derivation for each fixture, not fabricated to match ground truth |
| Dogfood example (`examples/acceptance-test-engineer/`) | Done — real requirement (adversarial-diff-reviewer's actual CLI behavior), surfaced and fixed L10 |
| `project-memory-bank/17-experiment-viability-check.md` | Done — Experiment A/B viability assessment + 2 explicitly-labeled internal pilots (not the real experiments) |

## Not yet built

- Every other skill in the portfolio ([[08-roadmap]]) — Phase 4 onward, not started.
- Any real composition/workflow layer across skills (only a one-off manual
  pilot exists — [[17-experiment-viability-check]] Pilot B — not reusable
  infrastructure).
- Any UI.
- Multi-runtime validation (only exercised via this session's agent so far).
- Independent-rater evaluation for either judgment-based skill (L8) — needs
  a second, independent agent/session or real external usage.
- Experiment A and Experiment B at proper rigor (independent party, real
  task, real measurement) — only N=1 self-run pilots exist so far, see
  [[17-experiment-viability-check]].

## Last updated

2026-08-23 — end of Phase 3.
