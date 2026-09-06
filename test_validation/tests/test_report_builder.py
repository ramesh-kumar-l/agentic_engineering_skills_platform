import pytest

from test_validation.environment_loader import TestEnvironmentSummary
from test_validation.report_builder import build_validation_report
from test_validation.validation_runner import PytestUnavailableError

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


def test_max_test_files_cap_truncates_and_warns(tmp_path):
    for i in range(3):
        (tmp_path / f"test_{i}.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    report = build_validation_report(
        str(tmp_path), _PROFILE, str(tmp_path), "profile.json", max_test_files=2
    )

    assert report.stats.test_files_considered == 2
    assert any("exceeding max_test_files=2" in w for w in report.warnings)


def test_max_test_file_bytes_cap_skips_and_warns(tmp_path):
    small = tmp_path / "test_small.py"
    small.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    big = tmp_path / "test_big.py"
    big.write_text("# padding\n" + ("x = 1\n" * 1000), encoding="utf-8")

    report = build_validation_report(
        str(tmp_path), _PROFILE, str(tmp_path), "profile.json", max_test_file_bytes=100
    )

    assert report.stats.test_files_considered == 1
    assert any("max_test_file_bytes=100" in w for w in report.warnings)


def test_pytest_unavailable_raises_when_py_files_present(tmp_path, monkeypatch):
    (tmp_path / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    monkeypatch.setattr(
        "test_validation.validation_runner.importlib.util.find_spec", lambda name: None
    )

    with pytest.raises(PytestUnavailableError):
        build_validation_report(str(tmp_path), _PROFILE, str(tmp_path), "profile.json")
