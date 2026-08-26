from engine.decision_scanner import scan


def test_flags_vague_decision_language():
    flags = scan(
        "Option A: just switch to Redis, it's obviously simpler. "
        "Option B: keep Postgres, but that costs more ops time. This is reversible via rollback."
    )
    ids = {f.pattern_id for f in flags}
    assert "vague-decision-language" in ids


def test_flags_missing_alternatives_signal():
    flags = scan("We will add a background worker to process uploads.")
    ids = {f.pattern_id for f in flags}
    assert "no-alternatives-signal" in ids


def test_flags_missing_reversibility_signal():
    flags = scan(
        "Option A: use Redis instead of Postgres for sessions. "
        "This trades operational cost for lower latency."
    )
    ids = {f.pattern_id for f in flags}
    assert "no-reversibility-signal" in ids


def test_flags_missing_tradeoff_signal():
    flags = scan(
        "Option A: use Redis instead of Postgres. This is fully reversible via rollback."
    )
    ids = {f.pattern_id for f in flags}
    assert "no-tradeoff-signal" in ids


def test_flags_missing_security_signal():
    flags = scan(
        "Option A: use Redis instead of Postgres. This is reversible via rollback, "
        "but costs more to operate."
    )
    ids = {f.pattern_id for f in flags}
    assert "no-security-signal" in ids


def test_well_specified_decision_has_no_flags():
    flags = scan(
        "Option A: use Redis instead of Postgres for session storage. "
        "This trades operational cost for lower latency, and is fully "
        "reversible via a rollback migration. No new credentials or "
        "authentication surface is introduced."
    )
    ids = {f.pattern_id for f in flags}
    assert "no-alternatives-signal" not in ids
    assert "no-reversibility-signal" not in ids
    assert "no-tradeoff-signal" not in ids
    assert "no-security-signal" not in ids
