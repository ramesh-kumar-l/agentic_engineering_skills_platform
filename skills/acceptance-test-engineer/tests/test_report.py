from engine.report import build_report


def test_report_assembles_stats_flags_and_sentences():
    report = build_report("The dashboard must load fast for all users.")
    assert report.stats.sentence_count == 1
    assert len(report.testability_flags) >= 1
    assert len(report.sentences) == 1
    assert report.warnings == []


def test_empty_requirement_produces_warning():
    report = build_report("")
    assert report.sentences == []
    assert any("No sentences parsed" in w for w in report.warnings)
