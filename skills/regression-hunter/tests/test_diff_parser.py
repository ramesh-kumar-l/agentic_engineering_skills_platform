from engine.diff_parser import parse_diff

DIFF = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,3 +1,3 @@
 def bar():
-    return 1
+    return 2
"""


def test_parses_file_paths():
    ctx = parse_diff(DIFF)
    assert len(ctx.files) == 1
    assert ctx.files[0].old_path == "engine/foo.py"
    assert ctx.files[0].new_path == "engine/foo.py"


def test_parses_hunk_lines():
    ctx = parse_diff(DIFF)
    hunk = ctx.files[0].hunks[0]
    kinds = [line.kind for line in hunk.lines]
    assert kinds == ["context", "remove", "add"]


def test_new_file_detected():
    diff = """diff --git a/new.py b/new.py
--- /dev/null
+++ b/new.py
@@ -0,0 +1,2 @@
+def x():
+    pass
"""
    ctx = parse_diff(diff)
    assert ctx.files[0].is_new_file is True
    assert ctx.files[0].old_path is None


def test_deleted_file_detected():
    diff = """diff --git a/gone.py b/gone.py
--- a/gone.py
+++ /dev/null
@@ -1,2 +0,0 @@
-def x():
-    pass
"""
    ctx = parse_diff(diff)
    assert ctx.files[0].is_deleted_file is True
    assert ctx.files[0].new_path is None


def test_hunk_header_before_file_header_warns():
    diff = "@@ -1,1 +1,1 @@\n-x\n+y\n"
    ctx = parse_diff(diff)
    assert ctx.warnings
    assert ctx.files == []


def test_effective_path_prefers_new_path():
    diff = """diff --git a/gone.py b/gone.py
--- a/gone.py
+++ /dev/null
@@ -1,1 +0,0 @@
-x
"""
    ctx = parse_diff(diff)
    assert ctx.files[0].effective_path == "gone.py"


def test_empty_diff_yields_no_files():
    ctx = parse_diff("")
    assert ctx.files == []
    assert ctx.warnings == []


def test_line_numbers_tracked_correctly():
    ctx = parse_diff(DIFF)
    hunk = ctx.files[0].hunks[0]
    removed = [l for l in hunk.lines if l.kind == "remove"][0]
    added = [l for l in hunk.lines if l.kind == "add"][0]
    assert removed.old_lineno == 2
    assert added.new_lineno == 2
