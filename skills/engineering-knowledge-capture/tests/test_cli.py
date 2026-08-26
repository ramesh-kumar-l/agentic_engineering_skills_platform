import json

from engine.cli import main


def _write_ci_report(tmp_path):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({"root_path": "/repo", "modules": []}), encoding="utf-8")
    return path


def _write_narrative(tmp_path, text):
    path = tmp_path / "narrative.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_cli_exits_nonzero_on_missing_ci_report(tmp_path):
    narrative = _write_narrative(tmp_path, "We decided to ship it.")
    exit_code = main([str(narrative), "--ci-report", str(tmp_path / "missing.json")])
    assert exit_code == 1


def test_cli_exits_nonzero_on_missing_narrative_path(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    exit_code = main([str(tmp_path / "missing.txt"), "--ci-report", str(ci_report)])
    assert exit_code == 1


def test_cli_writes_both_formats_to_out_dir(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    narrative = _write_narrative(tmp_path, "We decided to ship it.")
    out_dir = tmp_path / "out"
    exit_code = main([str(narrative), "--ci-report", str(ci_report), "--out", str(out_dir)])
    assert exit_code == 0
    assert (out_dir / "engineering-knowledge-capture-report.json").exists()
    assert (out_dir / "engineering-knowledge-capture-report.md").exists()


def test_cli_prints_to_stdout_when_no_out_dir(tmp_path, capsys):
    ci_report = _write_ci_report(tmp_path)
    narrative = _write_narrative(tmp_path, "We decided to ship it.")
    exit_code = main([str(narrative), "--ci-report", str(ci_report), "--format", "json"])
    assert exit_code == 0
    assert "candidates" in capsys.readouterr().out


def test_cli_reads_narrative_from_stdin(tmp_path, monkeypatch, capsys):
    import io
    ci_report = _write_ci_report(tmp_path)
    monkeypatch.setattr("sys.stdin", io.StringIO("We decided to ship it."))
    exit_code = main(["-", "--ci-report", str(ci_report), "--format", "json"])
    assert exit_code == 0
    assert "decision" in capsys.readouterr().out
