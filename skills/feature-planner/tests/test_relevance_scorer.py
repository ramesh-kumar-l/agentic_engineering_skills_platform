from engine.models import CiDependencyGraph, CiModule, CiReportContext
from engine.relevance_scorer import score_relevance


def _ctx():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(
                path="engine/cli.py",
                docstring="Entry point.",
                functions=["main"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/report.py",
                docstring="Builds a report, invoked by the cli wrapper.",
                functions=["build_report"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/unrelated.py",
                docstring="Handles totally different concerns.",
                functions=["do_other_thing"],
                classes=[],
                imports=[],
            ),
        ],
        dependency_graph=CiDependencyGraph(
            fan_in={"engine/cli.py": 3},
            fan_out={"engine/cli.py": 1},
            hotspots=["engine/cli.py"],
        ),
    )


def test_scores_module_matching_task_keywords_higher():
    result = score_relevance("update the cli", _ctx())
    paths = [s.path for s in result.scores]
    assert paths[0] == "engine/cli.py"
    assert "engine/report.py" in paths
    assert "engine/unrelated.py" not in paths


def test_path_match_outweighs_incidental_text_match():
    result = score_relevance("update the cli", _ctx())
    by_path = {s.path: s.score for s in result.scores}
    assert by_path["engine/cli.py"] > by_path["engine/report.py"]


def test_hotspot_and_fan_signals_annotated():
    result = score_relevance("update the cli", _ctx())
    match = next(s for s in result.scores if s.path == "engine/cli.py")
    assert match.is_hotspot is True
    assert match.fan_in == 3
    assert match.fan_out == 1


def test_no_keyword_overlap_produces_no_scores():
    result = score_relevance("xyzxyz qqqqq", _ctx())
    assert result.scores == []


def test_stopwords_and_short_words_excluded_from_keywords():
    result = score_relevance("the a to of is it as by at", _ctx())
    assert result.keywords == []
