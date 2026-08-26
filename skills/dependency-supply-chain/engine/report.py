"""Top-level orchestration: loads a codebase-intelligence report.json
(required precondition, ADR-010), scans its `external_dependencies`, and
assembles the final DependencySupplyChainReport handed to the agent's
Dependency Risk Checklist workflow.
"""

from __future__ import annotations

from pathlib import Path

from .ci_report_loader import load_ci_report
from .models import DependencySupplyChainReport
from .risk_scorer import compute_risk_level
from .scanner import scan
from .stats import compute_stats
from .surface_area import compute_surface_area


def build_report(ci_report_path: str | Path) -> DependencySupplyChainReport:
    ci_context = load_ci_report(ci_report_path)

    records, flags = scan(ci_context.dependencies)
    surface_area = compute_surface_area(records)
    stats = compute_stats(flags)

    warnings: list[str] = []
    if not ci_context.dependencies:
        warnings.append(
            "codebase-intelligence report declared zero external_dependencies — "
            "either the target repo genuinely has none, or it uses a manifest "
            "format codebase-intelligence's external_deps.py doesn't parse "
            "(e.g. Pipfile, poetry's [tool.poetry.dependencies] block, a "
            "non-root-level manifest). Treat a zero-dependency result with "
            "suspicion, not as confirmation of a clean supply chain."
        )

    risk_level = compute_risk_level(flags, len(records), warnings)

    return DependencySupplyChainReport(
        dependencies=records,
        flags=flags,
        surface_area=surface_area,
        stats=stats,
        suggested_risk_level=risk_level,
        warnings=warnings,
    )
