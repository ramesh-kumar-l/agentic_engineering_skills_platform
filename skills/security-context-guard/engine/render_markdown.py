"""Condensed, human/agent-readable Markdown rendering of a
SecurityGuardReport."""

from __future__ import annotations

from .models import SecurityGuardReport

TOP_N = 20


def render_markdown(report: SecurityGuardReport) -> str:
    lines: list[str] = []
    lines.append("# Security Guard Report")
    lines.append("")

    c = report.classification
    lines.append("## Classification (recommendation only — not a self-executed gate)")
    lines.append(f"- Sensitivity: **{c.sensitivity}**")
    lines.append(f"- Suggested verdict: **{c.suggested_verdict}**")
    lines.append(f"- Uncertain: {c.uncertain}")
    for item in c.evidence:
        lines.append(f"  - {item}")
    lines.append("")

    s = report.stats
    lines.append("## Stats")
    lines.append(f"- Content words: {s.content_word_count}")
    lines.append(f"- Secret matches: {s.secret_count}")
    lines.append(f"- PII matches: {s.pii_count}")
    lines.append(f"- Sensitive path matches: {s.sensitive_path_count}")
    lines.append(f"- Action flags: {s.action_flag_count}")
    lines.append("")

    lines.append("## Secret Matches (redacted — leads, not verdicts)")
    if not report.secrets:
        lines.append("- None detected by pattern matching.")
    else:
        for m in report.secrets[:TOP_N]:
            lines.append(f"- [{m.severity}] `{m.pattern_id}` — {m.description}")
    lines.append("")

    lines.append("## PII Matches (redacted — leads, not verdicts)")
    if not report.pii:
        lines.append("- None detected by pattern matching.")
    else:
        for m in report.pii[:TOP_N]:
            lines.append(f"- [{m.category}] `{m.pattern_id}` — {m.description}")
    lines.append("")

    lines.append("## Sensitive Paths")
    if not report.sensitive_paths:
        lines.append("- None of the given paths matched a sensitive-path convention.")
    else:
        for m in report.sensitive_paths[:TOP_N]:
            lines.append(f"- `{m.path}` — {m.description}")
    lines.append("")

    lines.append(f"## Action ({', '.join(sorted({f.category for f in report.action_flags})) or 'no category matched'})")
    lines.append(report.action_text_redacted.strip() or "(none provided)")
    if report.action_flags:
        for f in report.action_flags[:TOP_N]:
            lines.append(f"- [{f.category}] `{f.pattern_id}` — {f.description}")
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
