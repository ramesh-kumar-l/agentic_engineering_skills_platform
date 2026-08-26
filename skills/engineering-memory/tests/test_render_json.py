import json

from engine.models import MemoryQueryReport, MemoryRecord, RelevanceMatch, ReportStats, StalenessFlag
from engine.render_json import render_json


def test_render_json_round_trips_basic_fields():
    record = MemoryRecord(
        record_id="L1", record_type="limitation", title="t", body="b",
        source_file="f.md", source_line=3,
    )
    match = RelevanceMatch(
        record=record, score=5, matched_keywords=["x"], staleness=StalenessFlag(is_stale=False)
    )
    report = MemoryQueryReport(
        task_description="task", matches=[match],
        stats=ReportStats(records_scanned=1, match_count=1),
    )
    data = json.loads(render_json(report))
    assert data["task_description"] == "task"
    assert data["matches"][0]["record"]["record_id"] == "L1"
    assert data["matches"][0]["score"] == 5
