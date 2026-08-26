from engine.pin_checker import classify_pin_status, is_unpinned


def test_missing_version_is_missing():
    assert classify_pin_status(None) == "missing"
    assert classify_pin_status("") == "missing"
    assert classify_pin_status("   ") == "missing"


def test_wildcard_version():
    assert classify_pin_status("*") == "wildcard"
    assert classify_pin_status("1.x") == "wildcard"
    assert classify_pin_status("1.2.x") == "wildcard"


def test_range_version():
    assert classify_pin_status(">=1.2.0") == "range"
    assert classify_pin_status("^1.2.3") == "range"
    assert classify_pin_status("~1.2.3") == "range"
    assert classify_pin_status(">=1.0,<2.0") == "range"
    assert classify_pin_status("!=1.5") == "range"


def test_pinned_version():
    assert classify_pin_status("1.2.3") == "pinned"
    assert classify_pin_status("==1.2.3") == "pinned"
    assert classify_pin_status("===1.2.3") == "pinned"


def test_is_unpinned():
    assert is_unpinned("missing") is True
    assert is_unpinned("wildcard") is True
    assert is_unpinned("range") is True
    assert is_unpinned("pinned") is False
