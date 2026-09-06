from test_validation.environment_loader import TestEnvironmentSummary
from test_validation.report_builder import build_validation_report

_PROFILE = TestEnvironmentSummary(repo_root="/tmp/target", primary_test_framework="pytest")


def test_zero_files_warns_and_reports_empty(tmp_path):
    report = build_validation_report(str(tmp_path), _PROFILE, str(tmp_path), "profile.json")

    assert report.outcomes == []
    assert any("nothing to validate" in w for w in report.warnings)
    assert report.stats.test_files_considered == 0


def test_mixed_pass_and_fail_stats(tmp_path):
    (tmp_path / "test_pass.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (tmp_path / "test_fail.py").write_text("def test_bad():\n    assert False\n", encoding="utf-8")

    report = build_validation_report(str(tmp_path), _PROFILE, str(tmp_path), "profile.json")

    assert report.stats.test_files_considered == 2
    assert report.stats.passed == 1
    assert report.stats.failed == 1
    assert report.stats.timed_out == 0
    assert report.generated_tests_dir == str(tmp_path)
    assert report.test_environment_profile_path == "profile.json"
