import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cli.py",
            "docstring": "CLI entry point.",
            "functions": ["main"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {
        "fan_in": {"engine/cli.py": 2},
        "fan_out": {"engine/cli.py": 1},
        "hotspots": ["engine/cli.py"],
    },
}


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report("Only update the CLI. Verify via tests.", str(report_path))

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["relevance"]["scores"][0]["path"] == "engine/cli.py"

    markdown_output = render_markdown(report)
    assert "Feature Planning Report" in markdown_output
    assert "engine/cli.py" in markdown_output


def test_report_never_fabricates_a_structured_plan(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report("Only update the CLI. Verify via tests.", str(report_path))
    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert "steps" not in parsed
    assert "scope" not in parsed
    assert "non_goals" not in parsed
