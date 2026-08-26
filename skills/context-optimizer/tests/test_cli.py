import json

from engine.cli import main


def _write_ci_report(tmp_path):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({
        "root_path": "/repo",
        "files": [{"path": "engine/scanner.py", "language": "python",
                   "size_bytes": 100, "line_count": 20}],
        "modules": [{"path": "engine/scanner.py", "docstring": "Scans the repo.",
                     "functions": [], "classes": [], "imports": []}],
        "dependency_graph": {},
    }), encoding="utf-8")
    return path


def _write_task(tmp_path, text):
    path = tmp_path / "task.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_cli_exits_nonzero_on_missing_ci_report(tmp_path):
    task = _write_task(tmp_path, "fix the scanner module")
    exit_code = main([str(task), "--ci-report", str(tmp_path / "missing.json")])
    assert exit_code == 1


def test_cli_exits_nonzero_on_missing_task_path(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    exit_code = main([str(tmp_path / "missing.txt"), "--ci-report", str(ci_report)])
    assert exit_code == 1


def test_cli_exits_nonzero_on_negative_budget(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    task = _write_task(tmp_path, "fix the scanner module")
    exit_code = main([str(task), "--ci-report", str(ci_report), "--budget-lines", "-1"])
    assert exit_code == 1


def test_cli_writes_both_formats_to_out_dir(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    task = _write_task(tmp_path, "fix the scanner module")
    out_dir = tmp_path / "out"
    exit_code = main([str(task), "--ci-report", str(ci_report), "--out", str(out_dir)])
    assert exit_code == 0
    assert (out_dir / "context-optimization-report.json").exists()
    assert (out_dir / "context-optimization-report.md").exists()


def test_cli_prints_to_stdout_when_no_out_dir(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path)
    task = _write_task(tmp_path, "fix the scanner module")
    exit_code = main([str(task), "--ci-report", str(ci_report), "--format", "json"])
    assert exit_code == 0
    assert "recommendations" in capsys.readouterr().out


def test_cli_reads_task_from_stdin(tmp_path, monkeypatch, capsys):
    import io
    ci_report = _write_ci_report(tmp_path)
    monkeypatch.setattr("sys.stdin", io.StringIO("fix the scanner module"))
    exit_code = main(["-", "--ci-report", str(ci_report), "--format", "json"])
    assert exit_code == 0
    assert "scanner.py" in capsys.readouterr().out


def test_cli_respects_budget_lines_flag(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path)
    task = _write_task(tmp_path, "fix the scanner module")
    exit_code = main(
        [str(task), "--ci-report", str(ci_report), "--budget-lines", "5", "--format", "json"]
    )
    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["recommendations"][0]["oversized_alone"] is True
