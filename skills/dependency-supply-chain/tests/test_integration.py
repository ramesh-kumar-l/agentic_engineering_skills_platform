"""End-to-end: a realistic multi-manifest CI report through build_report,
confirming the flags, surface area, and risk level compose correctly."""

import json

from engine.report import build_report


def test_full_pipeline_on_realistic_multi_manifest_input(tmp_path):
    ci_report = tmp_path / "ci-report.json"
    ci_report.write_text(json.dumps({
        "root_path": "/repo",
        "external_dependencies": [
            {"name": "requests", "version": "==2.28.0", "source_file": "requirements.txt"},
            {"name": "requests", "version": ">=2.31", "source_file": "pyproject.toml"},
            {"name": "flask", "version": "*", "source_file": "requirements.txt"},
            {"name": "request", "version": "2.88.0", "source_file": "package.json"},
            {"name": "stable-pkg", "version": "1.0.0", "source_file": "requirements.txt"},
        ],
    }), encoding="utf-8")

    report = build_report(ci_report)

    assert report.surface_area.total_dependencies == 5
    categories = {f.category for f in report.flags}
    assert "duplicate-version" in categories
    assert "wildcard-version" in categories
    assert "known-risk-name" in categories
    assert report.suggested_risk_level == "REQUIRES_REVIEW"  # wildcard is high severity
    assert report.warnings == []  # dependencies were found, no ambiguity
