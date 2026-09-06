from scenario_planner.models import (
    ScenarioCandidate,
    ScenarioPlanReport,
    ScenarioPlanStats,
    TargetScenarioPlan,
)


def test_to_dict_and_from_dict_round_trip():
    report = ScenarioPlanReport(
        schema_version="1.0",
        repo_root="/tmp/target",
        test_strategy_report_path="s.json",
        regression_report_path="r.json",
        ci_report_path="c.json",
        stats=ScenarioPlanStats(
            targets_considered=1,
            targets_with_structural_detail=1,
            targets_missing_structural_detail=0,
            scenarios_generated=1,
        ),
        plans=[
            TargetScenarioPlan(
                file="pkg/module.py",
                priority="high",
                generation_feasible=True,
                recommended_framework="pytest",
                structural_detail_available=True,
                scenarios=[
                    ScenarioCandidate(
                        scenario_name="exercise function `foo`",
                        symbol_kind="function",
                        rationale="rationale text",
                        source="structural-listing",
                        target_symbol="foo",
                    )
                ],
            )
        ],
        warnings=["a warning"],
    )

    restored = ScenarioPlanReport.from_dict(report.to_dict())

    assert restored == report


def test_from_dict_ignores_unknown_top_level_keys():
    data = {
        "schema_version": "1.0",
        "repo_root": "/tmp/target",
        "test_strategy_report_path": "s.json",
        "regression_report_path": "r.json",
        "ci_report_path": "c.json",
        "stats": {
            "targets_considered": 0,
            "targets_with_structural_detail": 0,
            "targets_missing_structural_detail": 0,
            "scenarios_generated": 0,
        },
        "plans": [],
        "warnings": [],
        "future_field_from_a_newer_schema_version": "ignored",
    }

    restored = ScenarioPlanReport.from_dict(data)

    assert restored.repo_root == "/tmp/target"
    assert restored.plans == []
