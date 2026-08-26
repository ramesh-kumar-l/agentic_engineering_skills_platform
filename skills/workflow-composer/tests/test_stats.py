from engine.models import (
    CompatibilityIssue,
    StepResult,
    StepStatus,
    WiringMode,
    WorkflowRunReport,
    WorkflowStep,
)
from engine.stats import compute_stats


def _step():
    return WorkflowStep(skill_name="a", output_filename="a.json", wiring_mode=WiringMode.CLI_FLAG)


def test_compute_stats_counts_by_status():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=False,
        step_results=[
            StepResult(step=_step(), status=StepStatus.OK, duration_seconds=1.0),
            StepResult(step=_step(), status=StepStatus.FAILED, duration_seconds=0.5),
            StepResult(step=_step(), status=StepStatus.SKIPPED),
        ],
    )
    stats = compute_stats(report)
    assert stats["step_count"] == 3
    assert stats["status_counts"]["OK"] == 1
    assert stats["status_counts"]["FAILED"] == 1
    assert stats["status_counts"]["SKIPPED"] == 1
    assert stats["status_counts"]["PENDING"] == 0
    assert stats["total_duration_seconds"] == 1.5


def test_compute_stats_includes_compatibility_issue_count():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=False,
        compatibility_issues=[CompatibilityIssue(step_skill_name="a", detail="d")],
    )
    stats = compute_stats(report)
    assert stats["compatibility_issue_count"] == 1


def test_compute_stats_on_empty_report():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=True
    )
    stats = compute_stats(report)
    assert stats["step_count"] == 0
    assert stats["total_duration_seconds"] == 0.0
