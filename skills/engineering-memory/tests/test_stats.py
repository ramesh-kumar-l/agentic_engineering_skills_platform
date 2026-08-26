from engine.models import MemoryRecord, RecordStatus, RelevanceMatch
from engine.stats import compute_stats


def _record(record_type, status=RecordStatus.ACTIVE):
    return MemoryRecord(
        record_id="X", record_type=record_type, title="t", body="b",
        source_file="f", source_line=1, status=status,
    )


def test_records_scanned_by_type():
    records = [_record("decision"), _record("limitation"), _record("limitation")]
    stats = compute_stats(records, [])
    assert stats.records_scanned == 3
    assert stats.records_scanned_by_type == {"decision": 1, "limitation": 2}


def test_match_count_by_status():
    records = [_record("decision")]
    match = RelevanceMatch(record=records[0], score=5)
    stats = compute_stats(records, [match])
    assert stats.match_count == 1
    assert stats.match_count_by_status == {"ACTIVE": 1}


def test_empty_inputs_all_zero():
    stats = compute_stats([], [])
    assert stats.records_scanned == 0
    assert stats.match_count == 0
    assert stats.records_scanned_by_type == {}
    assert stats.match_count_by_status == {}
