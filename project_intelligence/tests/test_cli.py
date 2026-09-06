import json

from project_intelligence.cli import main

_REPORT = {
    "root_path": "/tmp/target",
    "language_breakdown": {"python": 1},
    "external_dependencies": [{"name": "pytest", "version": "7.0", "source_file": "pyproject.toml"}],
    "files": [{"path": "pyproject.toml"}],
}


def test_cli_missing_report_returns_error(capsys, tmp_path):
    exit_code = main([str(tmp_path / "missing.json")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_writes_profile_to_out_dir(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps(_REPORT), encoding="utf-8")
    out_dir = tmp_path / "out"

    exit_code = main([str(report_path), "--out", str(out_dir)])

    assert exit_code == 0
    profile_path = out_dir / "test-environment-profile.json"
    assert profile_path.exists()
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    assert data["primary_language"] == "python"


def test_cli_prints_to_stdout_when_no_out(capsys, tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps(_REPORT), encoding="utf-8")

    exit_code = main([str(report_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["primary_language"] == "python"
