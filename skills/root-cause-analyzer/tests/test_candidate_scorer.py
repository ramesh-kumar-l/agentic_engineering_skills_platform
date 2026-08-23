from engine.candidate_scorer import score_candidates
from engine.models import CiDependencyGraph, CiModule, CiReportContext, StackFrame


def _ctx():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(
                path="engine/cart.py",
                docstring="Cart total computation.",
                functions=["total"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/checkout.py",
                docstring="Checkout flow, calls cart total.",
                functions=["checkout"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/unrelated.py",
                docstring="Handles logging configuration.",
                functions=["do_other_thing"],
                classes=[],
                imports=[],
            ),
        ],
        dependency_graph=CiDependencyGraph(
            fan_in={"engine/cart.py": 3},
            fan_out={"engine/cart.py": 1},
            hotspots=["engine/cart.py"],
        ),
    )


def test_keyword_overlap_scores_matching_module():
    result = score_candidates("the cart total is wrong", _ctx(), [])
    paths = [c.path for c in result.candidates]
    assert "engine/cart.py" in paths
    assert "engine/unrelated.py" not in paths


def test_stack_trace_hit_outranks_keyword_only_match():
    frame = StackFrame(path="engine/checkout.py", line=5, symbol=None, raw_text="")
    result = score_candidates("the cart total is wrong", _ctx(), [frame])
    by_path = {c.path: c for c in result.candidates}
    assert by_path["engine/checkout.py"].evidence_tier == "stack-trace"
    assert by_path["engine/checkout.py"].score > by_path["engine/cart.py"].score


def test_stack_trace_hit_included_even_without_keyword_overlap():
    frame = StackFrame(path="engine/checkout.py", line=5, symbol=None, raw_text="")
    result = score_candidates("xyzxyz qqqqq", _ctx(), [frame])
    paths = [c.path for c in result.candidates]
    assert paths == ["engine/checkout.py"]


def test_hotspot_and_fan_signals_annotated():
    result = score_candidates("the cart total is wrong", _ctx(), [])
    match = next(c for c in result.candidates if c.path == "engine/cart.py")
    assert match.is_hotspot is True
    assert match.fan_in == 3
    assert match.fan_out == 1


def test_no_keyword_overlap_and_no_stack_hit_produces_no_candidates():
    result = score_candidates("xyzxyz qqqqq", _ctx(), [])
    assert result.candidates == []
