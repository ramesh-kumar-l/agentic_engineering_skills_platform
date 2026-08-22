from engine.requirement_parser import parse_requirement
from engine.testability_scanner import scan


def test_vague_performance_term_flagged():
    context = parse_requirement("The dashboard must load fast for all users.")
    flags = scan(context)
    assert any(f.pattern_id == "vague-performance-term" for f in flags)


def test_weak_modal_should_flagged():
    context = parse_requirement("The API should return a 404 for unknown IDs.")
    flags = scan(context)
    assert any(f.pattern_id == "weak-modal-should" for f in flags)


def test_no_error_handling_signal_flagged_when_absent():
    context = parse_requirement("The form accepts a username and a password.")
    flags = scan(context)
    assert any(f.pattern_id == "no-error-handling-signal" for f in flags)


def test_no_error_handling_signal_not_flagged_when_present():
    context = parse_requirement("The form rejects an invalid username with an error.")
    flags = scan(context)
    assert not any(f.pattern_id == "no-error-handling-signal" for f in flags)


def test_no_boundary_signal_flagged_when_no_numbers_present():
    context = parse_requirement("Users can upload files of a reasonable size.")
    flags = scan(context)
    assert any(f.pattern_id == "no-boundary-signal" for f in flags)


def test_well_specified_requirement_produces_no_flags():
    context = parse_requirement(
        "The API must reject any upload larger than 10 MB with HTTP 413 "
        "and must return HTTP 201 for uploads between 1 byte and 10 MB."
    )
    flags = scan(context)
    assert flags == []


def test_whole_document_flags_have_no_sentence_index():
    context = parse_requirement("The form accepts a username and a password.")
    flags = scan(context)
    absence_flags = [f for f in flags if f.pattern_id == "no-error-handling-signal"]
    assert absence_flags[0].sentence_index is None
