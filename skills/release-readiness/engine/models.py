"""Shared dataclass schema for the release-readiness engine.

Composes three input surfaces: the diff itself, a required
codebase-intelligence report (ADR-010, reused a sixth time — see
ci_report_loader.py), and two OPTIONAL evidence reports produced by other
skills in this portfolio (regression-hunter, security-context-guard — ADR-011
precedent, optional composition). Missing optional reports are simply absent
evidence, never a failure condition.
"""

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
    independently of the codebase-intelligence package itself (no
    cross-package import), so this engine stays portable on its own."""

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
class HygieneFlag:
    """A mechanically-detected, release-blocking diff-hygiene lead — never a
    verdict, same "leads not verdicts" discipline as every prior Pattern 2
    anti-pattern table (ADR-007). See engine/hygiene_patterns.py."""

    pattern_id: str
    category: str  # "debug-leftover" | "merge-conflict-marker" | "hardcoded-secret" | "todo-blocking"
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
    dependency graph — reuses refactoring-safety's/regression-hunter's
    target_resolver.py pattern as an independent copy (same substring-based
    caller-identification limitation, see L23/known-limitations note in
    SKILL.md)."""

    resolved_module_path: str | None = None
    fan_in: int = 0
    fan_out: int = 0
    is_hotspot: bool = False
    caller_modules: list[CallerModule] = field(default_factory=list)
    structural_tier: str = "low"  # "high" | "medium" | "low"


@dataclass
class TestCoverageStatus:
    """Axis 3: does a real test-shaped module import this file — reuses
    refactoring-safety's/regression-hunter's test_coverage_scanner.py pattern
    as an independent copy."""

    __test__ = False  # not a pytest test class, despite the name prefix

    test_coverage_modules: list[str] = field(default_factory=list)

    @property
    def has_coverage(self) -> bool:
        return bool(self.test_coverage_modules)


@dataclass
class RegressionEvidence:
    """Axis 4 (OPTIONAL): surfaced verbatim from a regression-hunter
    report.json for this same file, if --regression-report was supplied —
    never re-derived here. Absent when the flag is omitted or the file isn't
    present in that report, not a failure (ADR-011 precedent)."""

    available: bool = False
    overall_risk_tier: str | None = None
    diff_pattern_flag_count: int = 0
    source_path: str | None = None


@dataclass
class SecurityEvidence:
    """Axis 5 (OPTIONAL, report-level — security-context-guard classifies
    content/actions, not per-diff-file): surfaced verbatim from a
    security-context-guard report.json, if --security-report was supplied —
    never re-derived here. Absent when the flag is omitted, not a failure."""

    available: bool = False
    sensitivity: str | None = None
    suggested_verdict: str | None = None
    source_path: str | None = None


@dataclass
class FileReadinessAssessment:
    """One changed file's always-available axes (1-3) plus the derived
    per-file readiness_tier from the documented rule table in
    readiness_scorer.py (ADR-016). regression_evidence (Axis 4) is surfaced
    alongside but does not feed the rule table — see readiness_scorer.py's
    module docstring for why."""

    file: str
    is_new_file: bool
    is_deleted_file: bool
    lines_added: int
    lines_removed: int
    hygiene_flags: list[HygieneFlag] = field(default_factory=list)
    structural: StructuralAssessment = field(default_factory=StructuralAssessment)
    test_coverage: TestCoverageStatus = field(default_factory=TestCoverageStatus)
    regression_evidence: RegressionEvidence = field(default_factory=RegressionEvidence)
    readiness_tier: str = "clear"  # "blocked" | "needs-review" | "clear"


@dataclass
class ReadinessStats:
    files_changed: int
    files_added: int
    files_deleted: int
    lines_added: int
    lines_removed: int
    hygiene_flag_count: int
    blocked_file_count: int
    needs_review_file_count: int


@dataclass
class ReleaseReadinessReport:
    """The deterministic pre-decision packet handed to the agent's Release
    Readiness Checklist workflow (SKILL.md Step 3). `overall_verdict` is
    ALWAYS a recommendation for a human to review — the engine never
    authorizes a release itself (ADR-011 precedent, ADR-016)."""

    stats: ReadinessStats
    files: list[FileReadinessAssessment]
    overall_verdict: str  # "NOT_READY" | "READY_WITH_CONDITIONS" | "READY"
    regression_report_composed: bool = False
    security_report_composed: bool = False
    security_evidence: SecurityEvidence = field(default_factory=SecurityEvidence)
    warnings: list[str] = field(default_factory=list)
