from engine.diff_parser import parse_diff

SIMPLE_DIFF = """diff --git a/foo.py b/foo.py
--- a/foo.py
+++ b/foo.py
@@ -1,3 +1,4 @@
 def add(a, b):
-    return a + b
+    return a + b  # fixed
+
 print(add(1, 2))
"""

NEW_FILE_DIFF = """diff --git a/new_mod.py b/new_mod.py
new file mode 100644
--- /dev/null
+++ b/new_mod.py
@@ -0,0 +1,2 @@
+def hello():
+    return "hi"
"""

DELETED_FILE_DIFF = """diff --git a/old_mod.py b/old_mod.py
deleted file mode 100644
--- a/old_mod.py
+++ /dev/null
@@ -1,2 +0,0 @@
-def bye():
-    return "bye"
"""

MULTI_FILE_DIFF = SIMPLE_DIFF + NEW_FILE_DIFF


def test_parses_file_paths_and_hunk_bounds():
    context = parse_diff(SIMPLE_DIFF)
    assert len(context.files) == 1
    f = context.files[0]
    assert f.old_path == "foo.py"
    assert f.new_path == "foo.py"
    assert not f.is_new_file
    assert not f.is_deleted_file
    assert len(f.hunks) == 1
    hunk = f.hunks[0]
    assert hunk.old_start == 1
    assert hunk.new_start == 1


def test_line_kinds_and_line_numbers():
    context = parse_diff(SIMPLE_DIFF)
    lines = context.files[0].hunks[0].lines
    kinds = [line.kind for line in lines]
    assert kinds == ["context", "remove", "add", "add", "context"]
    added = [line for line in lines if line.kind == "add"]
    assert added[0].new_lineno == 2
    assert added[1].new_lineno == 3


def test_new_file_detected():
    context = parse_diff(NEW_FILE_DIFF)
    f = context.files[0]
    assert f.is_new_file
    assert f.old_path is None
    assert f.new_path == "new_mod.py"


def test_deleted_file_detected():
    context = parse_diff(DELETED_FILE_DIFF)
    f = context.files[0]
    assert f.is_deleted_file
    assert f.new_path is None
    assert f.old_path == "old_mod.py"


def test_multi_file_diff_produces_multiple_files():
    context = parse_diff(MULTI_FILE_DIFF)
    assert len(context.files) == 2
    assert context.files[0].new_path == "foo.py"
    assert context.files[1].new_path == "new_mod.py"


def test_no_newline_marker_is_ignored():
    diff_text = SIMPLE_DIFF + "\\ No newline at end of file\n"
    context = parse_diff(diff_text)
    assert len(context.files) == 1


def test_empty_diff_produces_no_files():
    context = parse_diff("")
    assert context.files == []
    assert context.warnings == []
