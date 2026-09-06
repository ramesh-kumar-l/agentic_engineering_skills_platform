import json

from scenario_planner.cli import main

_STRATEGY_REPORT = {
    "repo_root": "/tmp/target",
    "targets": [
        {
            "file": "pkg/module.py",
            "priority": "high",
            "reason": "reason text",
            "risk_tier": "high",
            "generation_feasible": True,
            "feasibility_note": "note",
            "recommended_framework": "pytest",
        }
    ],
}

_REGRESSION_REPORT = {
    "files": [{"file": "pkg/module.py", "diff_pattern_flags": []}],
}

_CI_REPORT = {
    "modules": [{"path": "pkg/module.py", "functions": ["foo"], "classes": []}],
}


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_cli_missing_strategy_report_returns_error(capsys, tmp_path):
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)
    ci_path = _write(tmp_path / "ci.json", _CI_REPORT)

    exit_code = main([str(tmp_path / "missing.json"), str(reg_path), str(ci_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_missing_regression_report_returns_error(capsys, tmp_path):
    strategy_path = _write(tmp_path / "strategy.json", _STRATEGY_REPORT)
    ci_path = _write(tmp_path / "ci.json", _CI_REPORT)

    exit_code = main([str(strategy_path), str(tmp_path / "missing.json"), str(ci_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_missing_ci_report_returns_error(capsys, tmp_path):
    strategy_path = _write(tmp_path / "strategy.json", _STRATEGY_REPORT)
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)

    exit_code = main([str(strategy_path), str(reg_path), str(tmp_path / "missing.json")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_writes_report_to_out_dir(tmp_path):
    strategy_path = _write(tmp_path / "strategy.json", _STRATEGY_REPORT)
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)
    ci_path = _write(tmp_path / "ci.json", _CI_REPORT)
    out_dir = tmp_path / "out"

    exit_code = main(
        [str(strategy_path), str(reg_path), str(ci_path), "--out", str(out_dir)]
    )

    assert exit_code == 0
    report_path = out_dir / "scenario-plan-report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["plans"][0]["file"] == "pkg/module.py"


def test_cli_prints_to_stdout_when_no_out(capsys, tmp_path):
    strategy_path = _write(tmp_path / "strategy.json", _STRATEGY_REPORT)
    reg_path = _write(tmp_path / "reg.json", _REGRESSION_REPORT)
    ci_path = _write(tmp_path / "ci.json", _CI_REPORT)

    exit_code = main([str(strategy_path), str(reg_path), str(ci_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["plans"][0]["scenarios"][0]["target_symbol"] == "foo"
