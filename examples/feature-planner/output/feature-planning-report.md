# Feature Planning Report

## Task
Only add a --verbose flag to acceptance-test-engineer's CLI that prints per-sentence testability flag detail. Verify via a new test that the flag prints one line per sentence with its matched flags.

## Stats
- Words: 35
- Vague scope markers: 0
- Weak goal modals: 0

## Planning Flags (mechanically-detected leads, not verdicts)
- None detected by pattern matching.

## Relevant Files (codebase-intelligence-grounded, ranked by keyword overlap)
- Extracted keywords: only, verbose, flag, acceptance, test, engineer, cli, prints, per, sentence, testability, detail, verify, via, new, one, line, its, matched, flags
- `evaluations/acceptance-test-engineer/run_evaluation.py` (score 25, fan_in=0, fan_out=0) — matched: only, flag, acceptance, test, engineer, per, testability, via, flags
- `skills/acceptance-test-engineer/tests/test_testability_scanner.py` (score 24, fan_in=0, fan_out=0) — matched: flag, acceptance, test, engineer, per, sentence, testability, flags
- `skills/acceptance-test-engineer/engine/models.py` (score 22, fan_in=6, fan_out=0 [hotspot]) — matched: flag, acceptance, test, engineer, sentence, testability
- `skills/acceptance-test-engineer/engine/patterns.py` (score 19, fan_in=1, fan_out=0) — matched: only, flag, acceptance, test, engineer, testability, its
- `skills/acceptance-test-engineer/tests/test_requirement_parser.py` (score 19, fan_in=0, fan_out=0) — matched: acceptance, test, engineer, sentence, one, line, its
- `skills/adversarial-diff-reviewer/tests/test_cli.py` (score 19, fan_in=0, fan_out=0) — matched: only, acceptance, test, engineer, cli, one, its
- `skills/acceptance-test-engineer/engine/requirement_parser.py` (score 17, fan_in=1, fan_out=1) — matched: only, acceptance, test, engineer, sentence, testability, via, new, line, its
- `skills/acceptance-test-engineer/tests/test_report.py` (score 17, fan_in=0, fan_out=0) — matched: flag, acceptance, test, engineer, sentence, flags
- `skills/acceptance-test-engineer/tests/test_integration.py` (score 15, fan_in=0, fan_out=0) — matched: acceptance, test, engineer, line
- `skills/acceptance-test-engineer/tests/test_stats.py` (score 15, fan_in=0, fan_out=0) — matched: acceptance, test, engineer, sentence, testability
- `skills/adversarial-diff-reviewer/tests/test_risk_scanner.py` (score 15, fan_in=0, fan_out=0) — matched: only, flag, test, one, line, flags
- `skills/acceptance-test-engineer/engine/testability_scanner.py` (score 14, fan_in=1, fan_out=2 [hotspot]) — matched: acceptance, test, engineer, testability
- `skills/acceptance-test-engineer/engine/cli.py` (score 13, fan_in=0, fan_out=3) — matched: acceptance, test, engineer, cli
- `skills/acceptance-test-engineer/engine/render_json.py` (score 13, fan_in=1, fan_out=1) — matched: acceptance, test, engineer, testability, detail
- `evaluations/feature-planner/run_evaluation.py` (score 12, fan_in=0, fan_out=0) — matched: only, flag, acceptance, test, engineer, per, via, flags
- ... and 50 more (see JSON output for full list)
