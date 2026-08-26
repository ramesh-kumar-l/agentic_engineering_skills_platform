from engine.diff_parser import parse_diff
from engine.hygiene_scanner import scan


def _files(diff_text):
    return parse_diff(diff_text).files


def test_flags_debug_print_leftover():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,3 @@
 def bar():
+    print("debug value:", x)
     return 1
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert "debug-print-leftover" in ids


def test_flags_console_log_leftover():
    diff = """diff --git a/app.js b/app.js
--- a/app.js
+++ b/app.js
@@ -1,1 +1,2 @@
 function f() {
+  console.log("here");
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert "debug-print-leftover" in ids


def test_no_debug_flag_on_removed_print_line():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,1 @@
-    print("debug")
     return 1
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert "debug-print-leftover" not in ids


def test_flags_todo_blocking_marker():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,1 +1,2 @@
 def bar():
+    # TODO: handle the edge case before release
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert "todo-blocking-marker" in ids


def test_flags_hardcoded_secret_shaped_literal():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,1 +1,2 @@
 def bar():
+    api_key = "sk-1234567890abcdef"
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert "hardcoded-secret-shaped" in ids


def test_flags_merge_conflict_marker():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,1 +1,5 @@
 def bar():
+<<<<<<< HEAD
+    return 1
+=======
+    return 2
+>>>>>>> feature-branch
"""
    flags = scan(_files(diff)[0])
    ids = [f.pattern_id for f in flags]
    assert ids.count("merge-conflict-marker") == 3


def test_no_flags_on_clean_diff():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
 def bar():
-    return 1
+    return 2
"""
    flags = scan(_files(diff)[0])
    assert flags == []


def test_multiple_flags_on_same_file_all_collected():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,1 +1,3 @@
 def bar():
+    print("x")
+    # TODO: fix this
"""
    flags = scan(_files(diff)[0])
    ids = {f.pattern_id for f in flags}
    assert {"debug-print-leftover", "todo-blocking-marker"} <= ids
