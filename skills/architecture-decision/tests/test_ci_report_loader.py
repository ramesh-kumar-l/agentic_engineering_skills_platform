import json

import pytest

from engine.ci_report_loader import CiReportError, load_ci_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/report.py",
            "docstring": "Builds the report.",
            "functions": ["build_report"],
            "classes": [],
            "imports": ["models"],
        }
    ],
    "dependency_graph": {
        "fan_in": {"engine/report.py": 2},
        "fan_out": {"engine/report.py": 1},
        "hotspots": ["engine/report.py"],
    },
}


def test_loads_valid_report(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    ctx = load_ci_report(report_path)

    assert ctx.root_path == "/repo"
    assert len(ctx.modules) == 1
    assert ctx.modules[0].path == "engine/report.py"
    assert ctx.dependency_graph.fan_in["engine/report.py"] == 2
    assert ctx.dependency_graph.hotspots == ["engine/report.py"]


def test_missing_report_raises_actionable_error(tmp_path):
    missing = tmp_path / "does-not-exist.json"
    with pytest.raises(CiReportError, match="not found"):
        load_ci_report(missing)


def test_malformed_json_raises_clear_error(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(CiReportError, match="not valid JSON"):
        load_ci_report(bad)


def test_missing_required_field_raises_clear_error(tmp_path):
    incomplete = tmp_path / "incomplete.json"
    incomplete.write_text(json.dumps({"modules": []}), encoding="utf-8")
    with pytest.raises(CiReportError, match="missing expected field"):
        load_ci_report(incomplete)
