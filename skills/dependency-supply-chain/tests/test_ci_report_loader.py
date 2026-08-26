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
    path = _write(tmp_path, "report.json", {"external_dependencies": []})
    with pytest.raises(CiReportError, match="missing expected field"):
        load_ci_report(path)


def test_loads_external_dependencies(tmp_path):
    path = _write(tmp_path, "report.json", {
        "root_path": "/repo",
        "external_dependencies": [
            {"name": "requests", "version": "2.28.0", "source_file": "requirements.txt"},
            {"name": "flask", "version": None, "source_file": "requirements.txt"},
        ],
    })
    ctx = load_ci_report(path)
    assert ctx.root_path == "/repo"
    assert len(ctx.dependencies) == 2
    assert ctx.dependencies[0].name == "requests"
    assert ctx.dependencies[1].version is None


def test_missing_external_dependencies_field_defaults_to_empty(tmp_path):
    path = _write(tmp_path, "report.json", {"root_path": "/repo"})
    ctx = load_ci_report(path)
    assert ctx.dependencies == []
