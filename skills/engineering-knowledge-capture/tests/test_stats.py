from engine.models import KnowledgeCandidate
from engine.stats import compute_stats


def _candidate(category, priority):
    return KnowledgeCandidate(
        pattern_id="x", category=category, matched_text="x", description="x",
        evidence="x", suggested_capture_priority=priority,
    )


def test_empty_candidates_produces_zeroed_stats():
    stats = compute_stats([])
    assert stats.candidate_count == 0
    assert stats.candidate_count_by_category == {}
    assert stats.candidate_count_by_priority == {}


def test_counts_by_category_and_priority():
    candidates = [
        _candidate("decision", "HIGH"),
        _candidate("decision", "MEDIUM"),
        _candidate("lesson", "MEDIUM"),
    ]
    stats = compute_stats(candidates)
    assert stats.candidate_count == 3
    assert stats.candidate_count_by_category == {"decision": 2, "lesson": 1}
    assert stats.candidate_count_by_priority == {"HIGH": 1, "MEDIUM": 2}
