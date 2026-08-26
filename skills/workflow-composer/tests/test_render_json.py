import json

from engine.models import StepResult, StepStatus, WiringMode, WorkflowRunReport, WorkflowStep
from engine.render_json import render_json


def test_render_json_round_trips_and_includes_stats():
    step = WorkflowStep(skill_name="a", output_filename="a.json", wiring_mode=WiringMode.CLI_FLAG)
    report = WorkflowRunReport(
        template_name="understand-then-plan", repo_path="/r", task_description="x",
        dry_run=False,
        step_results=[StepResult(step=step, status=StepStatus.OK, exit_code=0)],
    )
    payload = json.loads(render_json(report))
    assert payload["template_name"] == "understand-then-plan"
    assert payload["step_results"][0]["status"] == "OK"
    assert payload["step_results"][0]["step"]["wiring_mode"] == "cli_flag"
    assert payload["stats"]["step_count"] == 1
