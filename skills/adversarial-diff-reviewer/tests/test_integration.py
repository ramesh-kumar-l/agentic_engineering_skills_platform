import json

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report

DIFF_TEXT = """diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,1 +1,2 @@
 import os
+token = "do-not-leak-1234567890"
diff --git a/handler.py b/handler.py
--- a/handler.py
+++ b/handler.py
@@ -1,2 +1,4 @@
 try:
     risky()
+except:
+    pass
"""


def test_full_pipeline_produces_valid_json_and_markdown():
    report = build_report(DIFF_TEXT)

    json_output = render_json(report)
    parsed = json.loads(json_output)
    assert parsed["stats"]["files_touched"] == 2
    assert len(parsed["risk_flags"]) == 2

    markdown_output = render_markdown(report)
    assert "Diff Intelligence Report" in markdown_output
    assert "config.py" in markdown_output
    assert "handler.py" in markdown_output


def test_secret_value_never_leaks_into_json_or_markdown():
    report = build_report(DIFF_TEXT)
    json_output = render_json(report)
    markdown_output = render_markdown(report)

    assert "do-not-leak" not in json_output
    assert "do-not-leak" not in markdown_output
