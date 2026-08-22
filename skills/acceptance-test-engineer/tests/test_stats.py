from engine.requirement_parser import parse_requirement
from engine.stats import compute_stats
from engine.testability_scanner import scan


def test_sentence_and_word_counts():
    context = parse_requirement("The system must retry once. It must log the retry.")
    flags = scan(context)
    stats = compute_stats(context, flags)
    assert stats.sentence_count == 2
    assert stats.word_count == 10


def test_existing_criteria_markers_counted():
    text = "Given a valid user\nWhen they log in\nThen they see the dashboard"
    context = parse_requirement(text)
    flags = scan(context)
    stats = compute_stats(context, flags)
    assert stats.existing_criteria_markers >= 3


def test_numeric_quantifier_count():
    context = parse_requirement("Retry up to 3 times with a 500ms delay.")
    flags = scan(context)
    stats = compute_stats(context, flags)
    assert stats.numeric_quantifier_count == 2
