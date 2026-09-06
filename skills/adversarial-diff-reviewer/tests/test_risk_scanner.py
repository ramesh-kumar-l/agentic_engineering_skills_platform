from engine.diff_parser import parse_diff
from engine.risk_scanner import scan

SECRET_DIFF = """diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,1 +1,2 @@
 import os
+api_key = "sk-live-do-not-leak-this-value-12345"
"""

EVAL_DIFF = """diff --git a/run.py b/run.py
--- a/run.py
+++ b/run.py
@@ -1,1 +1,2 @@
 x = 1
+eval(user_input)
"""

BARE_EXCEPT_DIFF = """diff --git a/handler.py b/handler.py
--- a/handler.py
+++ b/handler.py
@@ -1,2 +1,4 @@
 try:
     risky()
+except:
+    pass
"""

CLEAN_DIFF = """diff --git a/util.py b/util.py
--- a/util.py
+++ b/util.py
@@ -1,1 +1,2 @@
 def add(a, b):
+    return a + b
"""


def test_hardcoded_secret_flagged_and_redacted():
    context = parse_diff(SECRET_DIFF)
    flags = scan(context)
    secret_flags = [f for f in flags if f.pattern_id == "hardcoded-secret"]
    assert len(secret_flags) == 1
    assert "do-not-leak" not in secret_flags[0].matched_text
    assert secret_flags[0].matched_text == "<redacted>"
    assert secret_flags[0].severity == "high"


def test_eval_call_flagged():
    context = parse_diff(EVAL_DIFF)
    flags = scan(context)
    assert any(f.pattern_id == "dangerous-eval-exec" for f in flags)


def test_bare_except_flagged():
    context = parse_diff(BARE_EXCEPT_DIFF)
    flags = scan(context)
    assert any(f.pattern_id == "broad-except-bare" for f in flags)


def test_clean_diff_produces_no_flags():
    context = parse_diff(CLEAN_DIFF)
    flags = scan(context)
    assert flags == []


def test_all_occurrences_of_a_secret_pattern_on_one_line_are_redacted():
    diff_text = """diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,1 +1,2 @@
 import os
+api_key = "primary-do-not-leak-AAAAAA"; token = "backup-do-not-leak-BBBBBB"
"""
    context = parse_diff(diff_text)
    flags = scan(context)
    redacted_line = context.files[0].hunks[0].lines[1].content
    assert "do-not-leak" not in redacted_line
    assert redacted_line.count("<redacted>") == 2


def test_jvm_runtime_exec_flagged():
    diff = """diff --git a/App.java b/App.java
--- a/App.java
+++ b/App.java
@@ -1,1 +1,2 @@
 public class App {
+    Runtime.getRuntime().exec(cmd);
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-runtime-exec" for f in flags)


def test_jvm_processbuilder_flagged():
    diff = """diff --git a/App.java b/App.java
--- a/App.java
+++ b/App.java
@@ -1,1 +1,2 @@
 public class App {
+    new ProcessBuilder(cmd).start();
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-processbuilder" for f in flags)


def test_jvm_broad_catch_exception_flagged():
    diff = """diff --git a/App.java b/App.java
--- a/App.java
+++ b/App.java
@@ -1,1 +1,2 @@
 try {
+} catch (Exception e) {
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-broad-catch-exception" for f in flags)


def test_jvm_broad_catch_throwable_flagged():
    diff = """diff --git a/App.java b/App.java
--- a/App.java
+++ b/App.java
@@ -1,1 +1,2 @@
 try {
+} catch (Throwable t) {
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-broad-catch-throwable" for f in flags)


def test_jvm_sql_string_concat_flagged():
    diff = """diff --git a/Dao.java b/Dao.java
--- a/Dao.java
+++ b/Dao.java
@@ -1,1 +1,2 @@
 public class Dao {
+    stmt.executeQuery("SELECT * FROM users WHERE id=" + id);
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-sql-string-concat" for f in flags)


def test_jvm_debug_println_flagged():
    diff = """diff --git a/App.java b/App.java
--- a/App.java
+++ b/App.java
@@ -1,1 +1,2 @@
 public class App {
+    System.out.println("debug");
"""
    flags = scan(parse_diff(diff))
    assert any(f.pattern_id == "jvm-debug-println" for f in flags)


def test_flags_only_scan_added_lines_not_removed():
    diff_text = """diff --git a/mod.py b/mod.py
--- a/mod.py
+++ b/mod.py
@@ -1,2 +1,2 @@
-eval(old_input)
+safe_call(new_input)
"""
    context = parse_diff(diff_text)
    flags = scan(context)
    assert flags == []
