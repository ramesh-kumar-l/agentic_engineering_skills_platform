from engine.models import MemoryRecord
from engine.relevance_scorer import score_relevance


def _record(title, body):
    return MemoryRecord(
        record_id="L1", record_type="limitation", title=title, body=body,
        source_file="x.md", source_line=1,
    )


def test_title_match_weighted_higher_than_body_match():
    title_hit = _record("scanner bug", "unrelated body")
    body_hit = _record("unrelated title", "mentions scanner somewhere")
    title_score, _ = score_relevance(title_hit, ["scanner"], 0)
    body_score, _ = score_relevance(body_hit, ["scanner"], 0)
    assert title_score > body_score


def test_no_keyword_overlap_scores_zero():
    record = _record("something", "else entirely")
    score, matched = score_relevance(record, ["unrelated"], 0)
    assert score == 0
    assert matched == []


def test_module_overlap_boosts_score_independent_of_keywords():
    record = _record("title", "body")
    score, _ = score_relevance(record, [], matched_module_count=2)
    assert score == 4


def test_matched_keywords_lists_each_hit_once():
    record = _record("scanner module", "the scanner runs fine")
    score, matched = score_relevance(record, ["scanner", "module"], 0)
    assert matched == ["scanner", "module"]


def test_keyword_matching_both_title_and_body_scores_higher():
    both = _record("scanner design", "the scanner runs fine")
    title_only = _record("scanner design", "unrelated body entirely")
    both_score, _ = score_relevance(both, ["scanner"], 0)
    title_only_score, _ = score_relevance(title_only, ["scanner"], 0)
    assert both_score > title_only_score
