from engine.knowledge_patterns import PATTERNS


def test_every_pattern_has_all_four_categories_represented():
    categories = {p.category for p in PATTERNS}
    assert categories == {"decision", "lesson", "limitation", "workaround"}


def test_pattern_ids_are_unique():
    ids = [p.pattern_id for p in PATTERNS]
    assert len(ids) == len(set(ids))


def test_decision_we_decided_matches():
    pattern = next(p for p in PATTERNS if p.pattern_id == "decision-we-decided")
    assert pattern.regex.search("We decided to use Pattern 2 here.")


def test_lesson_turns_out_matches():
    pattern = next(p for p in PATTERNS if p.pattern_id == "lesson-turns-out")
    assert pattern.regex.search("Turns out the bug was elsewhere.")


def test_limitation_known_limitation_matches():
    pattern = next(p for p in PATTERNS if p.pattern_id == "limitation-known-limitation")
    assert pattern.regex.search("This is a known limitation of the scanner.")


def test_workaround_explicit_matches():
    pattern = next(p for p in PATTERNS if p.pattern_id == "workaround-explicit")
    assert pattern.regex.search("We applied a workaround for now.")
