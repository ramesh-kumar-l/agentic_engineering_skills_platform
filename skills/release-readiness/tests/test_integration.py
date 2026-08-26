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
@@ -1,2 +1,3 @@
 def bar():
+    print("debug")
     return 1
"""


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(DIFF, str(report_path))

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["files"][0]["structural"]["resolved_module_path"] == "engine/foo.py"

    markdown_output = render_markdown(report)
    assert "Release Readiness Scorecard" in markdown_output
    assert "Overall Verdict" in markdown_output
    assert "recommendation for a human to review" in markdown_output
    assert "Axis 1" in markdown_output
    assert "Axis 2" in markdown_output
    assert "Axis 3" in markdown_output


def test_hygiene_flag_blocks_a_hotspot_covered_file_despite_coverage(tmp_path):
    """A hygiene blocker is absolute — coverage and structural tier cannot
    downgrade it. Mirrors this phase's ADR-016 rule table's first rule."""
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")

    report = build_report(DIFF, str(report_path))
    assert report.files[0].test_coverage.has_coverage is True
    assert report.files[0].structural.is_hotspot is True
    assert report.files[0].readiness_tier == "blocked"
    assert report.overall_verdict == "NOT_READY"
