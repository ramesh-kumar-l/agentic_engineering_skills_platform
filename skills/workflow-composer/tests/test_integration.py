import json
from pathlib import Path

from engine.executor import run_workflow
from engine.models import WiringMode, WorkflowStep, WorkflowTemplate
from engine.render_json import render_json
from engine.render_markdown import render_markdown

_FAKE_SKILLS_ROOT = Path(__file__).parent / "fixtures" / "fake-skills"


def test_full_pipeline_run_workflow_to_both_renderers(tmp_path):
    template = WorkflowTemplate(
        name="fake-template", description="d",
        steps=[
            WorkflowStep(skill_name="skill-a", output_filename="report.json",
                         wiring_mode=WiringMode.CLI_FLAG),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report"),
        ],
    )
    report = run_workflow(
        template, repo_path=tmp_path, task_description="add a feature",
        out_dir=tmp_path / "out", platform_root=_FAKE_SKILLS_ROOT,
    )

    json_payload = json.loads(render_json(report))
    md = render_markdown(report)

    assert json_payload["stats"]["status_counts"]["OK"] == 2
    assert "fake-template" in md
    assert "skill-a" in md
    assert "skill-b" in md
    assert json_payload["template_name"] == md.splitlines()[0].split(" — ")[1]
