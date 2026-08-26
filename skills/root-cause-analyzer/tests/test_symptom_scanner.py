from engine.symptom_scanner import scan


def test_vague_symptom_terms_flagged():
    flags = scan("It sometimes just stops working randomly.")
    ids = {f.pattern_id for f in flags}
    assert "vague-symptom-catchall" in ids


def test_vague_severity_flagged():
    flags = scan("Something's off, the page acts up. Expected the total to update; instead it stayed 0. Steps to reproduce: add an item. Error: NaN in console.")
    ids = {f.pattern_id for f in flags}
    assert "vague-symptom-severity" in ids


def test_expected_actual_absence_flagged_when_missing():
    flags = scan("The checkout page crashes with an error. Steps to reproduce: click submit.")
    ids = {f.pattern_id for f in flags}
    assert "no-expected-actual-signal" in ids


def test_repro_absence_flagged_when_missing():
    flags = scan("Expected the total to be 10 but got 0, error in console.")
    ids = {f.pattern_id for f in flags}
    assert "no-repro-signal" in ids


def test_error_signal_absence_flagged_when_missing():
    flags = scan("Expected the total to be 10 but got 0. Steps to reproduce: add an item.")
    ids = {f.pattern_id for f in flags}
    assert "no-error-signal" in ids


def test_well_specified_symptom_has_no_flags():
    text = (
        "Expected the cart total to be $10 but got $0 instead. "
        "Steps to reproduce: add one item priced at $10, then open the cart. "
        'Error: TypeError: NaN in console. File "engine/cart.py", line 12, in total'
    )
    flags = scan(text)
    ids = {f.pattern_id for f in flags}
    assert "vague-symptom-catchall" not in ids
    assert "no-expected-actual-signal" not in ids
    assert "no-repro-signal" not in ids
    assert "no-error-signal" not in ids
