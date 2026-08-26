"""Condensed, human/agent-readable Markdown rendering of a RootCauseReport."""

from __future__ import annotations

from .models import RootCauseReport

TOP_N_CANDIDATES = 15
TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: RootCauseReport) -> str:
    lines: list[str] = []
    lines.append("# Root Cause Investigation Report")
    lines.append("")
    lines.append("## Symptom")
    lines.append(report.symptom_text.strip())
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Words: {s.word_count}")
    lines.append(f"- Vague symptom markers: {s.vague_symptom_count}")
    lines.append(f"- Parsed stack frames: {s.stack_frame_count}")
    lines.append("")

    lines.append("## Symptom Flags (mechanically-detected leads, not verdicts)")
    if not report.symptom_flags:
        lines.append("- None detected by pattern matching.")
    else:
        sorted_flags = sorted(
            report.symptom_flags, key=lambda f: _SEVERITY_ORDER.get(f.severity, 3)
        )
        for flag in sorted_flags[:TOP_N_FLAGS]:
            lines.append(f"- [{flag.severity}] `{flag.pattern_id}` — {flag.description}")
        remaining = len(sorted_flags) - TOP_N_FLAGS
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    lines.append("## Parsed Stack Frames")
    if not report.candidates.stack_frames:
        lines.append("- None found in the symptom text.")
    else:
        for frame in report.candidates.stack_frames:
            symbol = f", in {frame.symbol}" if frame.symbol else ""
            lines.append(f"- `{frame.path}:{frame.line}`{symbol}")
    lines.append("")

    lines.append(
        "## Candidate Locations (codebase-intelligence-grounded, "
        "stack-trace evidence ranked above keyword overlap)"
    )
    lines.append(f"- Extracted keywords: {', '.join(report.candidates.keywords) or '(none)'}")
    if not report.candidates.candidates:
        lines.append("- No candidate locations found — root cause location must be stated as an assumption.")
    else:
        for c in report.candidates.candidates[:TOP_N_CANDIDATES]:
            hotspot = " [hotspot]" if c.is_hotspot else ""
            evidence = "STACK-TRACE HIT" if c.stack_trace_hit else "keyword"
            lines.append(
                f"- `{c.path}` (score {c.score}, tier={evidence}, fan_in={c.fan_in}, "
                f"fan_out={c.fan_out}{hotspot}) — matched: {', '.join(c.matched_keywords) or '(none)'}"
            )
        remaining = len(report.candidates.candidates) - TOP_N_CANDIDATES
        if remaining > 0:
            lines.append(f"- ... and {remaining} more (see JSON output for full list)")
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
