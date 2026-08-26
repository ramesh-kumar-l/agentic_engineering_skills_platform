from engine.models import RiskFlag
from engine.stats import compute_stats


def test_empty_flags():
    stats = compute_stats([])
    assert stats.flag_count == 0
    assert stats.flag_count_by_severity == {}
    assert stats.flag_count_by_category == {}


def test_counts_by_severity_and_category():
    flags = [
        RiskFlag("p1", "unpinned-version", "low", "a", "d", "e"),
        RiskFlag("p2", "unpinned-version", "low", "b", "d", "e"),
        RiskFlag("p3", "known-risk-name", "medium", "c", "d", "e"),
    ]
    stats = compute_stats(flags)
    assert stats.flag_count == 3
    assert stats.flag_count_by_severity == {"low": 2, "medium": 1}
    assert stats.flag_count_by_category == {"unpinned-version": 2, "known-risk-name": 1}
