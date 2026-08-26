from engine.models import (
    CompatibilityIssue,
    StepResult,
    StepStatus,
    WiringMode,
    WorkflowRunReport,
    WorkflowStep,
)
from engine.render_markdown import render_markdown


def test_render_markdown_includes_template_and_step_status():
    step = WorkflowStep(skill_name="feature-planner", output_filename="a.json",
                         wiring_mode=WiringMode.CLI_FLAG)
    report = WorkflowRunReport(
        template_name="understand-then-plan", repo_path="/r", task_description="x",
        dry_run=False,
        step_results=[StepResult(step=step, status=StepStatus.OK, exit_code=0,
                                  duration_seconds=1.234)],
    )
    md = render_markdown(report)
    assert "understand-then-plan" in md
    assert "feature-planner" in md
    assert "OK" in md
    assert "not Experiment B" in md


def test_render_markdown_includes_compatibility_issues_section():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=False,
        compatibility_issues=[CompatibilityIssue(step_skill_name="x", detail="drifted")],
    )
    md = render_markdown(report)
    assert "Compatibility issues" in md
    assert "drifted" in md


def test_render_markdown_includes_warnings_section():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=False,
        warnings=["refusing to execute"],
    )
    md = render_markdown(report)
    assert "Warnings" in md
    assert "refusing to execute" in md
