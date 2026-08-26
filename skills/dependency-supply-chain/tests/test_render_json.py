import json

from engine.models import DependencyRecord, DependencySupplyChainReport
from engine.render_json import render_json


def test_render_json_round_trips_key_fields():
    report = DependencySupplyChainReport(
        dependencies=[DependencyRecord(name="a", version="1.0.0", source_file="requirements.txt", pin_status="pinned")],
        suggested_risk_level="CLEAR",
    )
    parsed = json.loads(render_json(report))
    assert parsed["suggested_risk_level"] == "CLEAR"
    assert parsed["dependencies"][0]["name"] == "a"
