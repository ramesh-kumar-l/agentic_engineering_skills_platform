import json

from engine.models import ContextOptimizationReport, FileRelevance, ReportStats
from engine.render_json import render_json


def test_render_json_round_trips_core_fields():
    report = ContextOptimizationReport(
        task_keywords=["scanner"],
        recommendations=[FileRelevance(path="engine/scanner.py", relevance_score=6, tier="CORE")],
        stats=ReportStats(candidate_count=1, candidate_count_by_tier={"CORE": 1}),
        warnings=[],
    )
    parsed = json.loads(render_json(report))
    assert parsed["task_keywords"] == ["scanner"]
    assert parsed["recommendations"][0]["path"] == "engine/scanner.py"
    assert parsed["stats"]["candidate_count"] == 1


def test_render_json_empty_report_is_valid_json():
    report = ContextOptimizationReport()
    parsed = json.loads(render_json(report))
    assert parsed["recommendations"] == []
    assert parsed["warnings"] == []
