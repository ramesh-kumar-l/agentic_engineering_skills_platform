"""Shared dataclass schema for the root-cause-analyzer engine."""

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
class StackFrame:
    """A single frame extracted from a stack trace / traceback embedded in
    the symptom text. `path` is exactly as written in the trace — matching
    it against a real ci_report module path is the candidate scorer's job,
    not this parser's."""

    path: str
    line: int | None
    symbol: str | None
    raw_text: str


@dataclass
class SymptomFlag:
    pattern_id: str
    category: str  # "vague-symptom" | "unstated-signal"
    severity: str  # "low" | "medium" | "high"
    description: str
    matched_text: str


@dataclass
class SymptomStats:
    word_count: int
    vague_symptom_count: int
    stack_frame_count: int


@dataclass
class CandidateLocation:
    path: str
    score: int
    evidence_tier: str  # "stack-trace" | "keyword"
    matched_keywords: list[str]
    stack_trace_hit: bool
    fan_in: int
    fan_out: int
    is_hotspot: bool


@dataclass
class CandidateReport:
    keywords: list[str]
    stack_frames: list[StackFrame] = field(default_factory=list)
    candidates: list[CandidateLocation] = field(default_factory=list)  # sorted desc by score


@dataclass
class RootCauseReport:
    """The deterministic pre-investigation packet handed to the agent's
    Root Cause Investigation Checklist workflow (SKILL.md Step 3)."""

    symptom_text: str
    stats: SymptomStats
    symptom_flags: list[SymptomFlag]
    candidates: CandidateReport
    warnings: list[str] = field(default_factory=list)
