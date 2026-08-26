from engine.size_estimator import TOKENS_PER_LINE_ESTIMATE, estimate_tokens


def test_estimate_tokens_applies_fixed_multiplier():
    assert estimate_tokens(10) == 10 * TOKENS_PER_LINE_ESTIMATE


def test_estimate_tokens_zero_lines_is_zero():
    assert estimate_tokens(0) == 0


def test_estimate_tokens_never_negative():
    assert estimate_tokens(-5) == 0
