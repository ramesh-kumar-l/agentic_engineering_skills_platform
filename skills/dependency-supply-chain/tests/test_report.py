import json

import pytest
from engine.ci_report_loader import CiReportError
from engine.report import build_report


def _write_ci_report(tmp_path, dependencies):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({"root_path": "/repo", "external_dependencies": dependencies}), encoding="utf-8")
    return path


def test_build_report_hard_fails_on_missing_ci_report(tmp_path):
    with pytest.raises(CiReportError):
        build_report(tmp_path / "missing.json")


def test_build_report_warns_and_requires_review_on_zero_dependencies(tmp_path):
    path = _write_ci_report(tmp_path, [])
    report = build_report(path)
    assert report.warnings
    assert report.suggested_risk_level == "REQUIRES_REVIEW"


def test_build_report_clear_for_clean_pinned_dependencies(tmp_path):
    path = _write_ci_report(tmp_path, [
        {"name": "totally-fine", "version": "1.0.0", "source_file": "requirements.txt"},
    ])
    report = build_report(path)
    assert report.suggested_risk_level == "CLEAR"
    assert report.flags == []
    assert report.surface_area.total_dependencies == 1


def test_build_report_needs_review_on_unpinned_dependency(tmp_path):
    path = _write_ci_report(tmp_path, [
        {"name": "totally-fine", "version": ">=1.0", "source_file": "requirements.txt"},
    ])
    report = build_report(path)
    assert report.suggested_risk_level == "NEEDS_REVIEW"
