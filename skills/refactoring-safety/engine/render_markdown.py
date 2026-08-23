"""Condensed, human/agent-readable Markdown rendering of a
RefactoringSafetyReport."""

from __future__ import annotations

from .models import RefactoringSafetyReport

TOP_N_CALLERS = 10
TOP_N_FLAGS = 20
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
_TIER_ORDER = {"high": 0, "medium": 1, "low": 2}


def render_markdown(report: RefactoringSafetyReport) -> str:
    lines: list[str] = []
    lines.append("# Refactoring Safety Pre-Decision Report")
    lines.append("")
    lines.append("## Refactor Description")
    lines.append(report.refactor_text.strip())
    lines.append("")
    lines.append(f"**Detected operation type:** `{report.operation_type}`")
    lines.append("")

    lines.append("## Stats")
    s = report.stats
    lines.append(f"- Words: {s.word_count}")
    lines.append(f"- Targets parsed: {s.target_count} (resolved: {s.resolved_target_count})")
    lines.append(f"- Flags: {s.flag_count} (high severity: {s.high_severity_flag_count})")
    lines.append("")

    lines.append("## Safety Flags (mechanically-detected leads, not verdicts)")
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
        "## Target Assessment (codebase-intelligence-grounded blast radius "
        "+ test coverage, not just a name match)"
    )
    if not report.targets:
        lines.append("- No targets parsed.")
    else:
        sorted_targets = sorted(report.targets, key=lambda t: _TIER_ORDER.get(t.risk_tier, 3))
        for t in sorted_targets:
            if t.resolved_module_path is None:
                lines.append(f"### `{t.target_name}` — unresolved")
                lines.append(
                    "- Did not match any module, function, or class in the "
                    "codebase-intelligence report."
                )
                lines.append("")
                continue

            hotspot = " [hotspot]" if t.is_hotspot else ""
            tested = "yes" if t.test_coverage_modules else "no"
            lines.append(
                f"### `{t.target_name}` -> `{t.resolved_module_path}` "
                f"(risk: {t.risk_tier}, fan_in={t.fan_in}, fan_out={t.fan_out}"
                f"{hotspot}, test coverage: {tested})"
            )
            if t.matched_functions or t.matched_classes:
                lines.append(
                    f"- Matched symbols: functions={t.matched_functions or '(none)'}, "
                    f"classes={t.matched_classes or '(none)'}"
                )
            if not t.caller_modules:
                lines.append("- No caller modules found in the dependency graph.")
            else:
                for c in t.caller_modules[:TOP_N_CALLERS]:
                    c_hotspot = " [hotspot]" if c.is_hotspot else ""
                    lines.append(
                        f"- caller: `{c.path}` (fan_in={c.fan_in}, "
                        f"fan_out={c.fan_out}{c_hotspot})"
                    )
                remaining = len(t.caller_modules) - TOP_N_CALLERS
                if remaining > 0:
                    lines.append(f"- ... and {remaining} more callers (see JSON output)")
            if t.test_coverage_modules:
                lines.append(f"- Covered by: {', '.join(t.test_coverage_modules)}")
            lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)
