"""The hardcoded workflow template registry.

Deliberately NOT a generic arbitrary-skill chainer (ADR-020). Every
template here reuses a composition this project has already run for real
in an earlier phase's dogfood — a new template requires a code change and
a real dogfood run, not just a registry entry.
"""

from __future__ import annotations

from .models import WiringMode, WorkflowStep, WorkflowTemplate

REGISTRY: dict[str, WorkflowTemplate] = {
    "understand-then-plan": WorkflowTemplate(
        name="understand-then-plan",
        description=(
            "codebase-intelligence -> feature-planner, wired via "
            "feature-planner's --ci-report flag. Reuses Phase 4's real "
            "dogfood composition (examples/feature-planner/example-run.md)."
        ),
        steps=[
            WorkflowStep(
                skill_name="codebase-intelligence",
                output_filename="report.json",
                wiring_mode=WiringMode.CLI_FLAG,
            ),
            WorkflowStep(
                skill_name="feature-planner",
                output_filename="feature-planning-report.json",
                wiring_mode=WiringMode.CLI_FLAG,
                wiring_flag="--ci-report",
                upstream_context_marker="codebase-intelligence",
            ),
        ],
    ),
    "understand-then-test-plan": WorkflowTemplate(
        name="understand-then-test-plan",
        description=(
            "codebase-intelligence -> acceptance-test-engineer, wired via "
            "text-append (acceptance-test-engineer's CLI has no --ci-report "
            "flag). Reproduces Phase 3's real Pilot B composition "
            "(17-experiment-viability-check.md)."
        ),
        steps=[
            WorkflowStep(
                skill_name="codebase-intelligence",
                output_filename="report.json",
                wiring_mode=WiringMode.CLI_FLAG,
            ),
            WorkflowStep(
                skill_name="acceptance-test-engineer",
                output_filename="acceptance-testability-report.json",
                wiring_mode=WiringMode.TEXT_APPEND,
                upstream_context_marker="codebase-intelligence",
            ),
        ],
    ),
    "understand-then-optimize-context": WorkflowTemplate(
        name="understand-then-optimize-context",
        description=(
            "codebase-intelligence -> context-optimizer, wired via "
            "context-optimizer's --ci-report flag. Reuses Phase 13's real "
            "dogfood composition (examples/context-optimizer/example-run.md)."
        ),
        steps=[
            WorkflowStep(
                skill_name="codebase-intelligence",
                output_filename="report.json",
                wiring_mode=WiringMode.CLI_FLAG,
            ),
            WorkflowStep(
                skill_name="context-optimizer",
                output_filename="context-optimization-report.json",
                wiring_mode=WiringMode.CLI_FLAG,
                wiring_flag="--ci-report",
                upstream_context_marker="codebase-intelligence",
            ),
        ],
    ),
}


def list_templates() -> list[WorkflowTemplate]:
    return list(REGISTRY.values())


def get_template(name: str) -> WorkflowTemplate | None:
    return REGISTRY.get(name)
