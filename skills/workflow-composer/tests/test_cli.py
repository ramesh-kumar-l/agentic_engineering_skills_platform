import json
from pathlib import Path

from engine.cli import main

_TINY_REPO = Path(__file__).parent / "fixtures" / "tiny-repo"


def test_list_templates_exits_zero(capsys):
    exit_code = main(["--list-templates"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "understand-then-plan" in out
    assert "understand-then-test-plan" in out
    assert "understand-then-optimize-context" in out


def test_missing_template_name_is_an_error():
    assert main([]) == 1


def test_unknown_template_name_is_an_error(tmp_path):
    exit_code = main(["not-a-template", "--repo-path", str(_TINY_REPO), "--dry-run",
                       "--out-dir", str(tmp_path)])
    assert exit_code == 1


def test_missing_repo_path_is_an_error(tmp_path):
    exit_code = main(["understand-then-plan", "--task", "x", "--out-dir", str(tmp_path)])
    assert exit_code == 1


def test_missing_task_without_dry_run_is_an_error(tmp_path):
    exit_code = main(["understand-then-plan", "--repo-path", str(_TINY_REPO),
                       "--out-dir", str(tmp_path)])
    assert exit_code == 1


def test_dry_run_succeeds_and_writes_report(tmp_path):
    exit_code = main(["understand-then-plan", "--repo-path", str(_TINY_REPO),
                       "--dry-run", "--out-dir", str(tmp_path), "--format", "json"])
    assert exit_code == 0
    payload = json.loads((tmp_path / "workflow-run-report.json").read_text(encoding="utf-8"))
    assert payload["template_name"] == "understand-then-plan"
    assert payload["dry_run"] is True
    assert all(step["status"] == "PENDING" for step in payload["step_results"])


def test_dry_run_writes_both_formats_by_default(tmp_path):
    exit_code = main(["understand-then-plan", "--repo-path", str(_TINY_REPO),
                       "--dry-run", "--out-dir", str(tmp_path)])
    assert exit_code == 0
    assert (tmp_path / "workflow-run-report.json").exists()
    assert (tmp_path / "workflow-run-report.md").exists()
