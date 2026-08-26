"""Shared dataclass schema for the engineering-knowledge-capture engine.

Composes on top of a required codebase-intelligence report.json (ADR-010,
reused an EIGHTH time — see ci_report_loader.py). This engine reuses CI's
already-parsed module list and dependency graph rather than re-deriving
structural context itself.
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
    independently of the codebase-intelligence package itself (no cross-
    package import), so this engine stays portable on its own."""

    root_path: str
    modules: list[CiModule] = field(default_factory=list)
    dependency_graph: CiDependencyGraph = field(default_factory=CiDependencyGraph)


@dataclass
class ResolvedLocation:
    """A knowledge candidate's evidence line resolved to a real module in
    the composed codebase-intelligence report. See location_resolver.py."""

    module_path: str
    fan_in: int = 0
    is_hotspot: bool = False


@dataclass
class KnowledgeCandidate:
    """One mechanically-flagged candidate for durable capture — NEVER a
    verdict that something IS worth capturing. Only the agent's Step 3
    Knowledge Capture Checklist walk (project-memory-bank/
    05-evaluation-framework.md) makes that call, and only that walk ever
    drafts the actual ADR/known-limitation/lessons-learned entry text."""

    pattern_id: str
    category: str  # "decision" | "lesson" | "limitation" | "workaround"
    matched_text: str
    description: str
    evidence: str
    resolved_module_path: str | None = None
    fan_in: int = 0
    is_hotspot: bool = False
    # "HIGH" | "MEDIUM" | "LOW" — see priority_scorer.py. LOW is a defined
    # band this version's scorer never actually assigns (fails upward, not
    # downward, under uncertainty) — disclosed, not a silent gap.
    suggested_capture_priority: str = "MEDIUM"


@dataclass
class ReportStats:
    candidate_count: int = 0
    candidate_count_by_category: dict[str, int] = field(default_factory=dict)
    candidate_count_by_priority: dict[str, int] = field(default_factory=dict)


@dataclass
class KnowledgeCaptureReport:
    """The deterministic pre-decision packet handed to the agent's
    Knowledge Capture Checklist workflow (SKILL.md Step 3)."""

    candidates: list[KnowledgeCandidate] = field(default_factory=list)
    stats: ReportStats = field(default_factory=ReportStats)
    warnings: list[str] = field(default_factory=list)
