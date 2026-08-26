"""Renders a ContextOptimizationReport as human-readable Markdown."""

from __future__ import annotations

from .models import ContextOptimizationReport

_TIER_ORDER = {"CORE": 0, "SUPPORTING": 1, "EXCLUDED": 2}


def render_markdown(report: ContextOptimizationReport) -> str:
    lines: list[str] = []
    lines.append("# Context Optimization Report")
    lines.append("")
    lines.append(
        "Recommendations below are a deterministic relevance signal for a "
        "human/agent to review, not a claim that this file set is complete "
        "or sufficient — this skill never loads files into any actual "
        "context window itself (see SKILL.md)."
    )
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append(f"## Task keywords ({len(report.task_keywords)})")
    lines.append(", ".join(report.task_keywords) if report.task_keywords else "None extracted.")
    lines.append("")

    lines.append(f"## Recommendations ({report.stats.candidate_count})")
    if not report.recommendations:
        lines.append("None found.")
    else:
        for r in sorted(
            report.recommendations,
            key=lambda r: (_TIER_ORDER.get(r.tier, 9), -r.relevance_score),
        ):
            structural = " (hotspot)" if r.is_hotspot else f" (fan_in={r.fan_in})"
            oversized = " — OVERSIZED ALONE" if r.oversized_alone else ""
            lines.append(
                f"- **[{r.tier}] `{r.path}`** score={r.relevance_score}{structural}, "
                f"~{r.estimated_tokens} est. tokens ({r.line_count} lines){oversized}"
            )
            if r.matched_keywords:
                lines.append(f"  matched: {', '.join(r.matched_keywords)}")
            for note in r.notes:
                lines.append(f"  > {note}")
    lines.append("")

    lines.append("## Tier breakdown")
    if not report.stats.candidate_count_by_tier:
        lines.append("None found.")
    for tier, count in sorted(
        report.stats.candidate_count_by_tier.items(), key=lambda kv: _TIER_ORDER.get(kv[0], 9)
    ):
        lines.append(f"- {tier}: {count}")
    lines.append("")

    lines.append(
        f"## Estimated context budget: ~{report.stats.total_estimated_tokens} tokens "
        f"(CORE + SUPPORTING only; crude line-count heuristic, not a real tokenizer — "
        f"see SKILL.md Known Limitations)"
    )
    if report.stats.oversized_alone_count:
        lines.append(
            f"- {report.stats.oversized_alone_count} file(s) flagged oversized-alone — "
            "see notes above."
        )

    return "\n".join(lines) + "\n"
