from engine.keyword_extractor import extract_keywords, tokenize


def test_tokenize_splits_on_underscore_and_path_separators():
    assert tokenize("engine/location_resolver.py") == ["engine", "location", "resolver", "py"]


def test_tokenize_lowercases():
    assert tokenize("ADR-010 Composition") == ["adr", "010", "composition"]


def test_extract_keywords_drops_stopwords_and_short_tokens():
    keywords = extract_keywords("We decided to fix the relevance scorer for it")
    assert "we" not in keywords
    assert "to" not in keywords
    assert "it" not in keywords
    assert "relevance" in keywords
    assert "scorer" in keywords


def test_extract_keywords_deduplicates_preserving_first_occurrence_order():
    keywords = extract_keywords("scanner scanner scanner budget")
    assert keywords == ["scanner", "budget"]


def test_extract_keywords_splits_snake_case_task_terms():
    keywords = extract_keywords("fix location_resolver bug")
    assert "location" in keywords
    assert "resolver" in keywords


def test_empty_description_yields_no_keywords():
    assert extract_keywords("") == []


def test_all_stopword_description_yields_no_keywords():
    assert extract_keywords("the a an of it") == []
