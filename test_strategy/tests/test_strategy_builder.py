from test_strategy.profile_loader import TestEnvironmentSummary
from test_strategy.regression_report_loader import (
    RegressionFileAssessment,
    RegressionReportContext,
)
from test_strategy.strategy_builder import build_strategy


def _file(file="pkg/module.py", tier="low", covered=False, deleted=False, new=False):
    return RegressionFileAssessment(
        file=file,
        is_new_file=new,
        is_deleted_file=deleted,
        overall_risk_tier=tier,
        has_test_coverage=covered,
        flag_count=0,
    )


_FEASIBLE_PROFILE = TestEnvironmentSummary(
    repo_root="/tmp/target", primary_test_framework="pytest", unavailable=[]
)
_INFEASIBLE_PROFILE = TestEnvironmentSummary(
    repo_root="/tmp/target",
    primary_test_framework=None,
    unavailable=["test_framework", "mock_framework"],
)


def test_high_risk_uncovered_file_is_flagged_high_priority():
    ctx = RegressionReportContext(files=[_file(tier="high", covered=False)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert len(report.targets) == 1
    target = report.targets[0]
    assert target.priority == "high"
    assert target.risk_tier == "high"
    assert "overall_risk_tier as high" in target.reason
    assert report.stats.high_priority_count == 1


def test_already_covered_file_is_never_flagged_regardless_of_tier():
    ctx = RegressionReportContext(files=[_file(tier="high", covered=True)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert report.targets == []
    assert report.stats.files_already_covered == 1
    assert report.stats.targets_flagged == 0


def test_low_risk_uncovered_file_is_flagged_low_priority_informational():
    ctx = RegressionReportContext(files=[_file(tier="low", covered=False)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert len(report.targets) == 1
    assert report.targets[0].priority == "low"
    assert "informational" in report.targets[0].reason


def test_deleted_file_is_never_flagged():
    ctx = RegressionReportContext(files=[_file(tier="high", covered=False, deleted=True)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert report.targets == []
    assert report.stats.files_already_covered == 0


def test_targets_sorted_high_before_medium_before_low():
    ctx = RegressionReportContext(
        files=[
            _file(file="low.py", tier="low", covered=False),
            _file(file="high.py", tier="high", covered=False),
            _file(file="medium.py", tier="medium", covered=False),
        ]
    )

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert [t.file for t in report.targets] == ["high.py", "medium.py", "low.py"]


def test_generation_infeasible_when_no_test_framework_detected_never_a_guess():
    ctx = RegressionReportContext(files=[_file(tier="high", covered=False)])

    report = build_strategy(ctx, _INFEASIBLE_PROFILE, "reg.json", "profile.json")

    target = report.targets[0]
    assert target.generation_feasible is False
    assert target.recommended_framework is None
    assert "no test framework was detected" in target.feasibility_note


def test_generation_feasible_names_the_detected_framework():
    ctx = RegressionReportContext(files=[_file(tier="high", covered=False)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    target = report.targets[0]
    assert target.generation_feasible is True
    assert target.recommended_framework == "pytest"
    assert "pytest" in target.feasibility_note


def test_zero_changed_files_warns_and_reports_no_targets():
    ctx = RegressionReportContext(files=[])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert report.targets == []
    assert any("zero changed files" in w for w in report.warnings)


def test_report_carries_repo_root_and_source_paths_through():
    ctx = RegressionReportContext(files=[_file(tier="low", covered=False)])

    report = build_strategy(ctx, _FEASIBLE_PROFILE, "reg.json", "profile.json")

    assert report.repo_root == "/tmp/target"
    assert report.regression_report_path == "reg.json"
    assert report.profile_path == "profile.json"
