from test_strategy.models import (
    TestStrategyReport,
    TestStrategyStats,
    TestTarget,
)


def test_to_dict_and_from_dict_round_trip():
    report = TestStrategyReport(
        schema_version="1.0",
        repo_root="/tmp/target",
        regression_report_path="reg.json",
        profile_path="profile.json",
        stats=TestStrategyStats(
            files_considered=2,
            files_already_covered=1,
            targets_flagged=1,
            high_priority_count=1,
            medium_priority_count=0,
            low_priority_count=0,
        ),
        targets=[
            TestTarget(
                file="pkg/module.py",
                priority="high",
                reason="reason text",
                risk_tier="high",
                generation_feasible=True,
                feasibility_note="a test framework (pytest) was detected",
                recommended_framework="pytest",
            )
        ],
        warnings=["a warning"],
    )

    restored = TestStrategyReport.from_dict(report.to_dict())

    assert restored == report


def test_from_dict_ignores_unknown_top_level_keys():
    data = {
        "schema_version": "1.0",
        "repo_root": "/tmp/target",
        "regression_report_path": "reg.json",
        "profile_path": "profile.json",
        "stats": {
            "files_considered": 0,
            "files_already_covered": 0,
            "targets_flagged": 0,
            "high_priority_count": 0,
            "medium_priority_count": 0,
            "low_priority_count": 0,
        },
        "targets": [],
        "warnings": [],
        "future_field_from_a_newer_schema_version": "ignored",
    }

    restored = TestStrategyReport.from_dict(data)

    assert restored.repo_root == "/tmp/target"
    assert restored.targets == []
