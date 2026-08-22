"""CLI behavior tests, written up front this phase — Phases 3/4 each found a
zero-CLI-coverage gap via dogfooding a *different* skill's CLI (L10, L13);
adding this file from the start avoids being the next one found that way.
"""

from __future__ import annotations

import io

from engine.cli import main

_CLEAN_CONTENT = "This function computes a running total.\n"


def test_nonexistent_path_exits_nonzero_with_error(capsys):
    exit_code = main(["/no/such/path.txt"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "does not exist" in captured.err


def test_stdin_dash_reads_content(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(_CLEAN_CONTENT))
    exit_code = main(["-", "--action", "Read a file.", "--format", "json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "AUTHORIZE" in captured.out


def test_out_directory_writes_both_report_files(tmp_path):
    content_file = tmp_path / "content.txt"
    content_file.write_text(_CLEAN_CONTENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    exit_code = main([str(content_file), "--action", "Read a file.", "--format", "both", "--out", str(out_dir)])

    assert exit_code == 0
    assert (out_dir / "security-guard-report.json").exists()
    assert (out_dir / "security-guard-report.md").exists()


def test_format_json_only_writes_only_json(tmp_path):
    content_file = tmp_path / "content.txt"
    content_file.write_text(_CLEAN_CONTENT, encoding="utf-8")
    out_dir = tmp_path / "out"

    main([str(content_file), "--action", "Read a file.", "--format", "json", "--out", str(out_dir)])

    assert (out_dir / "security-guard-report.json").exists()
    assert not (out_dir / "security-guard-report.md").exists()


def test_paths_flag_surfaces_sensitive_path_in_output(tmp_path, capsys):
    content_file = tmp_path / "content.txt"
    content_file.write_text(_CLEAN_CONTENT, encoding="utf-8")

    exit_code = main([str(content_file), "--paths", ".env", "--format", "json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "dotenv-file" in captured.out
