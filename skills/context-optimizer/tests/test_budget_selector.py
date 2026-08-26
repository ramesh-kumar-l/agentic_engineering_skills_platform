from engine.budget_selector import CORE_THRESHOLD, apply_budget, assign_relevance_tiers
from engine.models import FileRelevance


def test_assign_relevance_tiers_core_threshold():
    core = FileRelevance(path="a.py", relevance_score=CORE_THRESHOLD)
    supporting = FileRelevance(path="b.py", relevance_score=CORE_THRESHOLD - 1)
    assign_relevance_tiers([core, supporting])
    assert core.tier == "CORE"
    assert supporting.tier == "SUPPORTING"


def test_no_budget_leaves_tiers_unchanged():
    c = FileRelevance(path="a.py", relevance_score=1, tier="SUPPORTING", line_count=999999)
    apply_budget([c], None)
    assert c.tier == "SUPPORTING"
    assert c.oversized_alone is False


def test_budget_preserves_core_that_fits():
    c1 = FileRelevance(path="a.py", relevance_score=8, tier="CORE", line_count=50)
    c2 = FileRelevance(path="b.py", relevance_score=6, tier="CORE", line_count=50)
    apply_budget([c1, c2], budget_lines=120)
    assert c1.tier == "CORE"
    assert c2.tier == "CORE"


def test_budget_excludes_lowest_scored_candidate_once_exceeded():
    c1 = FileRelevance(path="a.py", relevance_score=8, tier="CORE", line_count=50)
    c2 = FileRelevance(path="b.py", relevance_score=6, tier="CORE", line_count=50)
    c3 = FileRelevance(path="c.py", relevance_score=3, tier="SUPPORTING", line_count=50)
    apply_budget([c1, c2, c3], budget_lines=120)
    assert c1.tier == "CORE"
    assert c2.tier == "CORE"
    assert c3.tier == "EXCLUDED"
    assert c3.notes


def test_oversized_alone_file_never_excluded_and_is_flagged():
    c = FileRelevance(path="big.py", relevance_score=6, tier="CORE", line_count=500)
    apply_budget([c], budget_lines=100)
    assert c.tier == "CORE"
    assert c.oversized_alone is True
    assert c.notes


def test_oversized_alone_file_still_consumes_budget_and_can_crowd_out_others():
    big = FileRelevance(path="big.py", relevance_score=6, tier="CORE", line_count=500)
    small = FileRelevance(path="small.py", relevance_score=3, tier="SUPPORTING", line_count=10)
    apply_budget([big, small], budget_lines=100)
    assert big.oversized_alone is True
    assert big.tier == "CORE"
    assert small.tier == "EXCLUDED"
