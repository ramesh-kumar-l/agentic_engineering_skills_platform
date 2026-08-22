from engine.secret_patterns import PATTERNS


def _find(pattern_id):
    return next(p for p in PATTERNS if p.pattern_id == pattern_id)


def test_generic_credential_assignment_matches():
    pattern = _find("generic-credential-assignment")
    assert pattern.regex.search('api_key = "sk_live_abcdef123456"')
    assert pattern.regex.search("password: hunter2345")


def test_generic_credential_assignment_ignores_short_values():
    pattern = _find("generic-credential-assignment")
    assert not pattern.regex.search('token = "ab"')


def test_private_key_header_matches():
    pattern = _find("private-key-header")
    assert pattern.regex.search("-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA")


def test_aws_access_key_id_matches():
    pattern = _find("aws-access-key-id")
    assert pattern.regex.search("AKIAABCDEFGHIJKLMNOP")


def test_aws_access_key_id_ignores_shorter_strings():
    pattern = _find("aws-access-key-id")
    assert not pattern.regex.search("AKIASHORT")


def test_bearer_token_matches():
    pattern = _find("bearer-token")
    assert pattern.regex.search("Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5")


def test_no_pattern_matches_clean_text():
    text = "This function computes the sum of two integers and returns it."
    for pattern in PATTERNS:
        assert not pattern.regex.search(text)
