from engine.pii_patterns import PATTERNS


def _find(pattern_id):
    return next(p for p in PATTERNS if p.pattern_id == pattern_id)


def test_email_address_matches():
    pattern = _find("email-address")
    assert pattern.regex.search("Contact us at support@example.com for help.")


def test_phone_number_matches():
    pattern = _find("phone-number")
    assert pattern.regex.search("Call me at 555-123-4567 tomorrow.")


def test_ssn_shaped_matches():
    pattern = _find("ssn-shaped")
    assert pattern.regex.search("SSN on file: 123-45-6789")


def test_credit_card_shaped_matches():
    pattern = _find("credit-card-shaped")
    assert pattern.regex.search("Card number 4111 1111 1111 1111 on file")


def test_no_pattern_matches_clean_text():
    text = "The build passed on all three platforms this morning."
    for pattern in PATTERNS:
        assert not pattern.regex.search(text)
