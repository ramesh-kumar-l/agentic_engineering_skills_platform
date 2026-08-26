import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cache.py",
            "docstring": "Redis-backed cache layer.",
            "functions": ["get", "set"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {
        "fan_in": {"engine/cache.py": 12},
        "fan_out": {"engine/cache.py": 2},
        "hotspots": ["engine/cache.py"],
    },
}


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        "Option A: use Redis cache instead of Postgres for sessions.",
        str(report_path),
    )

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["option_impacts"][0]["impacted_modules"][0]["path"] == "engine/cache.py"

    markdown_output = render_markdown(report)
    assert "Architecture Decision Pre-Decision Report" in markdown_output
    assert "engine/cache.py" in markdown_output


def test_report_never_fabricates_a_verdict(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        "Option A: use Redis cache instead of Postgres for sessions.",
        str(report_path),
    )
    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert "decision" not in parsed
    assert "recommendation" not in parsed
    assert "chosen_option" not in parsed
