import json

from test_generation.cli import main

_SCENARIO_REPORT = {
    "repo_root": "/tmp/target",
    "plans": [
        {
            "file": "pkg/module.py",
            "recommended_framework": "pytest",
            "scenarios": [
                {
                    "scenario_name": "exercise function `foo`",
                    "symbol_kind": "function",
                    "rationale": "rationale text",
                    "source": "structural-listing",
                    "target_symbol": "foo",
                }
            ],
        }
    ],
}


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_cli_missing_scenario_report_returns_error(capsys, tmp_path):
    exit_code = main([str(tmp_path / "missing.json"), str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_writes_report_to_out_dir(tmp_path):
    scenario_path = _write(tmp_path / "scenario.json", _SCENARIO_REPORT)
    out_dir = tmp_path / "out"

    exit_code = main([str(scenario_path), str(tmp_path), "--out", str(out_dir)])

    assert exit_code == 0
    report_path = out_dir / "generation-plan-report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["specs"][0]["file"] == "pkg/module.py"


def test_cli_prints_to_stdout_when_no_out(capsys, tmp_path):
    scenario_path = _write(tmp_path / "scenario.json", _SCENARIO_REPORT)

    exit_code = main([str(scenario_path), str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["specs"][0]["target_symbol"] == "foo"


def test_cli_uses_naming_convention_override_file(capsys, tmp_path):
    scenario_path = _write(tmp_path / "scenario.json", _SCENARIO_REPORT)
    override_path = _write(
        tmp_path / "convention.json",
        {"pattern": "*_test.py", "example": "foo_test.py"},
    )

    exit_code = main(
        [str(scenario_path), str(tmp_path), "--naming-convention-file", str(override_path)]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["naming_convention"]["source"] == "override"
    assert data["naming_convention"]["pattern"] == "*_test.py"


def test_cli_missing_naming_convention_override_returns_error(capsys, tmp_path):
    scenario_path = _write(tmp_path / "scenario.json", _SCENARIO_REPORT)

    exit_code = main(
        [
            str(scenario_path),
            str(tmp_path),
            "--naming-convention-file",
            str(tmp_path / "missing-convention.json"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err
