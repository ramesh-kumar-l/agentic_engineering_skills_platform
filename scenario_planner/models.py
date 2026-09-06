"""Shared dataclass schema for the scenario-planner engine (TEP Phase 5b).

This package computes no risk score. Every ScenarioCandidate is grounded
in exactly one of two existing signals: a regression-hunter diff-pattern
flag's own description, or a named function/class from codebase-
intelligence's structural module listing. When a target's file has no
structural listing at all, a single explicit file-level fallback
scenario is emitted instead of a fabricated function-level claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class ScenarioCandidate:
    """One proposed test scenario for a target file."""

    __test__ = False  # not a pytest test class, despite the name prefix

    scenario_name: str
    symbol_kind: str  # "function" | "class" | "file"
    rationale: str
    source: str  # "regression-flag" | "structural-listing" | "file-level-fallback"
    target_symbol: str | None = None


@dataclass
class TargetScenarioPlan:
    """All candidate scenarios proposed for one Test Strategy Engine target."""

    __test__ = False  # not a pytest test class, despite the name prefix

    file: str
    priority: str  # carried verbatim from the test-strategy target
    generation_feasible: bool
    recommended_framework: str | None
    structural_detail_available: bool
    scenarios: list[ScenarioCandidate] = field(default_factory=list)


@dataclass
class ScenarioPlanStats:
    __test__ = False  # not a pytest test class, despite the name prefix

    targets_considered: int
    targets_with_structural_detail: int
    targets_missing_structural_detail: int
    scenarios_generated: int


@dataclass
class ScenarioPlanReport:
    __test__ = False  # not a pytest test class, despite the name prefix

    schema_version: str
    repo_root: str
    test_strategy_report_path: str
    regression_report_path: str
    ci_report_path: str
    stats: ScenarioPlanStats
    plans: list[TargetScenarioPlan] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "ScenarioPlanReport":
        known = set(ScenarioPlanReport.__dataclass_fields__)
        raw = {k: v for k, v in data.items() if k in known}
        raw["stats"] = ScenarioPlanStats(**raw["stats"])
        plans: list[TargetScenarioPlan] = []
        for p in raw.get("plans", []):
            p = dict(p)
            p["scenarios"] = [ScenarioCandidate(**s) for s in p.get("scenarios", [])]
            plans.append(TargetScenarioPlan(**p))
        raw["plans"] = plans
        return ScenarioPlanReport(**raw)
