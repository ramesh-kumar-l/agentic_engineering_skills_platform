import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/report.py",
            "docstring": "Builds the report.",
            "functions": ["build_report"],
            "classes": [],
            "imports": [],
        },
        {
            "path": "engine/cli.py",
            "docstring": "CLI entry point.",
            "functions": ["main"],
            "classes": [],
            "imports": ["engine.report"],
        },
        {
            "path": "tests/test_report.py",
            "docstring": "",
            "functions": ["test_build_report"],
            "classes": [],
            "imports": ["engine.report"],
        },
    ],
    "dependency_graph": {
        "fan_in": {"engine/report.py": 6},
        "fan_out": {},
        "hotspots": ["engine/report.py"],
    },
}


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        "Rename `report.py` to `builder.py`. Update all callers.",
        str(report_path),
    )

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["targets"][0]["resolved_module_path"] == "engine/report.py"

    markdown_output = render_markdown(report)
    assert "Refactoring Safety Pre-Decision Report" in markdown_output
    assert "engine/report.py" in markdown_output


def test_covered_target_has_no_untested_flag(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(
        "Rename `report.py`. Update all callers. Run tests. Revert if broken.",
        str(report_path),
    )

    assert report.targets[0].test_coverage_modules == ["tests/test_report.py"]
    assert not any(f.category == "untested-blast-radius" for f in report.flags)
