from test_validation.models import ValidationOutcome, ValidationReport, ValidationStats


def test_to_dict_and_from_dict_round_trip():
    report = ValidationReport(
        schema_version="1.0",
        repo_root="/tmp/target",
        generated_tests_dir="/tmp/target/out/generated-tests",
        test_environment_profile_path="profile.json",
        stats=ValidationStats(test_files_considered=1, passed=1, failed=0, timed_out=0),
        outcomes=[
            ValidationOutcome(
                test_file="test_a.py",
                framework="pytest",
                command=["python", "-m", "pytest", "test_a.py", "-q"],
                exit_code=0,
                passed=True,
                timed_out=False,
                stdout_excerpt="1 passed",
                stderr_excerpt="",
                duration_ms=42,
            )
        ],
        warnings=["a warning"],
    )

    restored = ValidationReport.from_dict(report.to_dict())

    assert restored == report


def test_from_dict_ignores_unknown_top_level_keys():
    data = {
        "schema_version": "1.0",
        "repo_root": "/tmp/target",
        "generated_tests_dir": "/tmp/target/out",
        "test_environment_profile_path": "profile.json",
        "stats": {"test_files_considered": 0, "passed": 0, "failed": 0, "timed_out": 0},
        "outcomes": [],
        "warnings": [],
        "future_field_from_a_newer_schema_version": "ignored",
    }

    restored = ValidationReport.from_dict(data)

    assert restored.repo_root == "/tmp/target"
    assert restored.outcomes == []
