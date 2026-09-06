import json

import pytest

from test_strategy.profile_loader import ProfileLoadError, load_test_environment_profile

_VALID_PROFILE = {
    "repo_root": "/tmp/target",
    "test_frameworks": [{"name": "pytest", "evidence": ["pytest"], "confidence": "dependency-confirmed"}],
    "unavailable": ["mock_framework", "coverage_tool"],
}


def test_missing_file_raises_profile_load_error(tmp_path):
    with pytest.raises(ProfileLoadError, match="cannot read"):
        load_test_environment_profile(tmp_path / "does-not-exist.json")


def test_malformed_json_raises_profile_load_error(tmp_path):
    path = tmp_path / "profile.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(ProfileLoadError, match="cannot read"):
        load_test_environment_profile(path)


def test_missing_required_field_raises_profile_load_error(tmp_path):
    path = tmp_path / "profile.json"
    path.write_text(json.dumps({"repo_root": "/tmp/target"}), encoding="utf-8")

    with pytest.raises(ProfileLoadError, match="missing required field"):
        load_test_environment_profile(path)


def test_loads_profile_with_test_framework(tmp_path):
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(_VALID_PROFILE), encoding="utf-8")

    summary = load_test_environment_profile(path)

    assert summary.repo_root == "/tmp/target"
    assert summary.primary_test_framework == "pytest"
    assert summary.unavailable == ["mock_framework", "coverage_tool"]


def test_loads_profile_with_no_test_framework(tmp_path):
    profile = dict(_VALID_PROFILE)
    profile["test_frameworks"] = []
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    summary = load_test_environment_profile(path)

    assert summary.primary_test_framework is None
