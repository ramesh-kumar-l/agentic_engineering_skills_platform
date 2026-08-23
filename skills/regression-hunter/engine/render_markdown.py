"""Condensed, human/agent-readable Markdown rendering of a
RegressionHunterReport. Keeps the three regression signals visibly
separate per file (ADR-015) rather than blending them into one line."""

from __future__ import annotations

from .models import RegressionHunterReport

TOP_N_FLAGS = 20
TOP_N_CALLERS = 10
_TIER_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: RegressionHunterReport) -> str:
    lines: list[str] = []
    lines.append("# Regression Hunter Pre-Decision Report")
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Files changed: {s.files_changed} (added: {s.files_added}, deleted: {s.files_deleted})")
    lines.append(f"- Lines added: {s.lines_added}, lines removed: {s.lines_removed}")
    lines.append(f"- Diff-pattern flags: {s.flag_count}")
    lines.append(f"- Files at HIGH overall risk: {s.high_risk_file_count}")
    lines.append("")

    lines.append(
        "## Per-File Risk Assessment (three separate signals, not blended — see ADR-015)"
    )
    if not report.files:
        lines.append("- No changed files parsed from the diff.")
    else:
        sorted_files = sorted(
            report.files, key=lambda f: _TIER_ORDER.get(f.overall_risk_tier, 3)
        )
        for f in sorted_files:
            kind = "new" if f.is_new_file else "deleted" if f.is_deleted_file else "modified"
            lines.append(
                f"### `{f.file}` ({kind}) — overall risk: **{f.overall_risk_tier.upper()}**"
            )
            lines.append(f"- Lines: +{f.lines_added} / -{f.lines_removed}")

            lines.append(
                f"- **Axis 1 — Diff-pattern flags** ({len(f.diff_pattern_flags)}):"
            )
            if not f.diff_pattern_flags:
                lines.append("  - None detected by pattern matching.")
            else:
                for flag in f.diff_pattern_flags[:TOP_N_FLAGS]:
                    lines.append(
                        f"  - [{flag.severity}] `{flag.pattern_id}` (line {flag.line}) — {flag.description}"
                    )
                remaining = len(f.diff_pattern_flags) - TOP_N_FLAGS
                if remaining > 0:
                    lines.append(f"  - ... and {remaining} more (see JSON output)")

            st = f.structural
            hotspot = " [hotspot]" if st.is_hotspot else ""
            lines.append(
                f"- **Axis 2 — Structural blast radius**: tier={st.structural_tier}, "
                f"resolved={st.resolved_module_path or '(unresolved)'}, "
                f"fan_in={st.fan_in}, fan_out={st.fan_out}{hotspot}"
            )
            if st.caller_modules:
                for c in st.caller_modules[:TOP_N_CALLERS]:
                    c_hotspot = " [hotspot]" if c.is_hotspot else ""
                    lines.append(f"  - caller: `{c.path}` (fan_in={c.fan_in}{c_hotspot})")
                remaining = len(st.caller_modules) - TOP_N_CALLERS
                if remaining > 0:
                    lines.append(f"  - ... and {remaining} more callers (see JSON output)")

            tc = f.test_coverage
            covered = "yes" if tc.has_coverage else "no"
            lines.append(f"- **Axis 3 — Test coverage**: covered={covered}")
            if tc.test_coverage_modules:
                lines.append(f"  - Covered by: {', '.join(tc.test_coverage_modules)}")
            lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
