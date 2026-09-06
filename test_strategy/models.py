"""Shared dataclass schema for the test-strategy engine (TEP Phase 5a).

This package computes no risk score of its own. It reuses regression-
hunter's existing FileRiskAssessment.overall_risk_tier and test-coverage
signal as the sole risk substrate, per
project-memory-bank/18-test-engineering-platform-contract.md's explicit
"extend, not replace ... do not build a second, competing risk scorer"
mandate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class TestTarget:
    """One changed file the engine believes needs a regression test — or
    an informational low-priority note for an already-low-risk gap."""

    __test__ = False  # not a pytest test class, despite the name prefix

    file: str
    priority: str  # "high" | "medium" | "low"
    reason: str
    risk_tier: str  # the exact regression-hunter overall_risk_tier this came from
    generation_feasible: bool
    feasibility_note: str
    recommended_framework: str | None = None


@dataclass
class TestStrategyStats:
    __test__ = False  # not a pytest test class, despite the name prefix

    files_considered: int
    files_already_covered: int
    targets_flagged: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int


@dataclass
class TestStrategyReport:
    __test__ = False  # not a pytest test class, despite the name prefix

    schema_version: str
    repo_root: str
    regression_report_path: str
    profile_path: str
    stats: TestStrategyStats
    targets: list[TestTarget] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "TestStrategyReport":
        known = set(TestStrategyReport.__dataclass_fields__)
        raw = {k: v for k, v in data.items() if k in known}
        raw["stats"] = TestStrategyStats(**raw["stats"])
        raw["targets"] = [TestTarget(**t) for t in raw.get("targets", [])]
        return TestStrategyReport(**raw)
