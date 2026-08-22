from engine.planning_scanner import scan
from engine.stats import compute_stats


def test_word_count_and_flag_derived_counts():
    text = "Clean up the module as needed. Only touch the CLI. Verify via tests."
    flags = scan(text)
    stats = compute_stats(text, flags)
    assert stats.word_count == 13
    assert stats.vague_scope_count == 2
    assert stats.weak_modal_count == 0


def test_no_flags_produces_zero_derived_counts():
    text = "Only touch the CLI. Verify via tests."
    flags = scan(text)
    stats = compute_stats(text, flags)
    assert stats.vague_scope_count == 0
    assert stats.weak_modal_count == 0
