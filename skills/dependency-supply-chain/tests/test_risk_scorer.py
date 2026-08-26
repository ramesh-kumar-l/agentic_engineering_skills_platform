from engine.models import RiskFlag
from engine.risk_scorer import compute_risk_level


def _flag(severity: str) -> RiskFlag:
    return RiskFlag(
        pattern_id="p", category="c", severity=severity,
        dependency_name="dep", description="d", evidence="e",
    )


def test_clear_when_no_flags_and_dependencies_present():
    assert compute_risk_level([], dependency_count=3, ci_warnings=[]) == "CLEAR"


def test_requires_review_on_high_severity_flag():
    assert compute_risk_level([_flag("high")], dependency_count=1, ci_warnings=[]) == "REQUIRES_REVIEW"


def test_needs_review_on_medium_severity_flag():
    assert compute_risk_level([_flag("medium")], dependency_count=1, ci_warnings=[]) == "NEEDS_REVIEW"


def test_needs_review_on_low_severity_flag():
    assert compute_risk_level([_flag("low")], dependency_count=1, ci_warnings=[]) == "NEEDS_REVIEW"


def test_fails_closed_to_requires_review_on_zero_dependencies():
    assert compute_risk_level([], dependency_count=0, ci_warnings=[]) == "REQUIRES_REVIEW"


def test_fails_closed_to_requires_review_on_ci_warnings():
    assert compute_risk_level([], dependency_count=3, ci_warnings=["something ambiguous"]) == "REQUIRES_REVIEW"
