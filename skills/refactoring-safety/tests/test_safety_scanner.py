from engine.safety_scanner import scan


def test_flags_vague_refactor_language():
    flags = scan("This is a trivial rename, shouldn't break anything.")
    ids = [f.pattern_id for f in flags]
    assert "vague-refactor-language" in ids


def test_flags_absence_of_test_plan_signal():
    flags = scan("Rename `foo.py` to `bar.py`.")
    ids = [f.pattern_id for f in flags]
    assert "no-test-plan-signal" in ids


def test_no_flag_when_test_plan_mentioned():
    flags = scan("Rename `foo.py` to `bar.py`. Run the unit tests after.")
    ids = [f.pattern_id for f in flags]
    assert "no-test-plan-signal" not in ids


def test_flags_absence_of_rollback_signal():
    flags = scan("Move `foo.py` into `core/`. Update the callers and run tests.")
    ids = [f.pattern_id for f in flags]
    assert "no-rollback-signal" in ids


def test_no_rollback_flag_when_feature_flag_mentioned():
    flags = scan("Move `foo.py` behind a feature flag so it's reversible.")
    ids = [f.pattern_id for f in flags]
    assert "no-rollback-signal" not in ids


def test_flags_absence_of_caller_update_signal():
    flags = scan("Rename `foo.py`. Run tests. Reversible via git revert.")
    ids = [f.pattern_id for f in flags]
    assert "no-caller-update-signal" in ids


def test_flags_absence_of_verification_signal():
    flags = scan("Rename `foo.py`. Update all call sites. Revert if needed.")
    ids = [f.pattern_id for f in flags]
    assert "no-verification-signal" in ids


def test_fully_specified_text_yields_no_absence_flags():
    text = (
        "Rename `foo.py` to `bar.py`. Update every call site and reference. "
        "Run the unit tests and CI to verify. Reversible via git revert "
        "since this is behind a feature flag."
    )
    flags = scan(text)
    ids = [f.pattern_id for f in flags]
    assert "no-test-plan-signal" not in ids
    assert "no-rollback-signal" not in ids
    assert "no-caller-update-signal" not in ids
    assert "no-verification-signal" not in ids
