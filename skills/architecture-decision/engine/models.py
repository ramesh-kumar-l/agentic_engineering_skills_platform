"""Shared dataclass schema for the architecture-decision engine."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CiModule:
    """Subset of codebase-intelligence's ModuleInfo this engine needs."""

    path: str
    docstring: str | None
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)


@dataclass
class CiDependencyGraph:
    """Subset of codebase-intelligence's DependencyGraph this engine needs."""

    fan_in: dict[str, int] = field(default_factory=dict)
    fan_out: dict[str, int] = field(default_factory=dict)
    hotspots: list[str] = field(default_factory=list)


@dataclass
class CiReportContext:
    """Lightweight local view of a codebase-intelligence report.json — loaded
    independently of the codebase-intelligence package itself (no cross-
    package import), so this engine stays portable on its own."""

    root_path: str
    modules: list[CiModule] = field(default_factory=list)
    dependency_graph: CiDependencyGraph = field(default_factory=CiDependencyGraph)


@dataclass
class DecisionOption:
    """One candidate option parsed out of the decision text. `label` is
    either an author-provided marker ("Option A", "1") or a synthesized
    fallback ("proposed") when the text names no explicit alternatives."""

    label: str
    raw_text: str


@dataclass
class DecisionFlag:
    pattern_id: str
    category: str  # "vague-decision" | "unstated-signal"
    severity: str  # "low" | "medium" | "high"
    description: str
    matched_text: str


@dataclass
class DecisionStats:
    word_count: int
    option_count: int
    flag_count: int
    high_severity_flag_count: int


@dataclass
class ImpactedModule:
    path: str
    relevance_score: int
    matched_keywords: list[str]
    fan_in: int
    fan_out: int
    is_hotspot: bool


@dataclass
class OptionImpact:
    """A single option's blast radius against the real dependency graph —
    not just which modules it mentions, but how structurally consequential
    touching them would be (ADR-013)."""

    option_label: str
    option_text: str
    impacted_modules: list[ImpactedModule]  # sorted desc by relevance_score
    blast_radius_score: int
    hotspot_count: int
    blast_radius_tier: str  # "high" | "medium" | "low"


@dataclass
class ArchitectureDecisionReport:
    """The deterministic pre-decision packet handed to the agent's
    Architecture Decision Record checklist workflow (SKILL.md Step 3)."""

    decision_text: str
    stats: DecisionStats
    flags: list[DecisionFlag]
    options: list[DecisionOption]
    option_impacts: list[OptionImpact]
    warnings: list[str] = field(default_factory=list)
