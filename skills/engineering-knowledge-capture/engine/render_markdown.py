"""Renders a KnowledgeCaptureReport as human-readable Markdown."""

from __future__ import annotations

from .models import KnowledgeCaptureReport

_PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def render_markdown(report: KnowledgeCaptureReport) -> str:
    lines: list[str] = []
    lines.append("# Engineering Knowledge Capture Report")
    lines.append("")
    lines.append(
        "Candidates below are leads for a human/agent to review and possibly "
        "draft into a canonical ADR / known-limitation / lessons-learned "
        "entry — this skill never writes into the memory bank itself (see SKILL.md)."
    )
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append(f"## Candidates ({report.stats.candidate_count})")
    if not report.candidates:
        lines.append("None found.")
    else:
        for c in sorted(report.candidates, key=lambda c: _PRIORITY_ORDER.get(c.suggested_capture_priority, 9)):
            if c.resolved_module_path:
                location = f" — resolved to `{c.resolved_module_path}`" + (
                    " (hotspot)" if c.is_hotspot else f" (fan_in={c.fan_in})"
                )
            else:
                location = " — no resolvable location"
            lines.append(
                f"- **[{c.suggested_capture_priority}] {c.category}** (`{c.pattern_id}`){location}"
            )
            lines.append(f"  > {c.evidence}")
    lines.append("")

    lines.append("## Category breakdown")
    if not report.stats.candidate_count_by_category:
        lines.append("None found.")
    for category, count in sorted(report.stats.candidate_count_by_category.items()):
        lines.append(f"- {category}: {count}")
    lines.append("")

    lines.append("## Priority breakdown")
    if not report.stats.candidate_count_by_priority:
        lines.append("None found.")
    for priority, count in sorted(report.stats.candidate_count_by_priority.items()):
        lines.append(f"- {priority}: {count}")

    return "\n".join(lines) + "\n"
