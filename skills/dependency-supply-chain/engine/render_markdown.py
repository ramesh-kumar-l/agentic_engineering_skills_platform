"""Renders a DependencySupplyChainReport as human-readable Markdown."""

from __future__ import annotations

from .models import DependencySupplyChainReport

_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: DependencySupplyChainReport) -> str:
    lines: list[str] = []
    lines.append("# Dependency / Supply Chain Report")
    lines.append("")
    lines.append(
        f"**Suggested risk level: {report.suggested_risk_level}** "
        "— advisory only; a human/agent makes the real call (see SKILL.md)."
    )
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    sa = report.surface_area
    lines.append("## Surface area")
    lines.append(f"- Total direct dependencies: {sa.total_dependencies}")
    lines.append(f"- Unpinned: {sa.unpinned_count} ({sa.unpinned_percentage}%)")
    for manifest, count in sorted(sa.manifest_breakdown.items()):
        lines.append(f"  - {manifest}: {count}")
    lines.append("")

    lines.append(f"## Flags ({report.stats.flag_count})")
    if not report.flags:
        lines.append("None found.")
    else:
        for flag in sorted(report.flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 9)):
            lines.append(
                f"- **[{flag.severity.upper()}] {flag.category}** — "
                f"{flag.dependency_name}: {flag.description} ({flag.evidence})"
            )
    lines.append("")

    lines.append(f"## Dependencies ({len(report.dependencies)})")
    for dep in sorted(report.dependencies, key=lambda d: d.name.lower()):
        lines.append(f"- `{dep.name}` {dep.version or '(none)'} [{dep.pin_status}] — {dep.source_file}")

    return "\n".join(lines) + "\n"
