# Implementation Status

Compressed "save state" — what code actually exists and works, right now.
Update this at the end of every major feature (user directive, Phase 1).
Replaced/updated in place, not appended to chronologically — see
[[07-current-state]] for the same discipline applied to the whole repo.

## Skills

| Skill | Maturity | Trust Status | Tests | Evaluation |
|---|---|---|---|---|
| codebase-intelligence | Level 2 — Evaluated | EXPERIMENTAL | 23/23 passing | 4/4 fixtures passing, see `evaluations/codebase-intelligence/RESULTS.md` |

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

## Not yet built

- Every other skill in the portfolio ([[08-roadmap]]) — Phase 2 onward, not started.
- Any composition/workflow layer across skills.
- Any UI.
- Multi-runtime validation (only exercised via this session's agent so far).

## Last updated

2026-08-22 — end of Phase 1.
