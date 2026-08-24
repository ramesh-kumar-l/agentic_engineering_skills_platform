from engine.models import HygieneFlag, StructuralAssessment, TestCoverageStatus
from engine.readiness_scorer import file_readiness_tier, overall_verdict


def _structural(**overrides) -> StructuralAssessment:
    base = dict(resolved_module_path="engine/foo.py", fan_in=0, fan_out=0, is_hotspot=False)
    base.update(overrides)
    return StructuralAssessment(**base)


def _coverage(covered: bool) -> TestCoverageStatus:
    return TestCoverageStatus(test_coverage_modules=["tests/test_foo.py"] if covered else [])


def _flag() -> list[HygieneFlag]:
    return [HygieneFlag("debug-print-leftover", "debug-leftover", "medium", "engine/foo.py", 1, "d", "print(x)")]


def test_hygiene_flag_is_absolute_blocker_even_with_low_structural_and_coverage():
    tier = file_readiness_tier(_flag(), _structural(fan_in=0), _coverage(True))
    assert tier == "blocked"


def test_high_structural_uncovered_is_blocked():
    tier = file_readiness_tier([], _structural(fan_in=5), _coverage(False))
    assert tier == "blocked"


def test_high_structural_covered_is_needs_review_not_clear():
    tier = file_readiness_tier([], _structural(fan_in=5), _coverage(True))
    assert tier == "needs-review"


def test_medium_structural_covered_is_needs_review():
    tier = file_readiness_tier([], _structural(fan_in=1), _coverage(True))
    assert tier == "needs-review"


def test_medium_structural_uncovered_is_needs_review():
    tier = file_readiness_tier([], _structural(fan_in=1), _coverage(False))
    assert tier == "needs-review"


def test_low_structural_uncovered_is_needs_review():
    tier = file_readiness_tier([], _structural(fan_in=0), _coverage(False))
    assert tier == "needs-review"


def test_low_structural_covered_is_clear():
    tier = file_readiness_tier([], _structural(fan_in=0), _coverage(True))
    assert tier == "clear"


def test_file_readiness_tier_sets_structural_tier_field_as_side_effect():
    assessment = _structural(fan_in=5)
    file_readiness_tier([], assessment, _coverage(True))
    assert assessment.structural_tier == "high"


def test_overall_verdict_not_ready_when_any_file_blocked():
    assert overall_verdict(["clear", "blocked", "needs-review"]) == "NOT_READY"


def test_overall_verdict_ready_with_conditions_when_any_needs_review():
    assert overall_verdict(["clear", "needs-review"]) == "READY_WITH_CONDITIONS"


def test_overall_verdict_ready_when_all_clear():
    assert overall_verdict(["clear", "clear"]) == "READY"


def test_overall_verdict_ready_on_empty_file_list():
    assert overall_verdict([]) == "READY"
