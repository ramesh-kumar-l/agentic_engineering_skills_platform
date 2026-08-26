from engine.risk_patterns import KNOWN_RISK_PATTERNS, match_known_risk


def test_matches_known_risk_name_case_insensitively():
    result = match_known_risk("Request")
    assert result is not None
    assert result.name_lower == "request"


def test_no_match_for_unknown_name():
    assert match_known_risk("totally-unremarkable-package") is None


def test_every_pattern_is_individually_matchable():
    for pattern in KNOWN_RISK_PATTERNS:
        assert match_known_risk(pattern.name_lower) is pattern


def test_matches_are_exact_not_substring():
    # "request" is a known pattern; "requests" (the real, actively-maintained
    # package) must NOT match — this is the same word-boundary-style
    # precision discipline as target_resolver.py's L23 fix elsewhere in the
    # project: an exact-name table, not a substring scan.
    assert match_known_risk("requests") is None
