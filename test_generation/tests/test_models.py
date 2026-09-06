from test_generation.models import (
    GenerationPlanReport,
    GenerationPlanStats,
    GenerationSlot,
    NamingConvention,
    TargetGenerationSpec,
)


def test_to_dict_and_from_dict_round_trip():
    report = GenerationPlanReport(
        schema_version="1.0",
        repo_root="/tmp/target",
        scenario_plan_report_path="s.json",
        naming_convention=NamingConvention(
            pattern="test_*.py", example="test_foo.py", source="inferred"
        ),
        stats=GenerationPlanStats(
            scenarios_considered=1,
            specs_produced=1,
            specs_with_source_excerpt=1,
            negative_slots_requested=4,
        ),
        specs=[
            TargetGenerationSpec(
                file="pkg/module.py",
                target_symbol="foo",
                symbol_kind="function",
                scenario_name="exercise function `foo`",
                scenario_rationale="rationale text",
                scenario_source="structural-listing",
                recommended_framework="pytest",
                naming_convention=NamingConvention(
                    pattern="test_*.py", example="test_foo.py", source="inferred"
                ),
                source_excerpt="def foo():\n    pass",
                source_excerpt_available=True,
                positive_slot=GenerationSlot(kind="positive", slot_index=0, instruction="do it"),
                negative_slots=[
                    GenerationSlot(kind="negative", slot_index=1, instruction="do it too")
                ],
            )
        ],
        warnings=["a warning"],
    )

    restored = GenerationPlanReport.from_dict(report.to_dict())

    assert restored == report


def test_from_dict_ignores_unknown_top_level_keys():
    data = {
        "schema_version": "1.0",
        "repo_root": "/tmp/target",
        "scenario_plan_report_path": "s.json",
        "naming_convention": {
            "pattern": "test_*.py",
            "example": "test_foo.py",
            "source": "inferred",
        },
        "stats": {
            "scenarios_considered": 0,
            "specs_produced": 0,
            "specs_with_source_excerpt": 0,
            "negative_slots_requested": 0,
        },
        "specs": [],
        "warnings": [],
        "future_field_from_a_newer_schema_version": "ignored",
    }

    restored = GenerationPlanReport.from_dict(data)

    assert restored.repo_root == "/tmp/target"
    assert restored.specs == []
