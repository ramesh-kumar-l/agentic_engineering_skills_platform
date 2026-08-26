from pathlib import Path

from engine.executor import run_workflow
from engine.models import StepStatus, WiringMode, WorkflowStep, WorkflowTemplate

_FAKE_SKILLS_ROOT = Path(__file__).parent / "fixtures" / "fake-skills"


def _template(step2_marker=None, wiring_mode=WiringMode.CLI_FLAG):
    return WorkflowTemplate(
        name="fake-template",
        description="d",
        steps=[
            WorkflowStep(skill_name="skill-a", output_filename="report.json",
                         wiring_mode=WiringMode.CLI_FLAG),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=wiring_mode,
                         wiring_flag="--ci-report" if wiring_mode == WiringMode.CLI_FLAG else None,
                         upstream_context_marker=step2_marker),
        ],
    )


def test_full_chain_succeeds_and_wires_ci_report_flag(tmp_path):
    report = run_workflow(
        _template(), repo_path=tmp_path, task_description="do the task",
        out_dir=tmp_path / "out", platform_root=_FAKE_SKILLS_ROOT,
    )
    assert [r.status for r in report.step_results] == [StepStatus.OK, StepStatus.OK]
    assert report.step_results[1].output_path is not None


def test_text_append_wiring_reaches_downstream_step(tmp_path):
    import json

    report = run_workflow(
        _template(wiring_mode=WiringMode.TEXT_APPEND), repo_path=tmp_path,
        task_description="do the task", out_dir=tmp_path / "out",
        platform_root=_FAKE_SKILLS_ROOT,
    )
    assert report.step_results[1].status == StepStatus.OK
    written = json.loads(Path(report.step_results[1].output_path).read_text(encoding="utf-8"))
    assert "Codebase Intelligence context" in written["task_text"]
    assert written["received_ci_report"] is None


def test_downstream_step_failure_is_recorded(tmp_path):
    report = run_workflow(
        _template(), repo_path=tmp_path, task_description="TRIGGER_FAIL",
        out_dir=tmp_path / "out", platform_root=_FAKE_SKILLS_ROOT,
    )
    assert report.step_results[0].status == StepStatus.OK
    assert report.step_results[1].status == StepStatus.FAILED


def test_failed_step_marks_remaining_steps_skipped(tmp_path):
    three_step = WorkflowTemplate(
        name="three", description="d",
        steps=[
            WorkflowStep(skill_name="skill-a", output_filename="report.json",
                         wiring_mode=WiringMode.CLI_FLAG),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report"),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report"),
        ],
    )
    report = run_workflow(
        three_step, repo_path=tmp_path, task_description="TRIGGER_FAIL",
        out_dir=tmp_path / "out", platform_root=_FAKE_SKILLS_ROOT,
    )
    assert report.step_results[1].status == StepStatus.FAILED
    assert report.step_results[2].status == StepStatus.SKIPPED


def test_compatibility_drift_blocks_all_real_execution(tmp_path):
    report = run_workflow(
        _template(step2_marker="skill-a"), repo_path=tmp_path,
        task_description="do the task", out_dir=tmp_path / "out",
        platform_root=_FAKE_SKILLS_ROOT,
    )
    assert len(report.compatibility_issues) == 1
    assert all(r.status == StepStatus.SKIPPED for r in report.step_results)
    assert report.warnings


def test_dry_run_never_calls_subprocess_even_with_no_drift(tmp_path):
    report = run_workflow(
        _template(), repo_path=tmp_path, task_description="do the task",
        out_dir=tmp_path / "out", dry_run=True, platform_root=_FAKE_SKILLS_ROOT,
    )
    assert all(r.status == StepStatus.PENDING for r in report.step_results)
    assert not (tmp_path / "out").exists() or not any((tmp_path / "out").rglob("*.json"))
