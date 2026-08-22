from engine.diff_parser import parse_diff
from engine.stats import compute_stats

DIFF_TEXT = """diff --git a/foo.py b/foo.py
--- a/foo.py
+++ b/foo.py
@@ -1,3 +1,4 @@
 def add(a, b):
-    return a + b
+    return a + b  # fixed
+
 print(add(1, 2))
diff --git a/new_mod.py b/new_mod.py
new file mode 100644
--- /dev/null
+++ b/new_mod.py
@@ -0,0 +1,2 @@
+def hello():
+    return "hi"
"""


def test_stats_counts_files_and_lines():
    context = parse_diff(DIFF_TEXT)
    stats = compute_stats(context)
    assert stats.files_touched == 2
    assert stats.files_added == 1
    assert stats.files_deleted == 0
    assert stats.lines_added == 4
    assert stats.lines_removed == 1
    assert stats.hunk_count == 2


def test_stats_on_empty_diff():
    context = parse_diff("")
    stats = compute_stats(context)
    assert stats.files_touched == 0
    assert stats.lines_added == 0
    assert stats.lines_removed == 0
