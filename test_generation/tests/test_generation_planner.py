from test_generation.generation_planner import NEGATIVE_SLOT_COUNT, build_generation_plan
from test_generation.models import NamingConvention
from test_generation.scenario_loader import ScenarioCandidateSummary, ScenarioPlanContext

_CONVENTION = NamingConvention(pattern="test_*.py", example="test_foo.py", source="inferred")


def _candidate(file="pkg/module.py", symbol="foo", kind="function", source="structural-listing"):
    return ScenarioCandidateSummary(
        file=file,
        target_symbol=symbol,
        symbol_kind=kind,
        scenario_name=f"exercise {kind} `{symbol}`",
        rationale="rationale text",
        source=source,
        recommended_framework="pytest",
    )


def test_one_positive_and_four_negative_slots_per_candidate(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "module.py").write_text("def foo():\n    pass\n", encoding="utf-8")
    ctx = ScenarioPlanContext(repo_root=str(tmp_path), candidates=[_candidate()])

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    spec = report.specs[0]
    assert spec.positive_slot.kind == "positive"
    assert len(spec.negative_slots) == NEGATIVE_SLOT_COUNT
    assert all(s.kind == "negative" for s in spec.negative_slots)
    assert [s.slot_index for s in spec.negative_slots] == list(range(1, NEGATIVE_SLOT_COUNT + 1))


def test_naming_convention_carried_through_untouched(tmp_path):
    ctx = ScenarioPlanContext(repo_root=str(tmp_path), candidates=[_candidate()])

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    assert report.naming_convention == _CONVENTION
    assert report.specs[0].naming_convention == _CONVENTION


def test_scenario_fields_carried_through_verbatim(tmp_path):
    ctx = ScenarioPlanContext(repo_root=str(tmp_path), candidates=[_candidate()])

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    spec = report.specs[0]
    assert spec.scenario_rationale == "rationale text"
    assert spec.scenario_source == "structural-listing"
    assert spec.recommended_framework == "pytest"


def test_source_excerpt_available_tracked_in_stats(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "module.py").write_text("def foo():\n    pass\n", encoding="utf-8")
    ctx = ScenarioPlanContext(
        repo_root=str(tmp_path),
        candidates=[_candidate(), _candidate(file="missing.py", symbol="bar")],
    )

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    assert report.stats.specs_with_source_excerpt == 1
    assert report.specs[0].source_excerpt_available is True
    assert report.specs[1].source_excerpt_available is False


def test_zero_candidates_warns_and_produces_no_specs(tmp_path):
    ctx = ScenarioPlanContext(repo_root=str(tmp_path), candidates=[])

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    assert report.specs == []
    assert any("zero candidate scenarios" in w for w in report.warnings)


def test_stats_and_source_path_correct(tmp_path):
    ctx = ScenarioPlanContext(repo_root=str(tmp_path), candidates=[_candidate(), _candidate(file="b.py")])

    report = build_generation_plan(ctx, _CONVENTION, str(tmp_path), "s.json")

    assert report.stats.scenarios_considered == 2
    assert report.stats.specs_produced == 2
    assert report.stats.negative_slots_requested == 2 * NEGATIVE_SLOT_COUNT
    assert report.scenario_plan_report_path == "s.json"
    assert report.repo_root == str(tmp_path)
