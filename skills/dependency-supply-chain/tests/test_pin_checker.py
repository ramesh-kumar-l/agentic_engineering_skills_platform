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


def test_maven_range_version():
    assert classify_pin_status("[1.0,2.0)", ecosystem="maven") == "range"
    assert classify_pin_status("[1.5,)", ecosystem="maven") == "range"


def test_maven_exact_version_still_pinned():
    assert classify_pin_status("31.1-jre", ecosystem="maven") == "pinned"


def test_maven_unresolved_property():
    assert classify_pin_status("${guava.version}", ecosystem="maven") == "unresolved"


def test_gradle_dynamic_version():
    assert classify_pin_status("31.+", ecosystem="gradle") == "wildcard"
    assert classify_pin_status("3.1.+", ecosystem="gradle") == "wildcard"


def test_gradle_exact_version_still_pinned():
    assert classify_pin_status("31.1-jre", ecosystem="gradle") == "pinned"


def test_generic_ecosystem_default_unaffected_by_jvm_rules():
    # A Maven-range-shaped string under the default "generic" ecosystem
    # classifies via the original pip/npm-style rules, not the new branch.
    assert classify_pin_status("[1.0,2.0)") == "range"


def test_is_unpinned_includes_unresolved():
    assert is_unpinned("unresolved") is True
