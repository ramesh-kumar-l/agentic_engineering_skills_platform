"""Condensed, human/agent-readable Markdown rendering of a
ReleaseReadinessReport. Keeps every axis visibly separate per file (ADR-016)
rather than blending them into one line, and states the overall_verdict as
an explicit recommendation, never as an executed decision."""

from __future__ import annotations

from .models import ReleaseReadinessReport

TOP_N_FLAGS = 20
TOP_N_CALLERS = 10
_TIER_ORDER = {"blocked": 0, "needs-review": 1, "clear": 2}


def render_markdown(report: ReleaseReadinessReport) -> str:
    lines: list[str] = []
    lines.append("# Release Readiness Scorecard")
    lines.append("")
    lines.append(
        f"## Overall Verdict: **{report.overall_verdict}**"
    )
    lines.append(
        "_This is a recommendation for a human to review, not an "
        "autonomous release gate — see SKILL.md's Security Constraints._"
    )
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Files changed: {s.files_changed} (added: {s.files_added}, deleted: {s.files_deleted})")
    lines.append(f"- Lines added: {s.lines_added}, lines removed: {s.lines_removed}")
    lines.append(f"- Diff-hygiene flags: {s.hygiene_flag_count}")
    lines.append(f"- Files BLOCKED: {s.blocked_file_count}")
    lines.append(f"- Files NEEDS-REVIEW: {s.needs_review_file_count}")
    lines.append(
        f"- Regression report composed: {report.regression_report_composed} "
        f"(optional — see ADR-011 precedent)"
    )
    lines.append(f"- Security report composed: {report.security_report_composed} (optional)")
    lines.append("")

    if report.security_evidence.available:
        lines.append("## Security Evidence (Axis 5, surfaced from security-context-guard, not re-derived)")
        lines.append(f"- sensitivity: {report.security_evidence.sensitivity}")
        lines.append(f"- suggested_verdict: {report.security_evidence.suggested_verdict}")
        lines.append(f"- source: {report.security_evidence.source_path}")
        lines.append("")

    lines.append(
        "## Per-File Readiness Assessment (axes kept separate, never blended — see ADR-016)"
    )
    if not report.files:
        lines.append("- No changed files parsed from the diff.")
    else:
        sorted_files = sorted(
            report.files, key=lambda f: _TIER_ORDER.get(f.readiness_tier, 3)
        )
        for f in sorted_files:
            kind = "new" if f.is_new_file else "deleted" if f.is_deleted_file else "modified"
            lines.append(
                f"### `{f.file}` ({kind}) — readiness: **{f.readiness_tier.upper()}**"
            )
            lines.append(f"- Lines: +{f.lines_added} / -{f.lines_removed}")

            lines.append(f"- **Axis 1 — Diff-hygiene flags** ({len(f.hygiene_flags)}):")
            if not f.hygiene_flags:
                lines.append("  - None detected by pattern matching.")
            else:
                for flag in f.hygiene_flags[:TOP_N_FLAGS]:
                    lines.append(
                        f"  - [{flag.severity}] `{flag.pattern_id}` (line {flag.line}) — {flag.description}"
                    )
                remaining = len(f.hygiene_flags) - TOP_N_FLAGS
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

            re_ = f.regression_evidence
            if re_.available:
                lines.append(
                    f"- **Axis 4 — Regression evidence (optional, surfaced not re-derived)**: "
                    f"overall_risk_tier={re_.overall_risk_tier}, "
                    f"diff_pattern_flag_count={re_.diff_pattern_flag_count}"
                )
            else:
                lines.append("- **Axis 4 — Regression evidence**: not supplied (`--regression-report` omitted or file not present in it)")
            lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
