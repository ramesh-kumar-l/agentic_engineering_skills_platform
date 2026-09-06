from project_intelligence.models import SCHEMA_VERSION, Finding, TestEnvironmentProfile


def _make_profile(**overrides) -> TestEnvironmentProfile:
    defaults = dict(
        schema_version=SCHEMA_VERSION,
        repo_root="/tmp/target",
        ci_report_path="/tmp/target/report.json",
        primary_language="python",
        language_breakdown={"python": 10},
        build_systems=[Finding(name="python (pyproject.toml)", evidence=["pytest"])],
        test_frameworks=[Finding(name="pytest", evidence=["pytest"])],
        mock_frameworks=[],
        coverage_tools=[],
        unavailable=["mock_framework", "coverage_tool"],
        warnings=[],
    )
    defaults.update(overrides)
    return TestEnvironmentProfile(**defaults)


def test_round_trip_through_dict():
    profile = _make_profile()

    restored = TestEnvironmentProfile.from_dict(profile.to_dict())

    assert restored == profile


def test_from_dict_ignores_unknown_fields():
    data = _make_profile().to_dict()
    data["future_field_not_yet_defined"] = "should be ignored"

    restored = TestEnvironmentProfile.from_dict(data)

    assert not hasattr(restored, "future_field_not_yet_defined")


def test_findings_round_trip_as_finding_objects():
    profile = _make_profile()

    restored = TestEnvironmentProfile.from_dict(profile.to_dict())

    assert all(isinstance(f, Finding) for f in restored.build_systems)
