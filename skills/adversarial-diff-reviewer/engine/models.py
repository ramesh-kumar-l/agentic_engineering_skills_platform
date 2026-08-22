"""Shared dataclass schema for the adversarial-diff-reviewer engine."""

from __future__ import annotations

from dataclasses import dataclass, field


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
class DiffFile:
    old_path: str | None
    new_path: str | None
    is_new_file: bool = False
    is_deleted_file: bool = False
    hunks: list[Hunk] = field(default_factory=list)


@dataclass
class RiskFlag:
    pattern_id: str
    category: str
    severity: str  # "low" | "medium" | "high"
    file: str
    line: int
    description: str
    matched_text: str  # redacted for secret-shaped patterns; see risk_patterns.py


@dataclass
class DiffStats:
    files_touched: int
    files_added: int
    files_deleted: int
    lines_added: int
    lines_removed: int
    hunk_count: int


@dataclass
class DiffContext:
    files: list[DiffFile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class DiffIntelligenceReport:
    """The deterministic pre-review packet handed to the agent's adversarial workflow."""

    stats: DiffStats
    risk_flags: list[RiskFlag]
    files: list[DiffFile]
    warnings: list[str] = field(default_factory=list)
