from engine.models import KnowledgeCaptureReport, KnowledgeCandidate, ReportStats
from engine.render_markdown import render_markdown


def test_render_markdown_no_candidates():
    report = KnowledgeCaptureReport()
    md = render_markdown(report)
    assert "# Engineering Knowledge Capture Report" in md
    assert "None found." in md


def test_render_markdown_includes_candidate_and_priority():
    report = KnowledgeCaptureReport(
        candidates=[
            KnowledgeCandidate(
                pattern_id="decision-we-decided", category="decision",
                matched_text="we decided", description="x", evidence="We decided to ship it.",
                resolved_module_path="engine/scanner.py", is_hotspot=True,
                suggested_capture_priority="HIGH",
            ),
        ],
        stats=ReportStats(candidate_count=1, candidate_count_by_category={"decision": 1},
                           candidate_count_by_priority={"HIGH": 1}),
    )
    md = render_markdown(report)
    assert "[HIGH] decision" in md
    assert "engine/scanner.py" in md
    assert "We decided to ship it." in md


def test_render_markdown_includes_warnings_section():
    report = KnowledgeCaptureReport(warnings=["Narrative text is empty — no candidates can be extracted."])
    md = render_markdown(report)
    assert "## Warnings" in md
