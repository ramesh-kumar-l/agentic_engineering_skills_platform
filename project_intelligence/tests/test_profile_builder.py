import json

from project_intelligence.profile_builder import build_profile

_REPORT_WITH_DEPS = {
    "root_path": "/tmp/target",
    "language_breakdown": {"python": 8, "javascript": 2},
    "external_dependencies": [
        {"name": "pytest", "version": "7.0", "source_file": "pyproject.toml"},
        {"name": "pytest-cov", "version": None, "source_file": "pyproject.toml"},
    ],
    "files": [{"path": "pyproject.toml"}, {"path": "src/main.py"}],
}

_REPORT_NO_DEPS = {
    "root_path": "/tmp/target",
    "language_breakdown": {"python": 5},
    "external_dependencies": [],
    "files": [{"path": "pyproject.toml"}],
}


def test_full_profile_with_real_dependencies(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps(_REPORT_WITH_DEPS), encoding="utf-8")

    profile = build_profile(path)

    assert profile.primary_language == "python"
    assert [f.name for f in profile.test_frameworks] == ["pytest"]
    assert [f.name for f in profile.coverage_tools] == ["pytest-cov"]
    assert profile.build_systems[0].confidence == "dependency-confirmed"
    assert "mock_framework" in profile.unavailable
    assert profile.warnings == []


def test_manifest_only_repo_reports_unavailable_and_warns(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps(_REPORT_NO_DEPS), encoding="utf-8")

    profile = build_profile(path)

    assert profile.build_systems[0].confidence == "manifest-only"
    assert set(profile.unavailable) == {"test_framework", "mock_framework", "coverage_tool"}
    assert any("zero external_dependencies" in w for w in profile.warnings)


def test_primary_language_is_most_common(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps(_REPORT_WITH_DEPS), encoding="utf-8")

    profile = build_profile(path)

    assert profile.primary_language == "python"
