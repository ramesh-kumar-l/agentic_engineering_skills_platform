from engine.diff_parser import parse_diff
from engine.regression_scanner import scan


def _files(diff_text):
    return parse_diff(diff_text).files


def test_flags_removed_exception_handling():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,5 +1,2 @@
 def bar():
-    try:
-        return 1
-    except Exception:
-        return None
+    return 1
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "removed-exception-handling" in ids


def test_no_flag_when_exception_handling_replaced_not_removed():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,3 +1,3 @@
 def bar():
-    except ValueError:
+    except (ValueError, TypeError):
         pass
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "removed-exception-handling" not in ids


def test_flags_removed_conditional_guard():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,4 +1,2 @@
 def bar(x):
-    if x is None:
-        return
     do_thing(x)
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "removed-conditional-guard" in ids


def test_no_flag_when_guard_replaced():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
-    if x is None:
+    if x is not None and x:
         return
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "removed-conditional-guard" not in ids


def test_flags_large_deletion_with_no_addition():
    removed_lines = "\n".join(f"-    line{i}" for i in range(12))
    diff = f"""diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,12 +0,0 @@
{removed_lines}
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "large-deletion-no-addition" in ids


def test_no_large_deletion_flag_below_threshold():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +0,0 @@
-    line1
-    line2
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "large-deletion-no-addition" not in ids


def test_flags_decreased_test_assertions_in_test_file():
    diff = """diff --git a/tests/test_foo.py b/tests/test_foo.py
--- a/tests/test_foo.py
+++ b/tests/test_foo.py
@@ -1,4 +1,2 @@
 def test_bar():
-    assert bar() == 1
-    assert bar() != 2
+    assert bar() == 1
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "decreased-test-assertions" in ids


def test_no_assertion_flag_when_not_a_test_file():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,1 @@
-    assert x
     pass
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "decreased-test-assertions" not in ids


def test_no_assertion_flag_when_assertions_increased():
    diff = """diff --git a/tests/test_foo.py b/tests/test_foo.py
--- a/tests/test_foo.py
+++ b/tests/test_foo.py
@@ -1,2 +1,3 @@
 def test_bar():
-    assert bar() == 1
+    assert bar() == 1
+    assert bar() != 2
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "decreased-test-assertions" not in ids


def test_flags_signature_change_with_no_test_file_in_diff():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
-def bar(x):
+def bar(x, y):
     pass
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" in ids


def test_no_signature_flag_when_matching_test_file_also_changed():
    diff = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
-def bar(x):
+def bar(x, y):
     pass
diff --git a/tests/test_foo.py b/tests/test_foo.py
--- a/tests/test_foo.py
+++ b/tests/test_foo.py
@@ -1,1 +1,1 @@
-    assert bar(1)
+    assert bar(1, 2)
"""
    files = _files(diff)
    foo_file = [f for f in files if f.new_path == "engine/foo.py"][0]
    flags = scan(foo_file, files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" not in ids


def test_no_signature_flag_for_test_file_itself():
    diff = """diff --git a/tests/test_foo.py b/tests/test_foo.py
--- a/tests/test_foo.py
+++ b/tests/test_foo.py
@@ -1,2 +1,2 @@
-def test_bar(x):
+def test_bar(x, y):
     pass
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" not in ids


def test_flags_java_signature_change_with_no_test_file_in_diff():
    diff = """diff --git a/src/main/java/com/example/App.java b/src/main/java/com/example/App.java
--- a/src/main/java/com/example/App.java
+++ b/src/main/java/com/example/App.java
@@ -1,2 +1,2 @@
-    public void doWork(int x) {
+    public void doWork(int x, int y) {
     }
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" in ids


def test_no_java_signature_flag_when_matching_test_file_also_changed():
    # Paths deliberately avoid a "test"/"tests" directory segment, so this
    # exercises is_test_shaped_path's new JVM PascalCase-suffix recognition
    # of "AppTest.java" (ADR-022), not the pre-existing path-segment check.
    diff = """diff --git a/com/example/App.java b/com/example/App.java
--- a/com/example/App.java
+++ b/com/example/App.java
@@ -1,2 +1,2 @@
-    public void doWork(int x) {
+    public void doWork(int x, int y) {
     }
diff --git a/com/example/AppTest.java b/com/example/AppTest.java
--- a/com/example/AppTest.java
+++ b/com/example/AppTest.java
@@ -1,1 +1,1 @@
-    app.doWork(1);
+    app.doWork(1, 2);
"""
    files = _files(diff)
    app_file = [f for f in files if f.new_path == "com/example/App.java"][0]
    flags = scan(app_file, files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" not in ids


def test_flags_kotlin_fun_signature_change_with_no_test_file_in_diff():
    diff = """diff --git a/src/main/kotlin/com/example/Util.kt b/src/main/kotlin/com/example/Util.kt
--- a/src/main/kotlin/com/example/Util.kt
+++ b/src/main/kotlin/com/example/Util.kt
@@ -1,2 +1,2 @@
-fun doWork(x: Int) {
+fun doWork(x: Int, y: Int) {
 }
"""
    files = _files(diff)
    flags = scan(files[0], files)
    ids = [f.pattern_id for f in flags]
    assert "modified-signature-no-test-change" in ids
