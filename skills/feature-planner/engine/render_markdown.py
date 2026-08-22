"""Condensed, human/agent-readable Markdown rendering of a
FeaturePlanningReport."""

from __future__ import annotations

from .models import FeaturePlanningReport

TOP_N_RELEVANCE = 15
TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: FeaturePlanningReport) -> str:
    lines: list[str] = []
    lines.append("# Feature Planning Report")
    lines.append("")
    lines.append("## Task")
    lines.append(report.task_text.strip())
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Words: {s.word_count}")
    lines.append(f"- Vague scope markers: {s.vague_scope_count}")
    lines.append(f"- Weak goal modals: {s.weak_modal_count}")
    lines.append("")

    lines.append("## Planning Flags (mechanically-detected leads, not verdicts)")
    if not report.planning_flags:
        lines.append("- None detected by pattern matching.")
    else:
        sorted_flags = sorted(
            report.planning_flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 3)
        )
        for flag in sorted_flags[:TOP_N_FLAGS]:
            lines.append(f"- [{flag.severity}] `{flag.pattern_id}` — {flag.description}")
        remaining = len(sorted_flags) - TOP_N_FLAGS
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    lines.append("## Relevant Files (codebase-intelligence-grounded, ranked by keyword overlap)")
    lines.append(f"- Extracted keywords: {', '.join(report.relevance.keywords) or '(none)'}")
    if not report.relevance.scores:
        lines.append("- No matching modules found — affected files must be stated as an assumption.")
    else:
        for score in report.relevance.scores[:TOP_N_RELEVANCE]:
            hotspot = " [hotspot]" if score.is_hotspot else ""
            lines.append(
                f"- `{score.path}` (score {score.score}, fan_in={score.fan_in}, "
                f"fan_out={score.fan_out}{hotspot}) — matched: {', '.join(score.matched_keywords)}"
            )
        remaining = len(report.relevance.scores) - TOP_N_RELEVANCE
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
