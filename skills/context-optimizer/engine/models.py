"""Shared dataclass schema for the context-optimizer engine.

Composes on top of a required codebase-intelligence report.json (ADR-010,
reused a NINTH time — see ci_report_loader.py). This engine reuses CI's
already-parsed file list, module metadata, and dependency graph rather
than re-scanning the target repo itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CiFile:
    """One file worth scoring for relevance: real line_count from CI's
    FileInfo, enriched with structural metadata from CI's ModuleInfo when
    that file was parseable (docstring/functions/classes/imports default
    empty for a file CI could not parse — see ci_report_loader.py)."""

    path: str
    line_count: int = 0
    docstring: str | None = None
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
    """Lightweight local view of a codebase-intelligence report.json —
    loaded independently of the codebase-intelligence package itself (no
    cross-package import), so this engine stays portable on its own."""

    root_path: str
    files: list[CiFile] = field(default_factory=list)
    dependency_graph: CiDependencyGraph = field(default_factory=CiDependencyGraph)


@dataclass
class FileRelevance:
    """One recommended file — NEVER a claim that the file WILL be
    sufficient for the task, only a deterministic relevance signal. Only
    the agent's Step 3 Context Optimization Checklist walk (project-
    memory-bank/05-evaluation-framework.md) decides whether the
    recommended set is actually complete and non-noisy."""

    path: str
    relevance_score: int
    matched_keywords: list[str] = field(default_factory=list)
    fan_in: int = 0
    is_hotspot: bool = False
    line_count: int = 0
    estimated_tokens: int = 0
    # "CORE" | "SUPPORTING" | "EXCLUDED" — see budget_selector.py.
    # EXCLUDED means "relevant but budget-constrained out", never
    # "irrelevant" — an irrelevant file (score <= 0) never becomes a
    # FileRelevance entry at all (see report.py).
    tier: str = "SUPPORTING"
    # True when this file's own line_count alone exceeds a supplied
    # budget. Such a file is NEVER silently excluded (ADR-019's fail-OPEN
    # rule) — it keeps its relevance tier and is flagged instead.
    oversized_alone: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class ReportStats:
    candidate_count: int = 0
    candidate_count_by_tier: dict[str, int] = field(default_factory=dict)
    # Sum of estimated_tokens across CORE + SUPPORTING candidates only
    # (EXCLUDED candidates are not meant to be loaded, so they are not
    # counted toward the total a caller would actually spend).
    total_estimated_tokens: int = 0
    oversized_alone_count: int = 0


@dataclass
class ContextOptimizationReport:
    """The deterministic pre-decision packet handed to the agent's
    Context Optimization Checklist workflow (SKILL.md Step 3)."""

    task_keywords: list[str] = field(default_factory=list)
    recommendations: list[FileRelevance] = field(default_factory=list)
    stats: ReportStats = field(default_factory=ReportStats)
    warnings: list[str] = field(default_factory=list)
