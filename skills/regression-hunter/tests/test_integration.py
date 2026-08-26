import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
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


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(DIFF, str(report_path))

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["files"][0]["structural"]["resolved_module_path"] == "engine/foo.py"

    markdown_output = render_markdown(report)
    assert "Regression Hunter Pre-Decision Report" in markdown_output
    assert "engine/foo.py" in markdown_output
    assert "Axis 1" in markdown_output
    assert "Axis 2" in markdown_output
    assert "Axis 3" in markdown_output


def test_covered_but_flagged_hotspot_file_stays_high_overall(tmp_path):
    """High structural tier + a real diff-pattern flag stays HIGH even
    though the file is genuinely test-covered — coverage alone cannot
    downgrade a hotspot file that also tripped a regression flag (ADR-015's
    rule table: high tier + has_flags -> HIGH regardless of coverage)."""
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(DIFF, str(report_path))
    assert report.files[0].test_coverage.has_coverage is True
    assert report.files[0].overall_risk_tier == "high"
