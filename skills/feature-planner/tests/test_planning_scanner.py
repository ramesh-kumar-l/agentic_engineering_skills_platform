from engine.planning_scanner import scan


def test_vague_scope_terms_flagged():
    flags = scan("Clean up the module as needed.")
    ids = {f.pattern_id for f in flags}
    assert "vague-scope-catchall" in ids
    assert "vague-scope-cleanup" in ids


def test_weak_goal_modal_flagged():
    flags = scan("We might want to add a flag, only touching the CLI. Verify via tests.")
    ids = {f.pattern_id for f in flags}
    assert "weak-goal-modal" in ids


def test_scope_boundary_absence_flagged_when_missing():
    flags = scan("Add a feature. Test it thoroughly.")
    ids = {f.pattern_id for f in flags}
    assert "no-scope-boundary-signal" in ids


def test_scope_boundary_absence_not_flagged_when_present():
    flags = scan("Only touch the CLI module. Test it thoroughly.")
    ids = {f.pattern_id for f in flags}
    assert "no-scope-boundary-signal" not in ids


def test_verification_absence_flagged_when_missing():
    flags = scan("Only touch the CLI module, nothing else.")
    ids = {f.pattern_id for f in flags}
    assert "no-verification-signal" in ids


def test_well_specified_task_has_no_flags():
    flags = scan(
        "Only add a --verbose flag to the CLI, excluding all other options. "
        "Verify via a new test that acceptance criteria pass."
    )
    assert flags == []
