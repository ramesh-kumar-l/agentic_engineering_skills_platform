"""CLI behavior tests — added in Phase 4 after dogfooding feature-planner
against a real task targeting this CLI surfaced that none of it (stdin
read, --out file writing, nonexistent-path exit code) had test coverage,
the same gap shape as L10 (adversarial-diff-reviewer, Phase 3). See
examples/feature-planner/example-run.md.
"""

from __future__ import annotations

import io

from engine.cli import main

_SIMPLE_REQUIREMENT = "The dashboard should load fast for all users.\n"


def test_nonexistent_path_exits_nonzero_with_error(capsys):
    exit_code = main(["/no/such/path.txt"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "does not exist" in captured.err


def test_stdin_dash_reads_requirement(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(_SIMPLE_REQUIREMENT))
    exit_code = main(["-", "--format", "json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "vague-performance-term" in captured.out


def test_out_directory_writes_both_report_files(tmp_path):
    req_file = tmp_path / "requirement.txt"
    req_file.write_text(_SIMPLE_REQUIREMENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    exit_code = main([str(req_file), "--format", "both", "--out", str(out_dir)])

    assert exit_code == 0
    assert (out_dir / "acceptance-testability-report.json").exists()
    assert (out_dir / "acceptance-testability-report.md").exists()


def test_format_json_only_writes_only_json(tmp_path):
    req_file = tmp_path / "requirement.txt"
    req_file.write_text(_SIMPLE_REQUIREMENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    main([str(req_file), "--format", "json", "--out", str(out_dir)])

    assert (out_dir / "acceptance-testability-report.json").exists()
    assert not (out_dir / "acceptance-testability-report.md").exists()
