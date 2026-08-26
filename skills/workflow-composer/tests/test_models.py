from engine.models import (
    StepResult,
    StepStatus,
    WiringMode,
    WorkflowRunReport,
    WorkflowStep,
    WorkflowTemplate,
)


def test_wiring_mode_values_are_plain_strings():
    assert WiringMode.CLI_FLAG == "cli_flag"
    assert WiringMode.TEXT_APPEND == "text_append"


def test_step_status_values_are_plain_strings():
    assert StepStatus.OK == "OK"
    assert StepStatus.FAILED == "FAILED"
    assert StepStatus.SKIPPED == "SKIPPED"
    assert StepStatus.PENDING == "PENDING"


def test_workflow_step_defaults():
    step = WorkflowStep(
        skill_name="codebase-intelligence",
        output_filename="report.json",
        wiring_mode=WiringMode.CLI_FLAG,
    )
    assert step.wiring_flag is None
    assert step.upstream_context_marker is None


def test_workflow_run_report_defaults_to_empty_collections():
    report = WorkflowRunReport(
        template_name="t", repo_path="/r", task_description="x", dry_run=True
    )
    assert report.compatibility_issues == []
    assert report.step_results == []
    assert report.warnings == []


def test_workflow_template_holds_ordered_steps():
    s1 = WorkflowStep(skill_name="a", output_filename="a.json", wiring_mode=WiringMode.CLI_FLAG)
    s2 = WorkflowStep(skill_name="b", output_filename="b.json", wiring_mode=WiringMode.TEXT_APPEND)
    template = WorkflowTemplate(name="t", description="d", steps=[s1, s2])
    assert template.steps == [s1, s2]


def test_step_result_optional_fields_default_none():
    step = WorkflowStep(skill_name="a", output_filename="a.json", wiring_mode=WiringMode.CLI_FLAG)
    result = StepResult(step=step, status=StepStatus.PENDING)
    assert result.exit_code is None
    assert result.output_path is None
    assert result.duration_seconds is None
    assert result.stderr_excerpt is None
