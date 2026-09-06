import json

import pytest

from project_intelligence.ci_report_loader import CiReportError, load_ci_report

_VALID_REPORT = {
    "root_path": "/tmp/target",
    "language_breakdown": {"python": 3},
    "external_dependencies": [{"name": "pytest", "version": "7.0", "source_file": "pyproject.toml"}],
    "files": [{"path": "pyproject.toml"}, {"path": "src/main.py"}],
}


def test_missing_file_raises_ci_report_error(tmp_path):
    with pytest.raises(CiReportError, match="not found"):
        load_ci_report(tmp_path / "does-not-exist.json")


def test_malformed_json_raises_ci_report_error(tmp_path):
    path = tmp_path / "report.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(CiReportError, match="not valid JSON"):
        load_ci_report(path)


def test_missing_required_field_raises_ci_report_error(tmp_path):
    path = tmp_path / "report.json"
    incomplete = {"root_path": "/tmp/target"}
    path.write_text(json.dumps(incomplete), encoding="utf-8")

    with pytest.raises(CiReportError, match="missing expected"):
        load_ci_report(path)


def test_loads_valid_report(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps(_VALID_REPORT), encoding="utf-8")

    ctx = load_ci_report(path)

    assert ctx.root_path == "/tmp/target"
    assert ctx.language_breakdown == {"python": 3}
    assert ctx.external_dependencies[0].name == "pytest"
    assert ctx.top_level_filenames == ["pyproject.toml"]
