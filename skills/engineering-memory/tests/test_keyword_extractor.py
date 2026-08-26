from engine.keyword_extractor import extract_keywords, tokenize


def test_tokenize_splits_on_non_alphanumeric():
    assert tokenize("engine/scanner.py") == ["engine", "scanner", "py"]


def test_tokenize_splits_underscores():
    assert tokenize("target_resolver.py") == ["target", "resolver", "py"]


def test_extract_keywords_drops_stopwords_and_short_tokens():
    keywords = extract_keywords("We are fixing the io bug in the scanner module")
    assert "the" not in keywords
    assert "io" not in keywords
    assert "scanner" in keywords
    assert "bug" in keywords


def test_extract_keywords_deduplicates_preserving_order():
    keywords = extract_keywords("scanner scanner module scanner")
    assert keywords == ["scanner", "module"]


def test_extract_keywords_empty_text_returns_empty_list():
    assert extract_keywords("") == []
