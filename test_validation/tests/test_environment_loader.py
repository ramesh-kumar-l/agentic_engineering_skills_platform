import json

import pytest

from test_validation.environment_loader import ProfileLoadError, load_test_environment_profile


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_loads_primary_framework_from_first_entry(tmp_path):
    path = _write(
        tmp_path / "profile.json",
        {
            "repo_root": "/tmp/target",
            "test_frameworks": [{"name": "pytest", "evidence": []}],
            "unavailable": [],
        },
    )

    summary = load_test_environment_profile(path)

    assert summary.primary_test_framework == "pytest"
    assert summary.repo_root == "/tmp/target"


def test_no_test_frameworks_gives_none(tmp_path):
    path = _write(
        tmp_path / "profile.json",
        {"repo_root": "/tmp/target", "test_frameworks": [], "unavailable": ["pytest"]},
    )

    summary = load_test_environment_profile(path)

    assert summary.primary_test_framework is None
    assert summary.unavailable == ["pytest"]


def test_missing_file_raises_error(tmp_path):
    with pytest.raises(ProfileLoadError):
        load_test_environment_profile(tmp_path / "missing.json")


def test_missing_required_field_raises_error(tmp_path):
    path = _write(tmp_path / "profile.json", {"repo_root": "/tmp/target"})

    with pytest.raises(ProfileLoadError):
        load_test_environment_profile(path)


def test_wrong_type_test_frameworks_raises_typed_error(tmp_path):
    path = _write(
        tmp_path / "profile.json",
        {"repo_root": "/tmp/target", "test_frameworks": "oops", "unavailable": []},
    )

    with pytest.raises(ProfileLoadError, match="must be a list"):
        load_test_environment_profile(path)
