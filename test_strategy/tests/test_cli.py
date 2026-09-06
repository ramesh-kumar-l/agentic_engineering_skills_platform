import json

from test_strategy.cli import main

_REGRESSION_REPORT = {
    "files": [
        {
            "file": "pkg/module.py",
            "is_new_file": False,
            "is_deleted_file": False,
            "overall_risk_tier": "high",
            "diff_pattern_flags": [],
            "test_coverage": {"test_coverage_modules": []},
        }
    ]
}

_PROFILE = {
    "repo_root": "/tmp/target",
    "test_frameworks": [{"name": "pytest", "evidence": ["pytest"], "confidence": "dependency-confirmed"}],
    "unavailable": [],
}


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_cli_missing_regression_report_returns_error(capsys, tmp_path):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)

    exit_code = main([str(tmp_path / "missing.json"), str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_missing_profile_returns_error(capsys, tmp_path):
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)

    exit_code = main([str(reg_path), str(tmp_path / "missing.json")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_writes_report_to_out_dir(tmp_path):
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)
    profile_path = _write(tmp_path / "profile.json", _PROFILE)
    out_dir = tmp_path / "out"

    exit_code = main([str(reg_path), str(profile_path), "--out", str(out_dir)])

    assert exit_code == 0
    report_path = out_dir / "test-strategy-report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["targets"][0]["priority"] == "high"


def test_cli_prints_to_stdout_when_no_out(capsys, tmp_path):
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)
    profile_path = _write(tmp_path / "profile.json", _PROFILE)

    exit_code = main([str(reg_path), str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["targets"][0]["file"] == "pkg/module.py"
