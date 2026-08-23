from engine.impact_scorer import score_option_impact, score_options
from engine.models import CiDependencyGraph, CiModule, CiReportContext, DecisionOption


def _ci_report():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(
                path="engine/cache.py",
                docstring="Redis-backed cache layer.",
                functions=["get", "set"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/unrelated.py",
                docstring="Handles logging configuration.",
                functions=[],
                classes=[],
                imports=[],
            ),
        ],
        dependency_graph=CiDependencyGraph(
            fan_in={"engine/cache.py": 12},
            fan_out={"engine/cache.py": 2},
            hotspots=["engine/cache.py"],
        ),
    )


def test_scores_matching_module_and_ignores_unrelated_one():
    option = DecisionOption(label="Option A", raw_text="Use Redis cache for session storage.")
    impact = score_option_impact(option, _ci_report())

    paths = [m.path for m in impact.impacted_modules]
    assert "engine/cache.py" in paths
    assert "engine/unrelated.py" not in paths


def test_hotspot_module_produces_high_blast_radius_tier():
    option = DecisionOption(label="Option A", raw_text="Use Redis cache for session storage.")
    impact = score_option_impact(option, _ci_report())

    assert impact.hotspot_count == 1
    assert impact.blast_radius_tier == "high"


def test_no_keyword_match_produces_low_blast_radius_with_no_modules():
    ci_report = CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/unrelated.py", docstring="Handles logging.", functions=[], classes=[], imports=[])
        ],
        dependency_graph=CiDependencyGraph(),
    )
    option = DecisionOption(label="Option A", raw_text="Use Redis cache for session storage.")
    impact = score_option_impact(option, ci_report)

    assert impact.impacted_modules == []
    assert impact.blast_radius_score == 0
    assert impact.blast_radius_tier == "low"


def test_medium_tier_from_nonzero_low_fanin_matches():
    ci_report = CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/cache.py", docstring="Cache helper.", functions=[], classes=[], imports=[])
        ],
        dependency_graph=CiDependencyGraph(fan_in={"engine/cache.py": 3}),
    )
    option = DecisionOption(label="Option A", raw_text="Touch the cache module.")
    impact = score_option_impact(option, ci_report)

    assert impact.blast_radius_score == 4
    assert impact.blast_radius_tier == "medium"


def test_score_options_scores_each_option_independently():
    ci_report = _ci_report()
    options = [
        DecisionOption(label="Option A", raw_text="Use Redis cache."),
        DecisionOption(label="Option B", raw_text="Do nothing structural."),
    ]
    impacts = score_options(options, ci_report)

    assert len(impacts) == 2
    assert impacts[0].option_label == "Option A"
    assert impacts[1].option_label == "Option B"
