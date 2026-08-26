from engine.models import CiFile
from engine.relevance_scorer import score_relevance


def test_no_keywords_scores_zero():
    f = CiFile(path="engine/scanner.py")
    score, matched = score_relevance(f, [])
    assert score == 0
    assert matched == []


def test_path_match_scores_path_weight():
    f = CiFile(path="engine/scanner.py")
    score, matched = score_relevance(f, ["scanner"])
    assert score == 3
    assert matched == ["scanner"]


def test_docstring_match_adds_docstring_weight():
    f = CiFile(path="engine/models.py", docstring="Defines the scanner output schema.")
    score, matched = score_relevance(f, ["scanner"])
    assert score == 2
    assert matched == ["scanner"]


def test_function_name_match_adds_name_weight():
    f = CiFile(path="engine/models.py", functions=["scan_repo"])
    score, matched = score_relevance(f, ["scan"])
    assert score == 2


def test_import_match_adds_import_weight():
    f = CiFile(path="engine/report.py", imports=["engine.scanner"])
    score, matched = score_relevance(f, ["scanner"])
    assert score == 1


def test_same_keyword_matching_multiple_fields_sums_weights():
    f = CiFile(
        path="engine/scanner.py",
        docstring="The scanner walks the tree.",
        functions=["scanner_entrypoint"],
    )
    score, matched = score_relevance(f, ["scanner"])
    assert score == 3 + 2 + 2  # path + docstring + function name
    assert matched == ["scanner"]


def test_keyword_does_not_match_pure_mid_word_substring():
    """A keyword with no token boundary at all around it must not match —
    the protection this scorer still shares with location_resolver.py's
    \\b fix, even though the two use different techniques."""
    f = CiFile(path="engine/location_resolver.py")
    score, matched = score_relevance(f, ["cat"])
    assert score == 0
    assert matched == []


def test_partial_keyword_does_not_match_a_longer_token():
    f = CiFile(path="engine/testability_scanner_utils.py")
    score, matched = score_relevance(f, ["scan"])
    assert score == 0
    assert matched == []


def test_snake_case_component_still_matches_as_its_own_token():
    f = CiFile(path="engine/location_resolver.py")
    score, matched = score_relevance(f, ["resolver"])
    assert score == 3
    assert matched == ["resolver"]


def test_component_of_compound_identifier_matches_disclosed_tradeoff():
    """Deliberately different from location_resolver.py: a keyword that is
    only ONE component of a longer compound filename still matches — the
    disclosed recall-over-precision tradeoff documented in this module's
    docstring and SKILL.md Known Limitations."""
    f = CiFile(path="engine/testability_scanner_utils.py")
    score, matched = score_relevance(f, ["scanner"])
    assert score == 3
    assert matched == ["scanner"]


def test_multiple_keywords_each_contribute():
    f = CiFile(path="engine/budget_selector.py")
    score, matched = score_relevance(f, ["budget", "selector"])
    assert score == 6
    assert set(matched) == {"budget", "selector"}
