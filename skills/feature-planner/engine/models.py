"""Shared dataclass schema for the feature-planner engine."""

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
class RelevanceScore:
    path: str
    score: int
    matched_keywords: list[str]
    fan_in: int
    fan_out: int
    is_hotspot: bool


@dataclass
class RelevanceReport:
    keywords: list[str]
    scores: list[RelevanceScore] = field(default_factory=list)  # sorted desc by score


@dataclass
class PlanningFlag:
    pattern_id: str
    category: str  # "vague-scope" | "weak-goal-modal" | "unstated-signal"
    severity: str  # "low" | "medium" | "high"
    description: str
    matched_text: str


@dataclass
class TaskStats:
    word_count: int
    vague_scope_count: int
    weak_modal_count: int


@dataclass
class FeaturePlanningReport:
    """The deterministic pre-planning packet handed to the agent's
    structured-plan-derivation workflow (SKILL.md Step 3)."""

    task_text: str
    stats: TaskStats
    planning_flags: list[PlanningFlag]
    relevance: RelevanceReport
    warnings: list[str] = field(default_factory=list)
