import json

import pytest

from test_strategy.regression_report_loader import (
    RegressionReportError,
    load_regression_report,
)

_FILE_ENTRY = {
    "file": "pkg/module.py",
    "is_new_file": False,
    "is_deleted_file": False,
    "overall_risk_tier": "high",
    "diff_pattern_flags": [{"pattern_id": "x"}],
    "test_coverage": {"test_coverage_modules": []},
}


def test_missing_file_raises_regression_report_error(tmp_path):
    with pytest.raises(RegressionReportError, match="cannot read"):
        load_regression_report(tmp_path / "does-not-exist.json")


def test_malformed_json_raises_regression_report_error(tmp_path):
    path = tmp_path / "report.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(RegressionReportError, match="cannot read"):
        load_regression_report(path)


def test_missing_files_key_raises_regression_report_error(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps({"stats": {}}), encoding="utf-8")

    with pytest.raises(RegressionReportError, match="missing required 'files' key"):
        load_regression_report(path)


def test_file_entry_missing_field_raises_regression_report_error(tmp_path):
    path = tmp_path / "report.json"
    incomplete = {"file": "pkg/module.py"}
    path.write_text(json.dumps({"files": [incomplete]}), encoding="utf-8")

    with pytest.raises(RegressionReportError, match="missing required field"):
        load_regression_report(path)


def test_loads_valid_report_with_no_coverage(tmp_path):
    path = tmp_path / "report.json"
    path.write_text(json.dumps({"files": [_FILE_ENTRY]}), encoding="utf-8")

    ctx = load_regression_report(path)

    assert len(ctx.files) == 1
    f = ctx.files[0]
    assert f.file == "pkg/module.py"
    assert f.overall_risk_tier == "high"
    assert f.has_test_coverage is False
    assert f.flag_count == 1


def test_loads_valid_report_with_coverage(tmp_path):
    entry = dict(_FILE_ENTRY)
    entry["test_coverage"] = {"test_coverage_modules": ["pkg/tests/test_module.py"]}
    path = tmp_path / "report.json"
    path.write_text(json.dumps({"files": [entry]}), encoding="utf-8")

    ctx = load_regression_report(path)

    assert ctx.files[0].has_test_coverage is True
