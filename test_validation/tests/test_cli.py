import json

from test_validation.cli import main

_PROFILE = {
    "repo_root": "/tmp/target",
    "test_frameworks": [{"name": "pytest", "evidence": []}],
    "unavailable": [],
}


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_cli_missing_profile_returns_error(capsys, tmp_path):
    exit_code = main([str(tmp_path), str(tmp_path / "missing.json"), str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_missing_generated_tests_dir_returns_error(capsys, tmp_path):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)

    exit_code = main(
        [str(tmp_path / "does-not-exist"), str(profile_path), str(tmp_path)]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_writes_report_to_out_dir(tmp_path):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)
    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    (tests_dir / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    out_dir = tmp_path / "out"

    exit_code = main(
        [str(tests_dir), str(profile_path), str(tmp_path), "--out", str(out_dir)]
    )

    assert exit_code == 0
    report_path = out_dir / "validation-report.json"
    assert report_path.exists()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["stats"]["passed"] == 1


def test_cli_prints_to_stdout_when_no_out(capsys, tmp_path):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)
    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    (tests_dir / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    exit_code = main([str(tests_dir), str(profile_path), str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["stats"]["test_files_considered"] == 1


def test_cli_max_test_files_flag_threads_through(capsys, tmp_path):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)
    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    for i in range(3):
        (tests_dir / f"test_{i}.py").write_text(
            "def test_ok():\n    assert True\n", encoding="utf-8"
        )

    exit_code = main(
        [str(tests_dir), str(profile_path), str(tmp_path), "--max-test-files", "2"]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["stats"]["test_files_considered"] == 2
    assert any("exceeding max_test_files=2" in w for w in data["warnings"])


def test_cli_reports_error_when_pytest_unavailable(capsys, tmp_path, monkeypatch):
    profile_path = _write(tmp_path / "profile.json", _PROFILE)
    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    (tests_dir / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    monkeypatch.setattr(
        "test_validation.validation_runner.importlib.util.find_spec", lambda name: None
    )

    exit_code = main([str(tests_dir), str(profile_path), str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "pytest is not installed" in captured.err
