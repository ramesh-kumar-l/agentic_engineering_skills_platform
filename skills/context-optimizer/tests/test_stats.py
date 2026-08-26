from engine.models import FileRelevance
from engine.stats import compute_stats


def test_empty_candidates_yields_zeroed_stats():
    stats = compute_stats([])
    assert stats.candidate_count == 0
    assert stats.candidate_count_by_tier == {}
    assert stats.total_estimated_tokens == 0
    assert stats.oversized_alone_count == 0


def test_counts_by_tier():
    candidates = [
        FileRelevance(path="a.py", relevance_score=6, tier="CORE", estimated_tokens=10),
        FileRelevance(path="b.py", relevance_score=3, tier="SUPPORTING", estimated_tokens=20),
        FileRelevance(path="c.py", relevance_score=3, tier="EXCLUDED", estimated_tokens=30),
    ]
    stats = compute_stats(candidates)
    assert stats.candidate_count == 3
    assert stats.candidate_count_by_tier == {"CORE": 1, "SUPPORTING": 1, "EXCLUDED": 1}


def test_total_estimated_tokens_excludes_excluded_tier():
    candidates = [
        FileRelevance(path="a.py", relevance_score=6, tier="CORE", estimated_tokens=10),
        FileRelevance(path="c.py", relevance_score=3, tier="EXCLUDED", estimated_tokens=30),
    ]
    stats = compute_stats(candidates)
    assert stats.total_estimated_tokens == 10


def test_oversized_alone_count():
    candidates = [
        FileRelevance(path="a.py", relevance_score=6, tier="CORE", oversized_alone=True),
        FileRelevance(path="b.py", relevance_score=3, tier="SUPPORTING", oversized_alone=False),
    ]
    stats = compute_stats(candidates)
    assert stats.oversized_alone_count == 1
