"""Shared dataclass schema for the test-generation engine (TEP Phase 5c).

This package never authors test code itself. codebase-intelligence's
structural listing carries no parameter/type/exception data, so deciding
what a plausible negative case even is requires reading real source and
reasoning about it -- the AI-judgment half of this project's standing
deterministic-engine-plus-agent-judgment split (ADR-005/007). This engine
produces a plan naming exactly what to author (file, symbol, naming
convention, source excerpt, slot count); the calling agent authors the
actual file content from that plan.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class NamingConvention:
    __test__ = False  # not a pytest test class, despite the name prefix

    pattern: str  # e.g. "test_*.py", "*Test.java"
    example: str
    source: str  # "inferred" | "override" | "platform-default"


@dataclass
class GenerationSlot:
    __test__ = False  # not a pytest test class, despite the name prefix

    kind: str  # "positive" | "negative"
    slot_index: int
    instruction: str


@dataclass
class TargetGenerationSpec:
    __test__ = False  # not a pytest test class, despite the name prefix

    file: str
    target_symbol: str | None
    symbol_kind: str  # "function" | "class" | "file"
    scenario_name: str
    scenario_rationale: str
    scenario_source: str  # carried verbatim from the scenario_planner candidate's `source`
    recommended_framework: str | None
    naming_convention: NamingConvention
    source_excerpt: str | None
    source_excerpt_available: bool
    positive_slot: GenerationSlot
    negative_slots: list[GenerationSlot] = field(default_factory=list)


@dataclass
class GenerationPlanStats:
    __test__ = False  # not a pytest test class, despite the name prefix

    scenarios_considered: int
    specs_produced: int
    specs_with_source_excerpt: int
    negative_slots_requested: int


@dataclass
class GenerationPlanReport:
    __test__ = False  # not a pytest test class, despite the name prefix

    schema_version: str
    repo_root: str
    scenario_plan_report_path: str
    naming_convention: NamingConvention
    stats: GenerationPlanStats
    specs: list[TargetGenerationSpec] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "GenerationPlanReport":
        known = set(GenerationPlanReport.__dataclass_fields__)
        raw = {k: v for k, v in data.items() if k in known}
        raw["stats"] = GenerationPlanStats(**raw["stats"])
        raw["naming_convention"] = NamingConvention(**raw["naming_convention"])
        specs: list[TargetGenerationSpec] = []
        for s in raw.get("specs", []):
            s = dict(s)
            s["naming_convention"] = NamingConvention(**s["naming_convention"])
            s["positive_slot"] = GenerationSlot(**s["positive_slot"])
            s["negative_slots"] = [GenerationSlot(**n) for n in s.get("negative_slots", [])]
            specs.append(TargetGenerationSpec(**s))
        raw["specs"] = specs
        return GenerationPlanReport(**raw)
