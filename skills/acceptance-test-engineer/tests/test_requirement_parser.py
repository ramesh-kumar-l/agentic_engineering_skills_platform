from engine.requirement_parser import parse_requirement


def test_splits_multiple_sentences_on_one_line():
    context = parse_requirement("The system must log errors. It must retry once.")
    assert [s.text for s in context.sentences] == [
        "The system must log errors.",
        "It must retry once.",
    ]


def test_preserves_bullet_lines_as_distinct_sentences_without_terminal_punctuation():
    text = "Requirements:\n- Fast response\n- Handles invalid input"
    context = parse_requirement(text)
    texts = [s.text for s in context.sentences]
    assert "Fast response" in texts
    assert "Handles invalid input" in texts


def test_numbered_list_bullet_prefix_is_stripped():
    context = parse_requirement("1. Reject empty input")
    assert context.sentences[0].text == "Reject empty input"


def test_blank_lines_produce_no_sentences():
    context = parse_requirement("First line.\n\n\nSecond line.")
    assert len(context.sentences) == 2


def test_empty_text_produces_no_sentences():
    context = parse_requirement("")
    assert context.sentences == []


def test_sentence_indices_are_sequential():
    context = parse_requirement("One. Two. Three.")
    assert [s.index for s in context.sentences] == [0, 1, 2]
