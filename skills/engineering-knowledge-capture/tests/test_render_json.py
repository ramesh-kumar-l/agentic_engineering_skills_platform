import json

from engine.models import KnowledgeCaptureReport, KnowledgeCandidate, ReportStats
from engine.render_json import render_json


def test_render_json_round_trips_basic_fields():
    report = KnowledgeCaptureReport(
        candidates=[
            KnowledgeCandidate(
                pattern_id="decision-we-decided", category="decision",
                matched_text="we decided", description="x", evidence="We decided to ship it.",
                suggested_capture_priority="MEDIUM",
            ),
        ],
        stats=ReportStats(candidate_count=1, candidate_count_by_category={"decision": 1},
                           candidate_count_by_priority={"MEDIUM": 1}),
        warnings=[],
    )
    parsed = json.loads(render_json(report))
    assert parsed["stats"]["candidate_count"] == 1
    assert parsed["candidates"][0]["category"] == "decision"
    assert parsed["warnings"] == []
