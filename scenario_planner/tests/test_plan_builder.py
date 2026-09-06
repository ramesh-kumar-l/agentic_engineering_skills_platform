from scenario_planner.ci_module_loader import ModuleSummary
from scenario_planner.plan_builder import build_scenario_plan
from scenario_planner.regression_flags_loader import FlagSummary
from scenario_planner.strategy_targets_loader import StrategyReportContext, TargetSummary


def _target(file="pkg/module.py", priority="high", feasible=True, framework="pytest"):
    return TargetSummary(
        file=file,
        priority=priority,
        generation_feasible=feasible,
        recommended_framework=framework,
    )


def test_flag_grounded_scenario_cites_the_flag_description():
    ctx = StrategyReportContext(repo_root="/tmp/target", targets=[_target()])
    flags_by_file = {
        "pkg/module.py": [
            FlagSummary(pattern_id="p1", severity="medium", description="flag description text")
        ]
    }

    report = build_scenario_plan(ctx, flags_by_file, {}, "s.json", "r.json", "c.json")

    plan = report.plans[0]
    assert len(plan.scenarios) == 1
    assert plan.scenarios[0].source == "regression-flag"
    assert plan.scenarios[0].rationale == "flag description text"


def test_structural_scenario_per_function_and_class():
    ctx = StrategyReportContext(repo_root="/tmp/target", targets=[_target()])
    modules = {"pkg/module.py": ModuleSummary(functions=["foo", "bar"], classes=["Baz"])}

    report = build_scenario_plan(ctx, {}, modules, "s.json", "r.json", "c.json")

    plan = report.plans[0]
    assert plan.structural_detail_available is True
    symbols = {s.target_symbol for s in plan.scenarios}
    assert symbols == {"foo", "bar", "Baz"}
    assert all(s.source == "structural-listing" for s in plan.scenarios)


def test_missing_module_and_no_flags_gets_file_level_fallback():
    ctx = StrategyReportContext(repo_root="/tmp/target", targets=[_target()])

    report = build_scenario_plan(ctx, {}, {}, "s.json", "r.json", "c.json")

    plan = report.plans[0]
    assert plan.structural_detail_available is False
    assert len(plan.scenarios) == 1
    assert plan.scenarios[0].source == "file-level-fallback"


def test_missing_module_but_has_flags_does_not_add_fallback():
    ctx = StrategyReportContext(repo_root="/tmp/target", targets=[_target()])
    flags_by_file = {"pkg/module.py": [FlagSummary("p1", "high", "desc")]}

    report = build_scenario_plan(ctx, flags_by_file, {}, "s.json", "r.json", "c.json")

    plan = report.plans[0]
    assert plan.structural_detail_available is False
    assert len(plan.scenarios) == 1
    assert plan.scenarios[0].source == "regression-flag"


def test_priority_and_feasibility_carried_through_from_target():
    ctx = StrategyReportContext(
        repo_root="/tmp/target",
        targets=[_target(priority="low", feasible=False, framework=None)],
    )

    report = build_scenario_plan(ctx, {}, {}, "s.json", "r.json", "c.json")

    plan = report.plans[0]
    assert plan.priority == "low"
    assert plan.generation_feasible is False
    assert plan.recommended_framework is None


def test_zero_targets_warns_and_reports_no_plans():
    ctx = StrategyReportContext(repo_root="/tmp/target", targets=[])

    report = build_scenario_plan(ctx, {}, {}, "s.json", "r.json", "c.json")

    assert report.plans == []
    assert any("zero flagged targets" in w for w in report.warnings)


def test_stats_and_source_paths_are_correct():
    ctx = StrategyReportContext(
        repo_root="/tmp/target",
        targets=[_target(file="a.py"), _target(file="b.py")],
    )
    modules = {"a.py": ModuleSummary(functions=["f"], classes=[])}

    report = build_scenario_plan(ctx, {}, modules, "s.json", "r.json", "c.json")

    assert report.stats.targets_considered == 2
    assert report.stats.targets_with_structural_detail == 1
    assert report.stats.targets_missing_structural_detail == 1
    assert report.stats.scenarios_generated == 2  # 1 structural + 1 fallback
    assert report.test_strategy_report_path == "s.json"
    assert report.regression_report_path == "r.json"
    assert report.ci_report_path == "c.json"
    assert report.repo_root == "/tmp/target"
