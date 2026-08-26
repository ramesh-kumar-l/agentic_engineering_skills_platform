from engine.models import DecisionFlag, DecisionOption
from engine.stats import compute_stats


def test_computes_word_option_and_flag_counts():
    options = [DecisionOption(label="Option A", raw_text="use redis")]
    flags = [
        DecisionFlag("no-tradeoff-signal", "unstated-signal", "medium", "desc", ""),
        DecisionFlag("vague-decision-language", "vague-decision", "high", "desc", "just"),
    ]
    stats = compute_stats("Option A: use redis for caching.", options, flags)

    assert stats.word_count == 6
    assert stats.option_count == 1
    assert stats.flag_count == 2
    assert stats.high_severity_flag_count == 1


def test_zero_flags_and_options():
    stats = compute_stats("", [], [])
    assert stats.word_count == 0
    assert stats.option_count == 0
    assert stats.flag_count == 0
    assert stats.high_severity_flag_count == 0
