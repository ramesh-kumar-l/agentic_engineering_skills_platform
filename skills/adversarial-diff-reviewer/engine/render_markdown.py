"""Condensed, human/agent-readable Markdown rendering of a DiffIntelligenceReport."""

from __future__ import annotations

from .models import DiffIntelligenceReport

TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: DiffIntelligenceReport) -> str:
    lines: list[str] = []
    lines.append("# Diff Intelligence Report")
    lines.append("")
    lines.append("## Stats")
    s = report.stats
    lines.append(
        f"- Files touched: {s.files_touched} "
        f"(added: {s.files_added}, deleted: {s.files_deleted})"
    )
    lines.append(f"- Lines: +{s.lines_added} / -{s.lines_removed}")
    lines.append(f"- Hunks: {s.hunk_count}")
    lines.append("")

    lines.append("## Files")
    for f in report.files:
        label = f.new_path or f.old_path or "<unknown>"
        tag = " (new)" if f.is_new_file else " (deleted)" if f.is_deleted_file else ""
        lines.append(f"- {label}{tag}")
    lines.append("")

    lines.append("## Risk Flags (mechanically-detected leads, not verdicts)")
    if not report.risk_flags:
        lines.append("- None detected by pattern matching.")
    else:
        sorted_flags = sorted(
            report.risk_flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 3)
        )
        for flag in sorted_flags[:TOP_N_FLAGS]:
            lines.append(
                f"- [{flag.severity}] `{flag.pattern_id}` "
                f"{flag.file}:{flag.line} — {flag.description}"
            )
        remaining = len(sorted_flags) - TOP_N_FLAGS
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
