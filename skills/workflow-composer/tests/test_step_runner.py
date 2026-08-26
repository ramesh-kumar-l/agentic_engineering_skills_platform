from pathlib import Path

from engine.models import StepStatus, WiringMode, WorkflowStep
from engine.step_runner import build_argv, prepare_downstream_input, run_step

_FAKE_SKILLS_ROOT = Path(__file__).parent / "fixtures" / "fake-skills"


def _skill_dir(name):
    return _FAKE_SKILLS_ROOT / "skills" / name


def test_prepare_downstream_input_cli_flag_mode_leaves_text_unchanged(tmp_path):
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report")
    task_file = prepare_downstream_input(step, "do the task", None, tmp_path)
    assert task_file.read_text(encoding="utf-8") == "do the task"


def test_prepare_downstream_input_text_append_adds_ci_excerpt(tmp_path):
    upstream = tmp_path / "report.json"
    upstream.write_text(
        '{"file_count": 3, "dependency_graph": {"hotspots": ["a.py"]}, "entry_points": []}',
        encoding="utf-8",
    )
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.TEXT_APPEND)
    task_file = prepare_downstream_input(step, "do the task", upstream, tmp_path)
    text = task_file.read_text(encoding="utf-8")
    assert "do the task" in text
    assert "Codebase Intelligence context" in text
    assert "a.py" in text


def test_prepare_downstream_input_text_append_tolerates_bad_json(tmp_path):
    upstream = tmp_path / "report.json"
    upstream.write_text("not json", encoding="utf-8")
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.TEXT_APPEND)
    task_file = prepare_downstream_input(step, "do the task", upstream, tmp_path)
    assert task_file.read_text(encoding="utf-8") == "do the task"


def test_build_argv_cli_flag_includes_flag(tmp_path):
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report")
    argv = build_argv(step, positional_arg="task.txt",
                       upstream_output_path=Path("report.json"), step_out_dir=tmp_path)
    assert "--ci-report" in argv
    assert "report.json" in argv


def test_build_argv_text_append_never_includes_flag(tmp_path):
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.TEXT_APPEND)
    argv = build_argv(step, positional_arg="task.txt",
                       upstream_output_path=Path("report.json"), step_out_dir=tmp_path)
    assert "--ci-report" not in argv


def test_run_step_dry_run_never_spawns_subprocess(tmp_path):
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report")
    result = run_step(step, skill_dir=_skill_dir("skill-b"), positional_arg="anything",
                       upstream_output_path=None, step_out_dir=tmp_path, dry_run=True)
    assert result.status == StepStatus.PENDING
    assert not (tmp_path / "out.json").exists()


def test_run_step_real_success(tmp_path):
    task_file = tmp_path / "input.txt"
    task_file.write_text("do the task", encoding="utf-8")
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report")
    out_dir = tmp_path / "out"
    result = run_step(step, skill_dir=_skill_dir("skill-b"), positional_arg=str(task_file),
                       upstream_output_path=None, step_out_dir=out_dir, dry_run=False)
    assert result.status == StepStatus.OK
    assert result.exit_code == 0
    assert result.output_path == str(out_dir / "out.json")


def test_run_step_real_failure_on_nonzero_exit(tmp_path):
    task_file = tmp_path / "input.txt"
    task_file.write_text("TRIGGER_FAIL", encoding="utf-8")
    step = WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report")
    out_dir = tmp_path / "out"
    result = run_step(step, skill_dir=_skill_dir("skill-b"), positional_arg=str(task_file),
                       upstream_output_path=None, step_out_dir=out_dir, dry_run=False)
    assert result.status == StepStatus.FAILED
    assert result.exit_code == 1
    assert not (out_dir / "out.json").exists()
