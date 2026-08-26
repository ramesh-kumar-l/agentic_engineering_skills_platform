import json

from engine.cli import main


def _write_ci_report(tmp_path):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({"root_path": "/repo", "modules": []}), encoding="utf-8")
    return path


def _write_decisions(tmp_path, text="## ADR-001: Scanner design\nDiscusses the scanner.\n"):
    path = tmp_path / "decisions.md"
    path.write_text(text, encoding="utf-8")
    return path


def _write_limitations(tmp_path, text=""):
    path = tmp_path / "limitations.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_cli_exits_nonzero_on_missing_ci_report(tmp_path):
    decisions = _write_decisions(tmp_path)
    limitations = _write_limitations(tmp_path)
    exit_code = main([
        "--task", "scanner", "--ci-report", str(tmp_path / "missing.json"),
        "--decisions-path", str(decisions), "--limitations-path", str(limitations),
    ])
    assert exit_code == 1


def test_cli_exits_nonzero_on_missing_decisions_path(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    limitations = _write_limitations(tmp_path)
    exit_code = main([
        "--task", "scanner", "--ci-report", str(ci_report),
        "--decisions-path", str(tmp_path / "missing.md"), "--limitations-path", str(limitations),
    ])
    assert exit_code == 1


def test_cli_exits_nonzero_on_missing_limitations_path(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path)
    exit_code = main([
        "--task", "scanner", "--ci-report", str(ci_report),
        "--decisions-path", str(decisions), "--limitations-path", str(tmp_path / "missing.md"),
    ])
    assert exit_code == 1


def test_cli_writes_both_formats_to_out_dir(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path)
    limitations = _write_limitations(tmp_path)
    out_dir = tmp_path / "out"
    exit_code = main([
        "--task", "scanner", "--ci-report", str(ci_report),
        "--decisions-path", str(decisions), "--limitations-path", str(limitations),
        "--out-dir", str(out_dir),
    ])
    assert exit_code == 0
    assert (out_dir / "engineering-memory-report.json").exists()
    assert (out_dir / "engineering-memory-report.md").exists()


def test_cli_prints_to_stdout_when_no_out_dir(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path)
    limitations = _write_limitations(tmp_path)
    exit_code = main([
        "--task", "scanner", "--ci-report", str(ci_report),
        "--decisions-path", str(decisions), "--limitations-path", str(limitations),
        "--format", "json",
    ])
    assert exit_code == 0
    assert "matches" in capsys.readouterr().out


def test_cli_top_n_flag_limits_matches(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path)
    decisions_text = "\n".join(
        f"## ADR-{i:03d}: scanner topic {i}\nBody about scanner.\n" for i in range(1, 6)
    )
    decisions = _write_decisions(tmp_path, decisions_text)
    limitations = _write_limitations(tmp_path)
    exit_code = main([
        "--task", "scanner", "--ci-report", str(ci_report),
        "--decisions-path", str(decisions), "--limitations-path", str(limitations),
        "--format", "json", "--top-n", "2",
    ])
    assert exit_code == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data["matches"]) == 2
