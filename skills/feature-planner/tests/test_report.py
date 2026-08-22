import json
from pathlib import Path

from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cli.py",
            "docstring": "CLI entry point.",
            "functions": ["main"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {"fan_in": {}, "fan_out": {}, "hotspots": []},
}


def _write_report(tmp_path: Path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_assembles_stats_flags_and_relevance(tmp_path):
    report = build_report(
        "Only update the CLI entry point. Verify via tests.", _write_report(tmp_path)
    )
    assert report.stats.word_count > 0
    assert len(report.relevance.scores) == 1
    assert report.relevance.scores[0].path == "engine/cli.py"
    assert report.warnings == []


def test_empty_task_and_no_matches_produce_warnings(tmp_path):
    report = build_report("", _write_report(tmp_path))
    assert any("empty" in w for w in report.warnings)
    assert any("No modules" in w for w in report.warnings)
