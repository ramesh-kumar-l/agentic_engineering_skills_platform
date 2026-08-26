"""Renders a MemoryQueryReport as human-readable Markdown."""

from __future__ import annotations

from .models import MemoryQueryReport


def render_markdown(report: MemoryQueryReport) -> str:
    lines: list[str] = []
    lines.append("# Engineering Memory Retrieval Report")
    lines.append("")
    lines.append(
        "Matches below are retrieved leads from this project's own memory "
        "bank, not verdicts — a human/agent still judges genuine relevance "
        "and weighs any staleness flag before treating a match as current "
        "guidance (see SKILL.md)."
    )
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append(f"## Matches ({report.stats.match_count})")
    if not report.matches:
        lines.append("None found.")
    else:
        for m in report.matches:
            stale_marker = " [STALE]" if m.staleness.is_stale else ""
            lines.append(f"- **[{m.score}] {m.record.record_id}**{stale_marker}: {m.record.title}")
            lines.append(f"  - Source: `{m.record.source_file}:{m.record.source_line}`")
            if m.matched_keywords:
                lines.append(f"  - Matched keywords: {', '.join(m.matched_keywords)}")
            if m.matched_modules:
                lines.append(f"  - Matched modules: {', '.join(m.matched_modules)}")
            if m.staleness.is_stale:
                lines.append(f"  - Staleness: {m.staleness.reason}")
    lines.append("")

    lines.append("## Records scanned")
    lines.append(f"- Total: {report.stats.records_scanned}")
    for record_type, count in sorted(report.stats.records_scanned_by_type.items()):
        lines.append(f"  - {record_type}: {count}")

    return "\n".join(lines) + "\n"
