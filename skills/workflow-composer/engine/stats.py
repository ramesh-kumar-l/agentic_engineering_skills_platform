"""Small summary stats over a WorkflowRunReport, kept separate from the
renderers so both JSON and Markdown output agree on the same numbers."""

from __future__ import annotations

from .models import StepStatus, WorkflowRunReport


def compute_stats(report: WorkflowRunReport) -> dict:
    counts = {status.value: 0 for status in StepStatus}
    total_duration = 0.0
    for result in report.step_results:
        counts[result.status.value] += 1
        if result.duration_seconds:
            total_duration += result.duration_seconds
    return {
        "step_count": len(report.step_results),
        "status_counts": counts,
        "total_duration_seconds": round(total_duration, 3),
        "compatibility_issue_count": len(report.compatibility_issues),
    }
