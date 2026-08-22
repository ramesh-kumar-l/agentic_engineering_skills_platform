from engine.report import build_report

DIFF_TEXT = """diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,1 +1,2 @@
 import os
+password = "hunter2-super-secret"
"""


def test_build_report_basic_shape():
    report = build_report(DIFF_TEXT)
    assert report.stats.files_touched == 1
    assert report.stats.lines_added == 1
    assert len(report.risk_flags) == 1
    assert report.risk_flags[0].pattern_id == "hardcoded-secret"
    assert len(report.files) == 1


def test_build_report_on_empty_diff():
    report = build_report("")
    assert report.stats.files_touched == 0
    assert report.risk_flags == []
    assert report.files == []
