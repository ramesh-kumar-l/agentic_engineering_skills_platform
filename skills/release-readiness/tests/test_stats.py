from engine.diff_parser import parse_diff
from engine.models import FileReadinessAssessment, HygieneFlag, StructuralAssessment, TestCoverageStatus
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
    assessment = FileReadinessAssessment(
        file="engine/foo.py",
        is_new_file=False,
        is_deleted_file=False,
        lines_added=1,
        lines_removed=1,
        hygiene_flags=[],
        structural=StructuralAssessment(),
        test_coverage=TestCoverageStatus(),
        readiness_tier="clear",
    )
    stats = compute_stats(files, [assessment])

    assert stats.files_changed == 1
    assert stats.lines_added == 1
    assert stats.lines_removed == 1
    assert stats.files_added == 0
    assert stats.files_deleted == 0
    assert stats.hygiene_flag_count == 0
    assert stats.blocked_file_count == 0
    assert stats.needs_review_file_count == 0


def test_counts_blocked_and_needs_review_files_and_flags():
    files = parse_diff(DIFF).files
    blocked = FileReadinessAssessment(
        file="engine/foo.py",
        is_new_file=False,
        is_deleted_file=False,
        lines_added=1,
        lines_removed=1,
        hygiene_flags=[HygieneFlag("p1", "debug-leftover", "medium", "engine/foo.py", 1, "d", "")],
        structural=StructuralAssessment(),
        test_coverage=TestCoverageStatus(),
        readiness_tier="blocked",
    )
    needs_review = FileReadinessAssessment(
        file="engine/bar.py",
        is_new_file=False,
        is_deleted_file=False,
        lines_added=0,
        lines_removed=0,
        hygiene_flags=[],
        structural=StructuralAssessment(),
        test_coverage=TestCoverageStatus(),
        readiness_tier="needs-review",
    )
    stats = compute_stats(files, [blocked, needs_review])

    assert stats.hygiene_flag_count == 1
    assert stats.blocked_file_count == 1
    assert stats.needs_review_file_count == 1


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
