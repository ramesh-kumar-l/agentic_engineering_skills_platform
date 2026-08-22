import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

REQUIREMENT_TEXT = (
    "The upload endpoint should be fast and user-friendly. "
    "It accepts a file from the user."
)


def test_full_pipeline_produces_valid_json_and_markdown():
    report = build_report(REQUIREMENT_TEXT)

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["stats"]["sentence_count"] == 2
    assert len(parsed["testability_flags"]) >= 3

    markdown_output = render_markdown(report)
    assert "Acceptance Testability Report" in markdown_output
    assert "Sentences" in markdown_output


def test_report_never_fabricates_acceptance_criteria():
    report = build_report(REQUIREMENT_TEXT)
    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert "given" not in parsed
    assert "when" not in parsed
    assert "then" not in parsed
