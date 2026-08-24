import json

from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/foo.py",
            "docstring": "Foo helper.",
            "functions": ["bar"],
            "classes": [],
            "imports": [],
        },
        {
            "path": "engine/caller.py",
            "docstring": "Calls foo.",
            "functions": ["main"],
            "classes": [],
            "imports": ["engine.foo"],
        },
        {
            "path": "tests/test_foo.py",
            "docstring": "",
            "functions": ["test_bar"],
            "classes": [],
            "imports": ["engine.foo"],
        },
    ],
    "dependency_graph": {
        "fan_in": {"engine/foo.py": 6},
        "fan_out": {},
        "hotspots": ["engine/foo.py"],
    },
}

DIFF = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
 def bar():
-    return 1
+    return 2
"""

DIFF_WITH_HYGIENE_FLAG = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,1 +1,2 @@
 def bar():
+    print("debug")
"""


def _write_ci_report(tmp_path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_resolves_and_scores_file():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        report = build_report(DIFF, _write_ci_report(Path(tmp)))
        assert len(report.files) == 1
        f = report.files[0]
        assert f.structural.resolved_module_path == "engine/foo.py"
        assert f.structural.is_hotspot is True
        assert f.test_coverage.has_coverage is True


def test_empty_diff_warns(tmp_path):
    report = build_report("", _write_ci_report(tmp_path))
    assert any("empty" in w.lower() for w in report.warnings)
    assert report.files == []


def test_unresolved_files_warn(tmp_path):
    diff = """diff --git a/unknown/nope.py b/unknown/nope.py
--- a/unknown/nope.py
+++ b/unknown/nope.py
@@ -1,1 +1,1 @@
-x = 1
+x = 2
"""
    report = build_report(diff, _write_ci_report(tmp_path))
    assert any("did not resolve" in w.lower() or "none of the changed files" in w.lower() for w in report.warnings)


def test_blocked_file_warns(tmp_path):
    report = build_report(DIFF_WITH_HYGIENE_FLAG, _write_ci_report(tmp_path))
    assert report.overall_verdict == "NOT_READY"
    assert any("BLOCKED" in w for w in report.warnings)


def test_report_never_fabricates_an_authorization_claim(tmp_path):
    from engine.render_json import render_json

    report = build_report(DIFF, _write_ci_report(tmp_path))
    parsed = json.loads(render_json(report))
    assert "authorized" not in parsed
    assert "approved" not in parsed
    assert "released" not in parsed


def test_axes_present_as_separate_fields(tmp_path):
    report = build_report(DIFF, _write_ci_report(tmp_path))
    f = report.files[0]
    assert hasattr(f, "hygiene_flags")
    assert hasattr(f, "structural")
    assert hasattr(f, "test_coverage")
    assert hasattr(f, "regression_evidence")
    assert hasattr(f, "readiness_tier")


def test_optional_reports_absent_by_default(tmp_path):
    report = build_report(DIFF, _write_ci_report(tmp_path))
    assert report.regression_report_composed is False
    assert report.security_report_composed is False
    assert report.files[0].regression_evidence.available is False
    assert report.security_evidence.available is False


def test_optional_regression_report_composed_when_supplied(tmp_path):
    regression_path = tmp_path / "regression-report.json"
    regression_path.write_text(
        json.dumps({"files": [{"file": "engine/foo.py", "overall_risk_tier": "medium", "diff_pattern_flags": []}]}),
        encoding="utf-8",
    )
    report = build_report(
        DIFF, _write_ci_report(tmp_path), regression_report_path=str(regression_path)
    )
    assert report.regression_report_composed is True
    assert report.files[0].regression_evidence.available is True
    assert report.files[0].regression_evidence.overall_risk_tier == "medium"


def test_optional_security_report_composed_when_supplied(tmp_path):
    security_path = tmp_path / "security-report.json"
    security_path.write_text(
        json.dumps({"classification": {"sensitivity": "high", "suggested_verdict": "REQUIRES_HUMAN_APPROVAL"}}),
        encoding="utf-8",
    )
    report = build_report(
        DIFF, _write_ci_report(tmp_path), security_report_path=str(security_path)
    )
    assert report.security_report_composed is True
    assert report.security_evidence.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"
    assert any("REQUIRES_HUMAN_APPROVAL" in w for w in report.warnings)


def test_missing_optional_report_is_a_warning_not_a_failure(tmp_path):
    report = build_report(
        DIFF, _write_ci_report(tmp_path), regression_report_path=str(tmp_path / "nope.json")
    )
    assert report.regression_report_composed is False
    assert any("does not exist" in w for w in report.warnings)
