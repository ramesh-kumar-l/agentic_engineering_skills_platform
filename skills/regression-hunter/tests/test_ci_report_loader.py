import json

import pytest

from engine.ci_report_loader import CiReportError, load_ci_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cache.py",
            "docstring": "Cache helper.",
            "functions": ["get", "set"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {"fan_in": {"engine/cache.py": 3}, "fan_out": {}, "hotspots": []},
}


def test_raises_when_report_missing(tmp_path):
    with pytest.raises(CiReportError, match="not found"):
        load_ci_report(tmp_path / "nope.json")


def test_raises_on_malformed_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CiReportError, match="not valid JSON"):
        load_ci_report(path)


def test_raises_on_missing_required_field(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps({"modules": []}), encoding="utf-8")
    with pytest.raises(CiReportError, match="missing expected field"):
        load_ci_report(path)


def test_loads_valid_report(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    ctx = load_ci_report(path)

    assert ctx.root_path == "/repo"
    assert ctx.modules[0].path == "engine/cache.py"
    assert ctx.dependency_graph.fan_in["engine/cache.py"] == 3
