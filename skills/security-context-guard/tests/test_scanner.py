from engine.scanner import scan_action, scan_content, scan_paths


def test_scan_content_redacts_a_single_secret():
    redacted, secrets, pii = scan_content('api_key = "sk_live_abcdef123456"')
    assert "sk_live_abcdef123456" not in redacted
    assert len(secrets) == 1


def test_scan_content_redacts_every_occurrence_of_a_repeated_pattern():
    text = 'api_key = "sk_live_abcdef123456"\npassword = "hunter2345678"'
    redacted, secrets, pii = scan_content(text)
    assert "sk_live_abcdef123456" not in redacted
    assert "hunter2345678" not in redacted
    assert len(secrets) == 2


def test_scan_content_redacts_pii():
    redacted, secrets, pii = scan_content("Contact: support@example.com")
    assert "support@example.com" not in redacted
    assert len(pii) == 1


def test_scan_content_returns_unmodified_text_when_clean():
    text = "This is a perfectly ordinary sentence about testing."
    redacted, secrets, pii = scan_content(text)
    assert redacted == text
    assert secrets == []
    assert pii == []


def test_scan_paths_flags_sensitive_conventions():
    matches = scan_paths([".env", "engine/report.py"])
    assert len(matches) == 1
    assert matches[0].path == ".env"


def test_scan_action_flags_matching_category():
    flags = scan_action("Deploy this change to production tonight.")
    assert any(f.category == "Production modifications" for f in flags)


def test_scan_action_returns_empty_for_benign_action():
    assert scan_action("Read the README file.") == []
