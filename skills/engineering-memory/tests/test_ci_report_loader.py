import json

import pytest
from engine.ci_report_loader import CiReportError, load_ci_report


def _write(tmp_path, name, content):
    path = tmp_path / name
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_text(json.dumps(content), encoding="utf-8")
    return path


def test_missing_file_raises_ci_report_error(tmp_path):
    with pytest.raises(CiReportError, match="not found"):
        load_ci_report(tmp_path / "does-not-exist.json")


def test_malformed_json_raises_ci_report_error(tmp_path):
    path = _write(tmp_path, "report.json", "{not valid json")
    with pytest.raises(CiReportError, match="not valid JSON"):
        load_ci_report(path)


def test_missing_required_field_raises_ci_report_error(tmp_path):
    path = _write(tmp_path, "report.json", {"root_path": "/repo"})
    with pytest.raises(CiReportError, match="missing expected field"):
        load_ci_report(path)


def test_loads_modules_and_dependency_graph(tmp_path):
    path = _write(tmp_path, "report.json", {
        "root_path": "/repo",
        "modules": [
            {"path": "engine/scanner.py", "docstring": "Scans things.",
             "functions": ["scan"], "classes": [], "imports": ["engine.models"]},
        ],
        "dependency_graph": {
            "fan_in": {"engine/scanner.py": 5},
            "fan_out": {"engine/scanner.py": 1},
            "hotspots": ["engine/scanner.py"],
        },
    })
    ctx = load_ci_report(path)
    assert ctx.root_path == "/repo"
    assert len(ctx.modules) == 1
    assert ctx.modules[0].path == "engine/scanner.py"
    assert ctx.dependency_graph.fan_in["engine/scanner.py"] == 5
    assert "engine/scanner.py" in ctx.dependency_graph.hotspots


def test_missing_dependency_graph_defaults_to_empty(tmp_path):
    path = _write(tmp_path, "report.json", {"root_path": "/repo", "modules": []})
    ctx = load_ci_report(path)
    assert ctx.dependency_graph.fan_in == {}
    assert ctx.dependency_graph.hotspots == []
