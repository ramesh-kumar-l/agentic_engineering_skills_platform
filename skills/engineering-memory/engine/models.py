"""Shared dataclass schema for the engineering-memory engine.

Composes on top of a required codebase-intelligence report.json (ADR-010,
reused an ELEVENTH time — see ci_report_loader.py). Unlike every prior
composing skill, this engine's primary retrieval corpus is this project's
OWN project-memory-bank/ markdown (11-decisions.md,
12-known-limitations.md), not a target repo's external artifacts — a new
"self-referential composition" category, see project-memory-bank/
11-decisions.md ADR-021.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RecordStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FIXED = "FIXED"
    SUPERSEDED = "SUPERSEDED"


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
class MemoryRecord:
    """One parsed entry from this project's own memory bank — an ADR
    (11-decisions.md) or a known limitation (12-known-limitations.md).
    `## L8 update:` style sub-entries are never parsed into their own
    MemoryRecord — see memory_bank_parser.py."""

    record_id: str  # e.g. "ADR-010", "L23"
    record_type: str  # "decision" | "limitation"
    title: str
    body: str
    source_file: str
    source_line: int
    status: RecordStatus = RecordStatus.ACTIVE
    mentioned_modules: list[str] = field(default_factory=list)


@dataclass
class ModuleFlag:
    """Whether one of a record's mentioned module references still
    resolves to a real module in the current codebase-intelligence
    report — see module_resolver.py."""

    module_path: str
    exists: bool
    is_hotspot: bool = False
    fan_in: int = 0


@dataclass
class StalenessFlag:
    """Always attached to a match, never omitted — see
    staleness_classifier.py and A8's own named risk in
    project-memory-bank/16-assumptions-and-validation.md."""

    is_stale: bool
    reason: str | None = None


@dataclass
class RelevanceMatch:
    record: MemoryRecord
    score: int
    matched_keywords: list[str] = field(default_factory=list)
    matched_modules: list[str] = field(default_factory=list)
    module_flags: list[ModuleFlag] = field(default_factory=list)
    staleness: StalenessFlag = field(default_factory=lambda: StalenessFlag(is_stale=False))


@dataclass
class ReportStats:
    records_scanned: int = 0
    records_scanned_by_type: dict[str, int] = field(default_factory=dict)
    match_count: int = 0
    match_count_by_status: dict[str, int] = field(default_factory=dict)


@dataclass
class MemoryQueryReport:
    """The deterministic pre-decision packet handed to the agent's
    Engineering Memory Retrieval Checklist workflow (SKILL.md)."""

    task_description: str
    matches: list[RelevanceMatch] = field(default_factory=list)
    stats: ReportStats = field(default_factory=ReportStats)
    warnings: list[str] = field(default_factory=list)
