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


def test_loads_files_enriched_with_module_metadata(tmp_path):
    path = _write(tmp_path, "report.json", {
        "root_path": "/repo",
        "files": [{"path": "engine/scanner.py", "language": "python",
                   "size_bytes": 100, "line_count": 42}],
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
    assert len(ctx.files) == 1
    f = ctx.files[0]
    assert f.path == "engine/scanner.py"
    assert f.line_count == 42
    assert f.docstring == "Scans things."
    assert f.functions == ["scan"]
    assert ctx.dependency_graph.fan_in["engine/scanner.py"] == 5
    assert "engine/scanner.py" in ctx.dependency_graph.hotspots


def test_file_without_matching_module_gets_empty_structural_profile(tmp_path):
    """A file CI recorded (real line_count) but never parsed as a module
    (e.g. a non-code file, or a parse_error) must still get a CiFile entry
    — not be silently dropped from consideration."""
    path = _write(tmp_path, "report.json", {
        "root_path": "/repo",
        "files": [{"path": "README.md", "language": "unknown",
                   "size_bytes": 500, "line_count": 30}],
        "modules": [],
        "dependency_graph": {},
    })
    ctx = load_ci_report(path)
    assert len(ctx.files) == 1
    f = ctx.files[0]
    assert f.path == "README.md"
    assert f.line_count == 30
    assert f.docstring is None
    assert f.functions == []


def test_missing_dependency_graph_defaults_to_empty(tmp_path):
    path = _write(tmp_path, "report.json", {"root_path": "/repo", "files": [], "modules": []})
    ctx = load_ci_report(path)
    assert ctx.dependency_graph.fan_in == {}
    assert ctx.dependency_graph.hotspots == []
