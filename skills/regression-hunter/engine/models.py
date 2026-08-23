"""Shared dataclass schema for the regression-hunter engine."""

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
class LineChange:
    kind: str  # "add" | "remove" | "context"
    content: str
    new_lineno: int | None = None
    old_lineno: int | None = None


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[LineChange] = field(default_factory=list)


@dataclass
class ChangedFile:
    old_path: str | None
    new_path: str | None
    is_new_file: bool = False
    is_deleted_file: bool = False
    hunks: list[Hunk] = field(default_factory=list)

    @property
    def effective_path(self) -> str | None:
        """The path used to resolve this file against a codebase-intelligence
        report — the new path if one exists (modified/added), else the old
        path (deleted file)."""
        return self.new_path if self.new_path is not None else self.old_path


@dataclass
class DiffContext:
    files: list[ChangedFile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class RegressionFlag:
    """A mechanically-detected diff-pattern lead — never a verdict. See
    engine/regression_patterns.py."""

    pattern_id: str
    category: str
    severity: str  # "low" | "medium" | "high"
    file: str
    line: int
    description: str
    matched_text: str


@dataclass
class CallerModule:
    path: str
    fan_in: int
    fan_out: int
    is_hotspot: bool


@dataclass
class StructuralAssessment:
    """Axis 2: blast radius grounded in the real codebase-intelligence
    dependency graph — reuses refactoring-safety's target_resolver.py/
    safety_scorer.py pattern (independent copy, ADR-013/ADR-014 lineage)."""

    resolved_module_path: str | None = None
    fan_in: int = 0
    fan_out: int = 0
    is_hotspot: bool = False
    caller_modules: list[CallerModule] = field(default_factory=list)
    structural_tier: str = "low"  # "high" | "medium" | "low"


@dataclass
class TestCoverageStatus:
    """Axis 3: does a real test-shaped module import this file — reuses
    refactoring-safety's test_coverage_scanner.py pattern (independent
    copy)."""

    __test__ = False  # not a pytest test class, despite the name prefix

    test_coverage_modules: list[str] = field(default_factory=list)

    @property
    def has_coverage(self) -> bool:
        return bool(self.test_coverage_modules)


@dataclass
class FileRiskAssessment:
    """One changed file's three explicitly separate, non-blended regression
    signals, plus the combined overall_risk_tier derived from the documented
    rule table in risk_scorer.py. See ADR-015."""

    file: str
    is_new_file: bool
    is_deleted_file: bool
    lines_added: int
    lines_removed: int
    diff_pattern_flags: list[RegressionFlag] = field(default_factory=list)
    structural: StructuralAssessment = field(default_factory=StructuralAssessment)
    test_coverage: TestCoverageStatus = field(default_factory=TestCoverageStatus)
    overall_risk_tier: str = "low"  # "high" | "medium" | "low"


@dataclass
class RegressionStats:
    files_changed: int
    files_added: int
    files_deleted: int
    lines_added: int
    lines_removed: int
    flag_count: int
    high_risk_file_count: int


@dataclass
class RegressionHunterReport:
    """The deterministic pre-decision packet handed to the agent's
    Regression Risk Checklist workflow (SKILL.md Step 3)."""

    stats: RegressionStats
    files: list[FileRiskAssessment]
    warnings: list[str] = field(default_factory=list)
