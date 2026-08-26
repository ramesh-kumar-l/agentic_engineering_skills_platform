"""Markdown rendering for a WorkflowRunReport."""

from __future__ import annotations

from .models import WorkflowRunReport
from .stats import compute_stats


def render_markdown(report: WorkflowRunReport) -> str:
    stats = compute_stats(report)
    lines = [
        f"# Workflow Run Report — {report.template_name}",
        "",
        f"- Repo path: `{report.repo_path}`",
        f"- Dry run: {report.dry_run}",
        f"- Task: {report.task_description.strip()[:200]}",
        f"- Steps: {stats['step_count']} "
        f"(OK={stats['status_counts']['OK']}, "
        f"FAILED={stats['status_counts']['FAILED']}, "
        f"SKIPPED={stats['status_counts']['SKIPPED']}, "
        f"PENDING={stats['status_counts']['PENDING']})",
        f"- Total duration: {stats['total_duration_seconds']}s",
        "",
    ]

    if report.compatibility_issues:
        lines.append("## Compatibility issues")
        for issue in report.compatibility_issues:
            lines.append(f"- **{issue.step_skill_name}**: {issue.detail}")
        lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for warning in report.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append("## Steps")
    for index, result in enumerate(report.step_results, start=1):
        lines.append(f"### Step {index}: {result.step.skill_name} — {result.status.value}")
        if result.exit_code is not None:
            lines.append(f"- exit_code: {result.exit_code}")
        if result.duration_seconds is not None:
            lines.append(f"- duration_seconds: {result.duration_seconds:.3f}")
        if result.output_path:
            lines.append(f"- output_path: `{result.output_path}`")
        if result.stderr_excerpt:
            lines.append(f"- stderr_excerpt: `{result.stderr_excerpt}`")
        lines.append("")

    lines.append("## Reminder")
    lines.append(
        "This is a real execution run, not Experiment B (ADR-009) — timing "
        "data here is disclosed evidence, never cited as validating A10."
    )
    return "\n".join(lines) + "\n"
