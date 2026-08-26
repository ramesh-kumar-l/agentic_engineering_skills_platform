from engine.models import StructuralAssessment, TestCoverageStatus
from engine.risk_scorer import overall_risk_tier, structural_tier


def _structural(**overrides) -> StructuralAssessment:
    base = dict(resolved_module_path="engine/foo.py", fan_in=0, fan_out=0, is_hotspot=False)
    base.update(overrides)
    return StructuralAssessment(**base)


def _coverage(covered: bool) -> TestCoverageStatus:
    return TestCoverageStatus(test_coverage_modules=["tests/test_foo.py"] if covered else [])


def test_structural_tier_unresolved_is_low():
    assert structural_tier(StructuralAssessment()) == "low"


def test_structural_tier_hotspot_is_high():
    assert structural_tier(_structural(is_hotspot=True)) == "high"


def test_structural_tier_high_fan_in_is_high():
    assert structural_tier(_structural(fan_in=5)) == "high"


def test_structural_tier_some_fan_in_is_medium():
    assert structural_tier(_structural(fan_in=1)) == "medium"


def test_structural_tier_zero_fan_in_is_low():
    assert structural_tier(_structural(fan_in=0)) == "low"


def test_high_structural_flagged_or_uncovered_stays_high():
    tier = overall_risk_tier(_structural(fan_in=5), _coverage(True), has_flags=True)
    assert tier == "high"
    tier = overall_risk_tier(_structural(fan_in=5), _coverage(False), has_flags=False)
    assert tier == "high"


def test_high_structural_covered_and_flag_free_is_medium():
    tier = overall_risk_tier(_structural(fan_in=5), _coverage(True), has_flags=False)
    assert tier == "medium"


def test_medium_structural_flagged_and_uncovered_escalates_to_high():
    tier = overall_risk_tier(_structural(fan_in=1), _coverage(False), has_flags=True)
    assert tier == "high"


def test_medium_structural_flagged_and_covered_stays_medium():
    tier = overall_risk_tier(_structural(fan_in=1), _coverage(True), has_flags=True)
    assert tier == "medium"


def test_medium_structural_unflagged_and_uncovered_stays_medium():
    tier = overall_risk_tier(_structural(fan_in=1), _coverage(False), has_flags=False)
    assert tier == "medium"


def test_medium_structural_unflagged_and_covered_is_low():
    tier = overall_risk_tier(_structural(fan_in=1), _coverage(True), has_flags=False)
    assert tier == "low"


def test_low_structural_flagged_and_uncovered_escalates_to_medium():
    tier = overall_risk_tier(_structural(fan_in=0), _coverage(False), has_flags=True)
    assert tier == "medium"


def test_low_structural_otherwise_stays_low():
    tier = overall_risk_tier(_structural(fan_in=0), _coverage(True), has_flags=True)
    assert tier == "low"
    tier = overall_risk_tier(_structural(fan_in=0), _coverage(False), has_flags=False)
    assert tier == "low"


def test_overall_risk_tier_sets_structural_tier_field_as_side_effect():
    assessment = _structural(fan_in=5)
    overall_risk_tier(assessment, _coverage(True), has_flags=False)
    assert assessment.structural_tier == "high"
