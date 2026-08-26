from engine.models import DependencyRecord, DependencySupplyChainReport, RiskFlag
from engine.render_markdown import render_markdown


def test_render_markdown_includes_risk_level_and_dependency():
    report = DependencySupplyChainReport(
        dependencies=[DependencyRecord(name="a", version="1.0.0", source_file="requirements.txt", pin_status="pinned")],
        suggested_risk_level="CLEAR",
    )
    md = render_markdown(report)
    assert "CLEAR" in md
    assert "`a`" in md


def test_render_markdown_lists_flags():
    report = DependencySupplyChainReport(
        flags=[RiskFlag("p", "unpinned-version", "high", "a", "desc", "evidence")],
        suggested_risk_level="REQUIRES_REVIEW",
    )
    md = render_markdown(report)
    assert "HIGH" in md
    assert "desc" in md


def test_render_markdown_handles_no_flags():
    report = DependencySupplyChainReport(suggested_risk_level="CLEAR")
    md = render_markdown(report)
    assert "None found." in md
