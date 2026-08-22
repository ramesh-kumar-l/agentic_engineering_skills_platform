from engine.action_patterns import PATTERNS


def _categories_matched(text):
    return {p.category for p in PATTERNS if p.matches(text)}


def test_production_deploy_matches():
    assert "Production modifications" in _categories_matched("Deploy this change to production tonight.")


def test_destructive_operation_matches():
    assert "Destructive operations" in _categories_matched("We need to delete the stale branch.")


def test_credential_handling_matches():
    assert "Credentials" in _categories_matched("Rotate the API key for the payments service.")


def test_security_control_change_matches():
    assert "Security controls" in _categories_matched("Temporarily disable authentication for the demo.")


def test_database_migration_matches():
    assert "Database migrations" in _categories_matched("Run the migration to add a new column.")


def test_publishing_matches():
    assert "Publishing" in _categories_matched("Push this branch to origin/main.")


def test_publishing_matches_with_an_object_list_between_verb_and_target():
    text = (
        "Push the new Security Context Guard skill files (skills/security-"
        "context-guard/, evaluations/security-context-guard/, project-"
        "memory-bank updates) to the shared origin repository."
    )
    assert "Publishing" in _categories_matched(text)


def test_publishing_does_not_match_push_in_an_unrelated_later_sentence():
    text = "Push the button to submit the form. Separately, review the shared design doc."
    assert "Publishing" not in _categories_matched(text)


def test_external_communication_matches():
    assert "External communications" in _categories_matched("Send the report to the customer via webhook.")


def test_benign_action_matches_nothing():
    assert _categories_matched("Read the README to understand the project layout.") == set()
