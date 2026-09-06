"""Lightweight, independent loader for a scenario_planner scenario-plan-
report.json -- flattens each TargetScenarioPlan's candidate scenarios into
one ScenarioCandidateSummary per scenario, carrying the parent target's
file/recommended_framework alongside. Independent copy convention, no
cross-package import (ADR-010 lineage): defines its own trimmed view rather
than importing scenario_planner's package internals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class ScenarioPlanError(Exception):
    """Raised when a path does not contain a valid scenario-plan-report.json."""


@dataclass
class ScenarioCandidateSummary:
    file: str
    target_symbol: str | None
    symbol_kind: str
    scenario_name: str
    rationale: str
    source: str
    recommended_framework: str | None


@dataclass
class ScenarioPlanContext:
    repo_root: str
    candidates: list[ScenarioCandidateSummary] = field(default_factory=list)


def load_scenario_plan(path: str | Path) -> ScenarioPlanContext:
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScenarioPlanError(
            f"cannot read scenario-plan report at {p}: {exc}"
        ) from exc

    try:
        repo_root = raw["repo_root"]
        plans_raw = raw["plans"]
    except KeyError as exc:
        raise ScenarioPlanError(
            f"{p} is missing required field {exc} — not a "
            "scenario-plan-report.json"
        ) from exc

    candidates: list[ScenarioCandidateSummary] = []
    for plan in plans_raw:
        try:
            file = plan["file"]
            recommended_framework = plan.get("recommended_framework")
            scenarios_raw = plan["scenarios"]
        except KeyError as exc:
            raise ScenarioPlanError(
                f"{p} has a plan entry missing required field {exc} — "
                "not a scenario-plan-report.json"
            ) from exc

        for s in scenarios_raw:
            try:
                candidates.append(
                    ScenarioCandidateSummary(
                        file=file,
                        target_symbol=s.get("target_symbol"),
                        symbol_kind=s["symbol_kind"],
                        scenario_name=s["scenario_name"],
                        rationale=s["rationale"],
                        source=s["source"],
                        recommended_framework=recommended_framework,
                    )
                )
            except KeyError as exc:
                raise ScenarioPlanError(
                    f"{p} has a scenario entry missing required field {exc} — "
                    "not a scenario-plan-report.json"
                ) from exc

    return ScenarioPlanContext(repo_root=repo_root, candidates=candidates)
