import json
from pathlib import Path

from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cache.py",
            "docstring": "Redis-backed cache layer.",
            "functions": ["get", "set"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {
        "fan_in": {"engine/cache.py": 12},
        "fan_out": {"engine/cache.py": 2},
        "hotspots": ["engine/cache.py"],
    },
}


def _write_report(tmp_path: Path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_assembles_stats_flags_and_impacts(tmp_path):
    report = build_report(
        "Option A: use Redis cache instead of Postgres for sessions. "
        "This trades ops cost for latency and is reversible via rollback. "
        "No new authentication surface is introduced.",
        _write_report(tmp_path),
    )
    assert report.stats.option_count == 1
    assert len(report.option_impacts) == 1
    assert report.option_impacts[0].impacted_modules[0].path == "engine/cache.py"
    assert report.option_impacts[0].blast_radius_tier == "high"


def test_empty_decision_and_no_matches_produce_warnings(tmp_path):
    report = build_report("", _write_report(tmp_path))
    assert any("empty" in w for w in report.warnings)
    assert any("No modules" in w for w in report.warnings)


def test_no_explicit_alternatives_produces_warning(tmp_path):
    report = build_report(
        "We will add a Redis cache in front of the database.", _write_report(tmp_path)
    )
    assert any("No explicit alternatives" in w for w in report.warnings)


def test_high_blast_radius_option_produces_warning(tmp_path):
    report = build_report(
        "Option A: touch the Redis cache module.", _write_report(tmp_path)
    )
    assert any("HIGH" in w for w in report.warnings)
