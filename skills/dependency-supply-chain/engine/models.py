"""Shared dataclass schema for the dependency-supply-chain engine.

Composes on top of a required codebase-intelligence report.json (ADR-010,
reused a seventh time — see ci_report_loader.py). This engine reuses CI's
already-parsed `external_dependencies` list rather than re-parsing
requirements.txt/pyproject.toml/package.json itself — avoids an eleventh
copy of manifest-parsing logic and inherits (and documents, see
SKILL.md Known Limitations) CI's existing root-level-only parsing scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CiExternalDependency:
    """Local copy of codebase-intelligence's ExternalDependency — loaded
    independently of the codebase-intelligence package itself (no
    cross-package import), so this engine stays portable on its own."""

    name: str
    version: str | None
    source_file: str


@dataclass
class CiReportContext:
    """Lightweight local view of a codebase-intelligence report.json."""

    root_path: str
    dependencies: list[CiExternalDependency] = field(default_factory=list)


@dataclass
class DependencyRecord:
    """One declared dependency, enriched with this engine's own deterministic
    pin-status classification. `name` is exactly as declared in the source
    manifest — no name normalization is performed across ecosystems."""

    name: str
    version: str | None
    source_file: str
    pin_status: str = "missing"  # "pinned" | "range" | "wildcard" | "missing"


@dataclass
class RiskFlag:
    """A mechanically-detected supply-chain risk lead — never a verdict, same
    "leads not verdicts" discipline as every prior Pattern 2 anti-pattern
    table (ADR-007). See risk_patterns.py, license_patterns.py."""

    pattern_id: str
    category: str  # "unpinned-version" | "known-risk-name" | "license-risk" | "duplicate-version" | "wildcard-version"
    severity: str  # "low" | "medium" | "high"
    dependency_name: str
    description: str
    evidence: str


@dataclass
class SurfaceAreaStats:
    total_dependencies: int = 0
    unpinned_count: int = 0
    unpinned_percentage: float = 0.0
    manifest_breakdown: dict[str, int] = field(default_factory=dict)


@dataclass
class ReportStats:
    flag_count: int = 0
    flag_count_by_severity: dict[str, int] = field(default_factory=dict)
    flag_count_by_category: dict[str, int] = field(default_factory=dict)


@dataclass
class DependencySupplyChainReport:
    """The deterministic pre-decision packet handed to the agent's
    Dependency Risk Checklist workflow (SKILL.md Step 3). `suggested_risk_level`
    is ALWAYS a recommendation for a human to review — the engine never
    authorizes a merge/release decision itself (ADR-011 precedent)."""

    dependencies: list[DependencyRecord] = field(default_factory=list)
    flags: list[RiskFlag] = field(default_factory=list)
    surface_area: SurfaceAreaStats = field(default_factory=SurfaceAreaStats)
    stats: ReportStats = field(default_factory=ReportStats)
    suggested_risk_level: str = "REQUIRES_REVIEW"  # "CLEAR" | "NEEDS_REVIEW" | "REQUIRES_REVIEW"
    warnings: list[str] = field(default_factory=list)
