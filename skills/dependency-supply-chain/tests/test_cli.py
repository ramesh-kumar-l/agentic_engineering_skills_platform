import json

from engine.cli import main


def _write_ci_report(tmp_path, dependencies):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({"root_path": "/repo", "external_dependencies": dependencies}), encoding="utf-8")
    return path


def test_cli_exits_nonzero_on_missing_ci_report(tmp_path, capsys):
    exit_code = main(["--ci-report", str(tmp_path / "missing.json")])
    assert exit_code == 1
    assert "error:" in capsys.readouterr().err


def test_cli_writes_both_formats_to_out_dir(tmp_path):
    ci_report = _write_ci_report(tmp_path, [{"name": "a", "version": "1.0.0", "source_file": "requirements.txt"}])
    out_dir = tmp_path / "out"
    exit_code = main(["--ci-report", str(ci_report), "--out", str(out_dir)])
    assert exit_code == 0
    assert (out_dir / "dependency-supply-chain-report.json").exists()
    assert (out_dir / "dependency-supply-chain-report.md").exists()


def test_cli_prints_to_stdout_when_no_out_dir(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path, [{"name": "a", "version": "1.0.0", "source_file": "requirements.txt"}])
    exit_code = main(["--ci-report", str(ci_report), "--format", "json"])
    assert exit_code == 0
    assert "suggested_risk_level" in capsys.readouterr().out
