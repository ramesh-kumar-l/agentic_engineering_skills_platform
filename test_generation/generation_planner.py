"""Composes one TargetGenerationSpec per scenario_planner candidate scenario
(TEP Phase 5c). Every field the deterministic engine can supply -- naming
convention, source excerpt, the scenario's own rationale -- is carried
through untouched; the engine requests, but never authors, 1 positive +
5 negative test slots per scenario, and explicitly tells the authoring
agent not to pad with fabricated cases a real source excerpt can't support.
"""

from __future__ import annotations

from .models import (
    SCHEMA_VERSION,
    GenerationPlanReport,
    GenerationPlanStats,
    GenerationSlot,
    NamingConvention,
    TargetGenerationSpec,
)
from .scenario_loader import ScenarioPlanContext
from .source_excerpt_reader import read_source_excerpt

NEGATIVE_SLOT_COUNT = 5  # fixed count of negative/edge-case slots requested per scenario

_POSITIVE_INSTRUCTION = (
    "Author one positive/happy-path test exercising this scenario as "
    "described in scenario_rationale, following the naming convention above."
)

_NEGATIVE_INSTRUCTION_TEMPLATE = (
    "Author negative/edge-case test {index} of a requested 5, grounded in "
    "the real source excerpt above (an invalid input, boundary condition, or "
    "error path this symbol's real code plausibly supports). If the real "
    "source excerpt cannot support this many genuinely distinct negative "
    "conditions, author fewer and say so in a comment rather than duplicate "
    "a case."
)


def _negative_slots() -> list[GenerationSlot]:
    return [
        GenerationSlot(
            kind="negative",
            slot_index=i,
            instruction=_NEGATIVE_INSTRUCTION_TEMPLATE.format(index=i),
        )
        for i in range(1, NEGATIVE_SLOT_COUNT + 1)
    ]


def build_generation_plan(
    scenario_ctx: ScenarioPlanContext,
    naming_convention: NamingConvention,
    repo_root: str,
    scenario_plan_report_path: str,
) -> GenerationPlanReport:
    specs: list[TargetGenerationSpec] = []
    with_excerpt = 0

    for candidate in scenario_ctx.candidates:
        excerpt = read_source_excerpt(repo_root, candidate.file, candidate.target_symbol)
        if excerpt is not None:
            with_excerpt += 1

        specs.append(
            TargetGenerationSpec(
                file=candidate.file,
                target_symbol=candidate.target_symbol,
                symbol_kind=candidate.symbol_kind,
                scenario_name=candidate.scenario_name,
                scenario_rationale=candidate.rationale,
                scenario_source=candidate.source,
                recommended_framework=candidate.recommended_framework,
                naming_convention=naming_convention,
                source_excerpt=excerpt,
                source_excerpt_available=excerpt is not None,
                positive_slot=GenerationSlot(
                    kind="positive", slot_index=0, instruction=_POSITIVE_INSTRUCTION
                ),
                negative_slots=_negative_slots(),
            )
        )

    warnings: list[str] = []
    if not scenario_ctx.candidates:
        warnings.append(
            "scenario-plan report contained zero candidate scenarios — "
            "nothing to plan test generation for"
        )

    stats = GenerationPlanStats(
        scenarios_considered=len(specs),
        specs_produced=len(specs),
        specs_with_source_excerpt=with_excerpt,
        negative_slots_requested=len(specs) * NEGATIVE_SLOT_COUNT,
    )

    return GenerationPlanReport(
        schema_version=SCHEMA_VERSION,
        repo_root=repo_root,
        scenario_plan_report_path=scenario_plan_report_path,
        naming_convention=naming_convention,
        stats=stats,
        specs=specs,
        warnings=warnings,
    )
