import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cart.py",
            "docstring": "Cart total computation.",
            "functions": ["total"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {
        "fan_in": {"engine/cart.py": 2},
        "fan_out": {"engine/cart.py": 1},
        "hotspots": ["engine/cart.py"],
    },
}


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        'Expected 10 but got 0. Steps to reproduce: add item. '
        'Error: File "engine/cart.py", line 12, in total',
        str(report_path),
    )

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["candidates"]["candidates"][0]["path"] == "engine/cart.py"

    markdown_output = render_markdown(report)
    assert "Root Cause Investigation Report" in markdown_output
    assert "engine/cart.py" in markdown_output


def test_report_never_fabricates_a_diagnosis(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        'Expected 10 but got 0. Steps to reproduce: add item. '
        'Error: File "engine/cart.py", line 12, in total',
        str(report_path),
    )
    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert "root_cause" not in parsed
    assert "diagnosis" not in parsed
    assert "fix" not in parsed
