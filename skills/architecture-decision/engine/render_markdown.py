"""Condensed, human/agent-readable Markdown rendering of an
ArchitectureDecisionReport."""

from __future__ import annotations

from .models import ArchitectureDecisionReport

TOP_N_MODULES = 10
TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
_TIER_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: ArchitectureDecisionReport) -> str:
    lines: list[str] = []
    lines.append("# Architecture Decision Pre-Decision Report")
    lines.append("")
    lines.append("## Decision Text")
    lines.append(report.decision_text.strip())
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Words: {s.word_count}")
    lines.append(f"- Options parsed: {s.option_count}")
    lines.append(f"- Flags: {s.flag_count} (high severity: {s.high_severity_flag_count})")
    lines.append("")

    lines.append("## Decision Flags (mechanically-detected leads, not verdicts)")
    if not report.flags:
        lines.append("- None detected by pattern matching.")
    else:
        sorted_flags = sorted(report.flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 3))
        for flag in sorted_flags[:TOP_N_FLAGS]:
            lines.append(f"- [{flag.severity}] `{flag.pattern_id}` — {flag.description}")
        remaining = len(sorted_flags) - TOP_N_FLAGS
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    lines.append(
        "## Option Impact (codebase-intelligence-grounded blast radius, "
        "not just keyword mentions)"
    )
    if not report.option_impacts:
        lines.append("- No options parsed.")
    else:
        sorted_impacts = sorted(
            report.option_impacts, key=lambda oi: _TIER_ORDER.get(oi.blast_radius_tier, 3)
        )
        for oi in sorted_impacts:
            lines.append(
                f"### {oi.option_label} (blast radius: {oi.blast_radius_tier}, "
                f"score {oi.blast_radius_score}, hotspots touched: {oi.hotspot_count})"
            )
            lines.append(f"> {oi.option_text}")
            if not oi.impacted_modules:
                lines.append(
                    "- No matching modules — blast radius could not be derived "
                    "from real structural data for this option."
                )
            else:
                for m in oi.impacted_modules[:TOP_N_MODULES]:
                    hotspot = " [hotspot]" if m.is_hotspot else ""
                    lines.append(
                        f"- `{m.path}` (relevance {m.relevance_score}, "
                        f"fan_in={m.fan_in}, fan_out={m.fan_out}{hotspot}) — "
                        f"matched: {', '.join(m.matched_keywords) or '(none)'}"
                    )
                remaining = len(oi.impacted_modules) - TOP_N_MODULES
                if remaining > 0:
                    lines.append(f"- ... and {remaining} more (see JSON output for full list)")
            lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
