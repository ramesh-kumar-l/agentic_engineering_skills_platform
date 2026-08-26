from engine.knowledge_scanner import scan


def test_clean_narrative_produces_no_candidates():
    candidates = scan("Status: all tests passing, no changes this session.")
    assert candidates == []


def test_single_decision_produces_one_candidate():
    candidates = scan("We decided to keep the CLI argument names consistent across skills.")
    assert len(candidates) == 1
    assert candidates[0].category == "decision"
    assert candidates[0].pattern_id == "decision-we-decided"


def test_compounding_narrative_produces_multiple_candidates_not_collapsed():
    text = (
        "We decided to keep the rate limiter in-process rather than extracting "
        "a shared service.\n"
        "Known limitation: this means each replica enforces its own independent "
        "limit, not a global one."
    )
    candidates = scan(text)
    categories = {c.category for c in candidates}
    assert categories == {"decision", "limitation"}
    assert len(candidates) == 2


def test_evidence_is_the_matched_line_not_the_whole_narrative():
    text = "First line is irrelevant context.\nWe learned that retries needed a cap."
    candidates = scan(text)
    assert len(candidates) == 1
    assert "We learned that retries needed a cap." in candidates[0].evidence
    assert "irrelevant" not in candidates[0].evidence


def test_repeated_marker_in_same_category_produces_two_candidates():
    text = "We decided to use JSON.\nLater, we decided to also support Markdown."
    candidates = scan(text)
    assert len(candidates) == 2
    assert all(c.category == "decision" for c in candidates)
