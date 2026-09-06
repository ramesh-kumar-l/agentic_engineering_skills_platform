"""Combines a test_strategy target list with regression-hunter's flag
descriptions and codebase-intelligence's structural listing to propose
candidate test scenarios (TEP Phase 5b).

Computes no risk score. Every scenario cites a concrete existing signal:
a regression-hunter flag's own description, or a named function/class
from codebase-intelligence's module listing. codebase-intelligence's
ModuleInfo carries no line-range data, so this engine cannot and does not
claim to know *which* function a diff actually touched — every function
and class in a flagged file's module listing is offered as an equally
plausible candidate rather than guessing one. A file absent from the
modules list gets one explicit file-level fallback scenario instead of a
fabricated function-level claim.
"""

from __future__ import annotations

from .ci_module_loader import ModuleSummary
from .models import (
    SCHEMA_VERSION,
    ScenarioCandidate,
    ScenarioPlanReport,
    ScenarioPlanStats,
    TargetScenarioPlan,
)
from .regression_flags_loader import FlagSummary
from .strategy_targets_loader import StrategyReportContext


def _flag_scenarios(flags: list[FlagSummary]) -> list[ScenarioCandidate]:
    return [
        ScenarioCandidate(
            scenario_name=f"verify the behavior flagged by `{f.pattern_id}`",
            symbol_kind="file",
            rationale=f.description,
            source="regression-flag",
        )
        for f in flags
    ]


def _structural_scenarios(module: ModuleSummary) -> list[ScenarioCandidate]:
    scenarios: list[ScenarioCandidate] = []
    total = len(module.functions) + len(module.classes)
    for fn in module.functions:
        scenarios.append(
            ScenarioCandidate(
                scenario_name=f"exercise function `{fn}`",
                symbol_kind="function",
                target_symbol=fn,
                rationale=(
                    f"`{fn}` is one of this file's {total} functions/classes "
                    "per codebase-intelligence's structural listing; no "
                    "line-range data exists to attribute the diff to one "
                    "specific symbol, so every symbol is listed as an "
                    "equally plausible candidate rather than a guess"
                ),
                source="structural-listing",
            )
        )
    for cls in module.classes:
        scenarios.append(
            ScenarioCandidate(
                scenario_name=f"exercise class `{cls}`",
                symbol_kind="class",
                target_symbol=cls,
                rationale=(
                    f"`{cls}` is one of this file's {total} functions/classes "
                    "per codebase-intelligence's structural listing; no "
                    "line-range data exists to attribute the diff to one "
                    "specific symbol, so every symbol is listed as an "
                    "equally plausible candidate rather than a guess"
                ),
                source="structural-listing",
            )
        )
    return scenarios


def _fallback_scenario() -> ScenarioCandidate:
    return ScenarioCandidate(
        scenario_name="smoke-test this file's observable behavior",
        symbol_kind="file",
        rationale=(
            "this file was not found in codebase-intelligence's modules "
            "listing (e.g. a non-source file, or the report predates this "
            "file) — no function/class-level detail is available, so only "
            "a generic file-level placeholder is offered"
        ),
        source="file-level-fallback",
    )


def build_scenario_plan(
    strategy_ctx: StrategyReportContext,
    flags_by_file: dict[str, list[FlagSummary]],
    modules_by_path: dict[str, ModuleSummary],
    strategy_report_path: str,
    regression_report_path: str,
    ci_report_path: str,
) -> ScenarioPlanReport:
    plans: list[TargetScenarioPlan] = []
    with_detail = 0

    for target in strategy_ctx.targets:
        flags = flags_by_file.get(target.file, [])
        module = modules_by_path.get(target.file)

        scenarios = _flag_scenarios(flags)
        if module is not None:
            scenarios.extend(_structural_scenarios(module))
            with_detail += 1
        elif not scenarios:
            scenarios.append(_fallback_scenario())

        plans.append(
            TargetScenarioPlan(
                file=target.file,
                priority=target.priority,
                generation_feasible=target.generation_feasible,
                recommended_framework=target.recommended_framework,
                structural_detail_available=module is not None,
                scenarios=scenarios,
            )
        )

    warnings: list[str] = []
    if not strategy_ctx.targets:
        warnings.append(
            "test-strategy report contained zero flagged targets — "
            "nothing to plan scenarios for"
        )

    stats = ScenarioPlanStats(
        targets_considered=len(plans),
        targets_with_structural_detail=with_detail,
        targets_missing_structural_detail=len(plans) - with_detail,
        scenarios_generated=sum(len(p.scenarios) for p in plans),
    )

    return ScenarioPlanReport(
        schema_version=SCHEMA_VERSION,
        repo_root=strategy_ctx.repo_root,
        test_strategy_report_path=strategy_report_path,
        regression_report_path=regression_report_path,
        ci_report_path=ci_report_path,
        stats=stats,
        plans=plans,
        warnings=warnings,
    )
