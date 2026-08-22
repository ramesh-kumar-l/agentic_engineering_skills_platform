"""Condensed, human/agent-readable Markdown rendering of an
AcceptanceTestabilityReport."""

from __future__ import annotations

from .models import AcceptanceTestabilityReport

TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: AcceptanceTestabilityReport) -> str:
    lines: list[str] = []
    lines.append("# Acceptance Testability Report")
    lines.append("")
    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Sentences: {s.sentence_count}  (words: {s.word_count})")
    lines.append(f"- Vague terms: {s.vague_term_count}")
    lines.append(f"- Weak modal verbs: {s.weak_modal_count}")
    lines.append(f"- Numeric quantifiers present: {s.numeric_quantifier_count}")
    lines.append(f"- Existing acceptance-criteria markers: {s.existing_criteria_markers}")
    lines.append("")

    lines.append("## Sentences")
    for sentence in report.sentences:
        lines.append(f"{sentence.index}. {sentence.text}")
    lines.append("")

    lines.append("## Testability Flags (mechanically-detected leads, not verdicts)")
    if not report.testability_flags:
        lines.append("- None detected by pattern matching.")
    else:
        sorted_flags = sorted(
            report.testability_flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 3)
        )
        for flag in sorted_flags[:TOP_N_FLAGS]:
            where = f"sentence {flag.sentence_index}" if flag.sentence_index is not None else "whole document"
            lines.append(
                f"- [{flag.severity}] `{flag.pattern_id}` ({where}) — {flag.description}"
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
