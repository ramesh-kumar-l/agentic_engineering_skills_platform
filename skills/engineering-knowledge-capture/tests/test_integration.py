"""End-to-end: a realistic multi-category narrative composed with a real-
shaped CI report, confirming candidates, location resolution, and priority
scoring compose correctly through the full pipeline."""

import json

from engine.report import build_report


def test_full_pipeline_on_realistic_narrative(tmp_path):
    ci_report = tmp_path / "ci-report.json"
    ci_report.write_text(json.dumps({
        "root_path": "/repo",
        "modules": [
            {"path": "engine/target_resolver.py", "docstring": None,
             "functions": [], "classes": [], "imports": []},
            {"path": "engine/stats.py", "docstring": None,
             "functions": [], "classes": [], "imports": []},
        ],
        "dependency_graph": {
            "fan_in": {"engine/target_resolver.py": 6, "engine/stats.py": 1},
            "fan_out": {},
            "hotspots": ["engine/target_resolver.py"],
        },
    }), encoding="utf-8")

    narrative = (
        "We decided to fix target_resolver.py's substring-collision bug across "
        "all three copies rather than leaving it disclosed a fourth time.\n"
        "Turns out stats.py needed no changes at all.\n"
        "As a workaround, we temporarily skipped the fourth copy pending review."
    )

    report = build_report(narrative, str(ci_report))

    assert report.stats.candidate_count == 3
    categories = {c.category for c in report.candidates}
    assert categories == {"decision", "lesson", "workaround"}

    decision = next(c for c in report.candidates if c.category == "decision")
    assert decision.resolved_module_path == "engine/target_resolver.py"
    assert decision.suggested_capture_priority == "HIGH"

    lesson = next(c for c in report.candidates if c.category == "lesson")
    assert lesson.resolved_module_path == "engine/stats.py"
    assert lesson.suggested_capture_priority == "MEDIUM"

    assert report.warnings == []
