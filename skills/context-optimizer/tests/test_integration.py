"""End-to-end: a realistic multi-file CI report and task description,
confirming keyword extraction, relevance scoring, structural boosting,
tiering, and budget selection compose correctly through the full
pipeline."""

import json

from engine.report import build_report


def test_full_pipeline_on_realistic_task(tmp_path):
    ci_report = tmp_path / "ci-report.json"
    ci_report.write_text(json.dumps({
        "root_path": "/repo",
        "files": [
            {"path": "engine/relevance_scorer.py", "language": "python",
             "size_bytes": 400, "line_count": 60},
            {"path": "engine/stats.py", "language": "python",
             "size_bytes": 100, "line_count": 15},
            {"path": "engine/unrelated_thing.py", "language": "python",
             "size_bytes": 200, "line_count": 25},
        ],
        "modules": [
            {"path": "engine/relevance_scorer.py",
             "docstring": "Scores one CI file's relevance against a task's keywords.",
             "functions": ["score_relevance"], "classes": [], "imports": []},
            {"path": "engine/stats.py", "docstring": "Report-level statistics.",
             "functions": [], "classes": [], "imports": []},
            {"path": "engine/unrelated_thing.py", "docstring": "Does something else entirely.",
             "functions": [], "classes": [], "imports": []},
        ],
        "dependency_graph": {
            "fan_in": {"engine/relevance_scorer.py": 5, "engine/stats.py": 1},
            "fan_out": {},
            "hotspots": ["engine/relevance_scorer.py"],
        },
    }), encoding="utf-8")

    task = "Improve the relevance scorer's scoring so stats stay accurate."

    report = build_report(task, str(ci_report), budget_lines=100)

    paths = {r.path for r in report.recommendations}
    assert "engine/relevance_scorer.py" in paths
    assert "engine/stats.py" in paths
    assert "engine/unrelated_thing.py" not in paths

    scorer = next(r for r in report.recommendations if r.path == "engine/relevance_scorer.py")
    assert scorer.tier == "CORE"
    assert scorer.is_hotspot is True

    stats = next(r for r in report.recommendations if r.path == "engine/stats.py")
    assert stats.tier == "SUPPORTING"

    assert report.warnings == []
    assert report.stats.candidate_count == 2
