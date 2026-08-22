from engine.classification import classify
from engine.models import ActionFlag, PiiMatch, SecretMatch, SensitivePathMatch


def test_no_signal_and_clear_action_authorizes():
    result = classify([], [], [], [], action_text="Read the README file.", content_text="Nothing sensitive here.")
    assert result.sensitivity == "low"
    assert result.suggested_verdict == "AUTHORIZE"
    assert result.uncertain is False


def test_empty_input_authorizes_with_none_sensitivity():
    result = classify([], [], [], [], action_text="Read the README file.", content_text="")
    assert result.sensitivity == "none"
    assert result.suggested_verdict == "AUTHORIZE"


def test_secret_match_forces_high_sensitivity_and_approval():
    secret = SecretMatch(pattern_id="generic-credential-assignment", severity="high", description="d")
    result = classify([secret], [], [], [], action_text="Read a file.", content_text="api_key = ...")
    assert result.sensitivity == "high"
    assert result.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"


def test_pii_match_forces_medium_sensitivity_and_approval():
    pii = PiiMatch(pattern_id="email-address", category="email", description="d")
    result = classify([], [pii], [], [], action_text="Read a file.", content_text="contact: a@b.com")
    assert result.sensitivity == "medium"
    assert result.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"


def test_sensitive_path_forces_medium_sensitivity_and_approval():
    path_match = SensitivePathMatch(path=".env", pattern_id="dotenv-file", description="d")
    result = classify([], [], [path_match], [], action_text="Read a file.", content_text="")
    assert result.sensitivity == "medium"
    assert result.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"


def test_high_risk_action_forces_approval_even_with_no_data_sensitivity():
    flag = ActionFlag(pattern_id="publishing", category="Publishing", description="d", matched_text="push")
    result = classify([], [], [], [flag], action_text="Push this branch to origin.", content_text="")
    assert result.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"


def test_missing_action_description_is_uncertain_and_fails_closed():
    result = classify([], [], [], [], action_text="", content_text="Some ordinary content.")
    assert result.uncertain is True
    assert result.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"
    assert any("no action description" in e.lower() for e in result.evidence)
