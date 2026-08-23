"""Shared dataclass schema for the refactoring-safety engine."""

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
class RefactorTarget:
    """One candidate identifier named in the refactor description, before
    resolution against the real codebase — a bare name, not yet known to be
    a module, function, or class."""

    name: str


@dataclass
class SafetyFlag:
    pattern_id: str
    category: str  # "vague-refactor" | "unstated-signal" | "untested-blast-radius"
    severity: str  # "low" | "medium" | "high"
    description: str
    matched_text: str


@dataclass
class RefactorStats:
    word_count: int
    target_count: int
    resolved_target_count: int
    flag_count: int
    high_severity_flag_count: int


@dataclass
class CallerModule:
    path: str
    fan_in: int
    fan_out: int
    is_hotspot: bool


@dataclass
class TargetAssessment:
    """One parsed target's resolution against the real codebase-intelligence
    report, plus the derived safety judgment for the proposed operation."""

    target_name: str
    resolved_module_path: str | None
    matched_functions: list[str] = field(default_factory=list)
    matched_classes: list[str] = field(default_factory=list)
    fan_in: int = 0
    fan_out: int = 0
    is_hotspot: bool = False
    caller_modules: list[CallerModule] = field(default_factory=list)
    test_coverage_modules: list[str] = field(default_factory=list)
    risk_tier: str = "low"  # "high" | "medium" | "low"


@dataclass
class RefactoringSafetyReport:
    """The deterministic pre-decision packet handed to the agent's
    Refactoring Safety Checklist workflow (SKILL.md Step 3)."""

    refactor_text: str
    operation_type: str
    stats: RefactorStats
    flags: list[SafetyFlag]
    targets: list[TargetAssessment]
    warnings: list[str] = field(default_factory=list)
