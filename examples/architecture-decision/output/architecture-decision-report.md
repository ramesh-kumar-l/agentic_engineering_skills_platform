# Architecture Decision Pre-Decision Report

## Decision Text
Option A: architecture-decision requires a codebase-intelligence report.json as a hard precondition -- the CLI refuses to run without one, reusing feature-planner's and root-cause-analyzer's ADR-010 required-composition pattern a third time.

Option B: architecture-decision treats a codebase-intelligence report as optional composed context, like security-context-guard does -- the engine still runs and produces decision flags without one, just without blast-radius grounding, reusing ADR-011's optional-composition stance instead.

Option A trades flexibility (you cannot run this skill on an ungrounded decision at all) for correctness -- an architecture decision's blast-radius claim without real fan-in/fan-out data would be a guess dressed up as evidence, which is actively worse than no blast-radius claim at all. This mirrors feature-planner's reasoning exactly: "ungrounded output is actively harmful." Option B trades correctness for reach -- a decision about pure business logic or a brand-new module with no dependency graph yet could still get anti-pattern flagging (vague language, missing alternatives, missing tradeoffs) even without a report, which is real value security-context-guard already proved out. This choice is fully reversible either way -- the ci_report_loader.py module is a small, isolated wrapper, and switching from required to optional later is a one-file change with no data migration. No new credentials, secrets, or authentication surface is introduced by either option.

## Stats
- Words: 233
- Options parsed: 2
- Flags: 1 (high severity: 0)

## Decision Flags (mechanically-detected leads, not verdicts)
- [medium] `vague-decision-language` — Confidence language with no supporting evidence — state the actual reasoning or data behind the claim instead of asserting it's easy/obvious.

## Option Impact (codebase-intelligence-grounded blast radius, not just keyword mentions)
### Option A (blast radius: high, score 241, hotspots touched: 10)
> architecture-decision requires a codebase-intelligence report.json as a hard precondition -- the CLI refuses to run without one, reusing feature-planner's and root-cause-analyzer's ADR-010 required-composition pattern a third time.
- `evaluations/architecture-decision/run_evaluation.py` (relevance 33, fan_in=0, fan_out=0) — matched: architecture, decision, codebase, intelligence, report, json, precondition, run, reusing, feature, planner, root, cause, analyzer, adr, required, composition, pattern, third, time
- `evaluations/root-cause-analyzer/run_evaluation.py` (relevance 32, fan_in=0, fan_out=0) — matched: decision, codebase, intelligence, report, json, precondition, run, reusing, feature, planner, root, cause, analyzer, adr, required, composition, pattern, time
- `skills/architecture-decision/engine/cli.py` (relevance 27, fan_in=0, fan_out=4) — matched: architecture, decision, codebase, intelligence, report, json, hard, precondition, cli, reusing, adr, required, composition, pattern, third, time
- `skills/root-cause-analyzer/engine/ci_report_loader.py` (relevance 26, fan_in=2, fan_out=1) — matched: decision, codebase, intelligence, report, json, hard, without, root, cause, analyzer, adr, required, composition, pattern, time
- `skills/root-cause-analyzer/engine/cli.py` (relevance 26, fan_in=0, fan_out=4) — matched: decision, codebase, intelligence, report, json, hard, precondition, cli, reusing, root, cause, analyzer, adr, required, composition, pattern, time
- `evaluations/feature-planner/run_evaluation.py` (relevance 25, fan_in=0, fan_out=0) — matched: codebase, intelligence, report, json, precondition, run, feature, planner, adr, required, composition, pattern, third, time
- `skills/architecture-decision/engine/ci_report_loader.py` (relevance 23, fan_in=2, fan_out=1) — matched: architecture, decision, codebase, intelligence, report, json, hard, adr, required, composition, pattern, third, time
- `skills/root-cause-analyzer/engine/symptom_patterns.py` (relevance 23, fan_in=1, fan_out=0) — matched: decision, report, feature, planner, root, cause, analyzer, adr, pattern, time
- `skills/root-cause-analyzer/tests/test_cli.py` (relevance 23, fan_in=0, fan_out=0) — matched: requires, report, json, cli, run, root, cause, analyzer
- `skills/architecture-decision/engine/decision_patterns.py` (relevance 22, fan_in=1, fan_out=0) — matched: architecture, decision, without, root, cause, analyzer, adr, pattern, time
- ... and 122 more (see JSON output for full list)

### Option B (blast radius: high, score 256, hotspots touched: 10)
> architecture-decision treats a codebase-intelligence report as optional composed context, like security-context-guard does -- the engine still runs and produces decision flags without one, just without blast-radius grounding, reusing ADR-011's optional-composition stance instead.
- `skills/security-context-guard/engine/report.py` (relevance 27, fan_in=1, fan_out=4) — matched: codebase, intelligence, report, optional, context, like, security, guard, engine, one, adr, composition
- `evaluations/architecture-decision/run_evaluation.py` (relevance 25, fan_in=0, fan_out=0) — matched: architecture, decision, codebase, intelligence, report, context, security, guard, engine, flags, blast, radius, reusing, adr, composition
- `skills/architecture-decision/engine/ci_report_loader.py` (relevance 25, fan_in=2, fan_out=1) — matched: architecture, decision, codebase, intelligence, report, context, engine, blast, radius, grounding, adr, composition
- `skills/security-context-guard/engine/models.py` (relevance 25, fan_in=6, fan_out=0) — matched: decision, report, context, security, guard, engine, adr
- `skills/architecture-decision/engine/impact_scorer.py` (relevance 23, fan_in=1, fan_out=1) — matched: architecture, decision, codebase, intelligence, does, engine, still, without, one, blast, radius, adr
- `skills/architecture-decision/tests/test_report.py` (relevance 23, fan_in=0, fan_out=0) — matched: architecture, decision, report, engine, produces, flags, blast, radius
- `skills/architecture-decision/engine/cli.py` (relevance 22, fan_in=0, fan_out=4) — matched: architecture, decision, codebase, intelligence, report, optional, context, engine, reusing, adr, composition
- `skills/codebase-intelligence/engine/models.py` (relevance 22, fan_in=8, fan_out=0 [hotspot]) — matched: codebase, intelligence, report, engine, produces, without, one
- `skills/security-context-guard/tests/test_report.py` (relevance 22, fan_in=0, fan_out=0) — matched: report, context, security, guard, does, engine, produces, flags
- `evaluations/security-context-guard/run_evaluation.py` (relevance 20, fan_in=0, fan_out=0) — matched: decision, report, optional, context, like, security, guard, engine, one, adr, composition
- ... and 133 more (see JSON output for full list)

## Warnings
- At least one option's blast radius is HIGH (touches a hotspot or high fan-in module) — this decision likely warrants wider review before proceeding.
