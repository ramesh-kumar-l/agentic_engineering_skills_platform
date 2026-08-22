"""CLI behavior tests — added in Phase 3 after dogfooding acceptance-test-
engineer against this CLI's real behavior surfaced that none of it (stdin
read, --out file writing, nonexistent-path exit code) had test coverage. See
examples/acceptance-test-engineer/example-run.md.
"""

from __future__ import annotations

import io

from engine.cli import main

_SIMPLE_DIFF = (
    "diff --git a/f.py b/f.py\n"
    "--- a/f.py\n"
    "+++ b/f.py\n"
    "@@ -1,1 +1,2 @@\n"
    " x = 1\n"
    "+eval(x)\n"
)


def test_nonexistent_path_exits_nonzero_with_error(capsys):
    exit_code = main(["/no/such/path.diff"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "does not exist" in captured.err


def test_stdin_dash_reads_diff(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(_SIMPLE_DIFF))
    exit_code = main(["-", "--format", "json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "dangerous-eval-exec" in captured.out


def test_out_directory_writes_both_report_files(tmp_path):
    diff_file = tmp_path / "change.diff"
    diff_file.write_text(_SIMPLE_DIFF, encoding="utf-8")
    out_dir = tmp_path / "out"

    exit_code = main([str(diff_file), "--format", "both", "--out", str(out_dir)])

    assert exit_code == 0
    assert (out_dir / "diff-report.json").exists()
    assert (out_dir / "diff-report.md").exists()


def test_format_json_only_writes_only_json(tmp_path):
    diff_file = tmp_path / "change.diff"
    diff_file.write_text(_SIMPLE_DIFF, encoding="utf-8")
    out_dir = tmp_path / "out"

    main([str(diff_file), "--format", "json", "--out", str(out_dir)])

    assert (out_dir / "diff-report.json").exists()
    assert not (out_dir / "diff-report.md").exists()
