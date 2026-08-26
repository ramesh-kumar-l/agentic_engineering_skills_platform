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
@@ -1,4 +1,1 @@
 def bar():
-    try:
-        return 1
-    except Exception:
-        return None
+    return 1
"""


def _write_ci_report(tmp_path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_resolves_and_scores_file(tmp_path):
    report = build_report(DIFF, _write_ci_report(tmp_path))
    assert len(report.files) == 1
    f = report.files[0]
    assert f.structural.resolved_module_path == "engine/foo.py"
    assert f.structural.is_hotspot is True
    assert f.test_coverage.has_coverage is True
    assert any(fl.pattern_id == "removed-exception-handling" for fl in f.diff_pattern_flags)


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


def test_high_risk_file_warns(tmp_path):
    report = build_report(DIFF, _write_ci_report(tmp_path))
    assert any("HIGH" in w for w in report.warnings)


def test_report_never_fabricates_a_verdict(tmp_path):
    from engine.render_json import render_json

    report = build_report(DIFF, _write_ci_report(tmp_path))
    parsed = json.loads(render_json(report))
    assert "decision" not in parsed
    assert "approved" not in parsed
    assert "safe_to_merge" not in parsed


def test_three_axes_present_as_separate_fields(tmp_path):
    report = build_report(DIFF, _write_ci_report(tmp_path))
    f = report.files[0]
    assert hasattr(f, "diff_pattern_flags")
    assert hasattr(f, "structural")
    assert hasattr(f, "test_coverage")
    assert hasattr(f, "overall_risk_tier")
