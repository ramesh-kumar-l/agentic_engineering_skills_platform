from engine.option_parser import parse_options


def test_parses_explicit_option_markers():
    text = (
        "Option A: Use a shared Redis cache for session storage.\n"
        "Option B: Store sessions in the existing Postgres database.\n"
    )
    options = parse_options(text)
    assert [o.label for o in options] == ["Option A", "Option B"]
    assert "Redis" in options[0].raw_text
    assert "Postgres" in options[1].raw_text


def test_parses_numbered_list_items():
    text = "1. Add a caching layer in front of the API.\n2. Scale the database vertically instead.\n"
    options = parse_options(text)
    assert [o.label for o in options] == ["Item 1", "Item 2"]


def test_parses_lettered_list_items():
    text = "a) Rewrite the module in Rust.\nb) Optimize the existing Python implementation.\n"
    options = parse_options(text)
    assert len(options) == 2


def test_falls_back_to_vs_split_single_line():
    text = "Should we use a message queue vs a direct synchronous call for this?"
    options = parse_options(text)
    assert len(options) == 2
    assert options[0].label == "Alternative 1"
    assert options[1].label == "Alternative 2"


def test_falls_back_to_single_proposed_option_when_no_shape_matches():
    text = "We will add a background worker to process uploads asynchronously."
    options = parse_options(text)
    assert len(options) == 1
    assert options[0].label == "proposed"
    assert options[0].raw_text == text


def test_empty_text_produces_no_options():
    assert parse_options("") == []
    assert parse_options("   \n  ") == []
