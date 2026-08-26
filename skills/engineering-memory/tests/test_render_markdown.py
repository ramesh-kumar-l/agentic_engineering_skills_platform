from engine.models import MemoryQueryReport, MemoryRecord, RelevanceMatch, ReportStats, StalenessFlag
from engine.render_markdown import render_markdown


def test_render_markdown_includes_stale_marker():
    record = MemoryRecord(
        record_id="L1", record_type="limitation", title="Old bug", body="b",
        source_file="f.md", source_line=3,
    )
    match = RelevanceMatch(
        record=record, score=5, staleness=StalenessFlag(is_stale=True, reason="flagged FIXED")
    )
    report = MemoryQueryReport(
        task_description="task", matches=[match],
        stats=ReportStats(records_scanned=1, match_count=1),
    )
    output = render_markdown(report)
    assert "[STALE]" in output
    assert "L1" in output
    assert "flagged FIXED" in output


def test_render_markdown_no_matches_says_none_found():
    report = MemoryQueryReport(task_description="task", matches=[], stats=ReportStats())
    output = render_markdown(report)
    assert "None found." in output


def test_render_markdown_includes_warnings_section():
    report = MemoryQueryReport(
        task_description="task", matches=[], stats=ReportStats(), warnings=["something"]
    )
    output = render_markdown(report)
    assert "## Warnings" in output
    assert "something" in output
