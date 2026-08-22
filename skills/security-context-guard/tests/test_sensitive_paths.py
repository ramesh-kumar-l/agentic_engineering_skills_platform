from engine.sensitive_paths import match_sensitive_paths


def test_dotenv_file_matches():
    matches = match_sensitive_paths([".env"])
    assert any(p.pattern_id == "dotenv-file" for _, p in matches)


def test_pem_key_matches():
    matches = match_sensitive_paths(["certs/server.pem"])
    assert any(p.pattern_id == "pem-key" for _, p in matches)


def test_ssh_private_key_matches():
    matches = match_sensitive_paths(["home/user/.ssh/id_rsa"])
    assert any(p.pattern_id == "ssh-private-key" for _, p in matches)


def test_aws_credentials_requires_aws_parent_dir():
    matches = match_sensitive_paths(["home/user/.aws/credentials"])
    assert any(p.pattern_id == "aws-credentials" for _, p in matches)

    matches_elsewhere = match_sensitive_paths(["some/other/dir/credentials"])
    assert not any(p.pattern_id == "aws-credentials" for _, p in matches_elsewhere)


def test_ordinary_source_file_does_not_match():
    matches = match_sensitive_paths(["skills/security-context-guard/engine/report.py"])
    assert matches == []


def test_empty_paths_list_returns_no_matches():
    assert match_sensitive_paths([]) == []
