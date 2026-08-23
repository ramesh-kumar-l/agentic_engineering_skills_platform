from engine.diff_parser import parse_diff
from engine.models import FileRiskAssessment, StructuralAssessment, TestCoverageStatus
from engine.stats import compute_stats

DIFF = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,3 +1,3 @@
 def bar():
-    return 1
+    return 2
"""


def test_computes_line_and_file_counts():
    files = parse_diff(DIFF).files
    assessment = FileRiskAssessment(
        file="engine/foo.py",
        is_new_file=False,
        is_deleted_file=False,
        lines_added=1,
        lines_removed=1,
        diff_pattern_flags=[],
        structural=StructuralAssessment(),
        test_coverage=TestCoverageStatus(),
        overall_risk_tier="low",
    )
    stats = compute_stats(files, [assessment])

    assert stats.files_changed == 1
    assert stats.lines_added == 1
    assert stats.lines_removed == 1
    assert stats.files_added == 0
    assert stats.files_deleted == 0
    assert stats.flag_count == 0
    assert stats.high_risk_file_count == 0


def test_counts_high_risk_files_and_flags():
    files = parse_diff(DIFF).files
    from engine.models import RegressionFlag

    assessment = FileRiskAssessment(
        file="engine/foo.py",
        is_new_file=False,
        is_deleted_file=False,
        lines_added=1,
        lines_removed=1,
        diff_pattern_flags=[RegressionFlag("p1", "diff-pattern", "high", "engine/foo.py", 1, "d", "")],
        structural=StructuralAssessment(),
        test_coverage=TestCoverageStatus(),
        overall_risk_tier="high",
    )
    stats = compute_stats(files, [assessment])

    assert stats.flag_count == 1
    assert stats.high_risk_file_count == 1


def test_counts_added_and_deleted_files():
    new_diff = """diff --git a/new.py b/new.py
--- /dev/null
+++ b/new.py
@@ -0,0 +1,1 @@
+x = 1
"""
    files = parse_diff(new_diff).files
    stats = compute_stats(files, [])
    assert stats.files_added == 1
    assert stats.files_deleted == 0
