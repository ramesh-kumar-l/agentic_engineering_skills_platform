from engine.models import ContextOptimizationReport, FileRelevance, ReportStats
from engine.render_markdown import render_markdown


def test_render_markdown_includes_warnings():
    report = ContextOptimizationReport(warnings=["Task description is empty."])
    md = render_markdown(report)
    assert "Task description is empty." in md
    assert "## Warnings" in md


def test_render_markdown_lists_recommendations_with_tier_and_score():
    report = ContextOptimizationReport(
        task_keywords=["scanner"],
        recommendations=[
            FileRelevance(
                path="engine/scanner.py", relevance_score=6, tier="CORE",
                is_hotspot=True, matched_keywords=["scanner"], estimated_tokens=160,
                line_count=20,
            )
        ],
        stats=ReportStats(candidate_count=1, candidate_count_by_tier={"CORE": 1},
                           total_estimated_tokens=160),
    )
    md = render_markdown(report)
    assert "engine/scanner.py" in md
    assert "CORE" in md
    assert "hotspot" in md
    assert "160" in md


def test_render_markdown_no_recommendations_says_none_found():
    report = ContextOptimizationReport()
    md = render_markdown(report)
    assert "None found." in md


def test_render_markdown_flags_oversized_alone_note():
    report = ContextOptimizationReport(
        recommendations=[
            FileRelevance(
                path="big.py", relevance_score=6, tier="CORE", oversized_alone=True,
                notes=["This file's own line count exceeds the budget alone"],
            )
        ],
        stats=ReportStats(candidate_count=1, oversized_alone_count=1),
    )
    md = render_markdown(report)
    assert "OVERSIZED ALONE" in md
    assert "exceeds the budget alone" in md
