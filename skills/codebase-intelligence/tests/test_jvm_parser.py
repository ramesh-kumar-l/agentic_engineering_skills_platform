from pathlib import Path

from engine import jvm_parser


def test_parses_java_package_imports_and_class(tmp_path: Path):
    (tmp_path / "App.java").write_text(
        "package com.example;\n"
        "\n"
        "import com.example.util.Helper;\n"
        "import java.util.List;\n"
        "\n"
        "public class App {\n"
        "}\n",
        encoding="utf-8",
    )

    info = jvm_parser.parse_jvm_file(tmp_path, "App.java", "java")

    assert info.package == "com.example"
    assert "com.example.util.Helper" in info.imports
    assert "java.util.List" in info.imports
    assert info.classes == ["App"]
    assert info.parse_error is None


def test_parses_kotlin_package_imports_class_and_function(tmp_path: Path):
    (tmp_path / "Util.kt").write_text(
        "package com.example\n"
        "\n"
        "import com.example.other.Thing\n"
        "\n"
        "class Helper {\n"
        "}\n"
        "\n"
        "fun doWork() {\n"
        "}\n",
        encoding="utf-8",
    )

    info = jvm_parser.parse_jvm_file(tmp_path, "Util.kt", "kotlin")

    assert info.package == "com.example"
    assert "com.example.other.Thing" in info.imports
    assert info.classes == ["Helper"]
    assert info.functions == ["doWork"]


def test_no_package_declaration_is_none(tmp_path: Path):
    (tmp_path / "NoPackage.java").write_text("public class NoPackage {\n}\n", encoding="utf-8")

    info = jvm_parser.parse_jvm_file(tmp_path, "NoPackage.java", "java")

    assert info.package is None


def test_wildcard_import_captured_with_suffix(tmp_path: Path):
    (tmp_path / "App.java").write_text(
        "package com.example;\n\nimport com.example.models.*;\n\npublic class App {\n}\n",
        encoding="utf-8",
    )

    info = jvm_parser.parse_jvm_file(tmp_path, "App.java", "java")

    assert "com.example.models.*" in info.imports


def test_java_main_detected(tmp_path: Path):
    (tmp_path / "Main.java").write_text(
        "package com.example;\n\n"
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        "    }\n"
        "}\n",
        encoding="utf-8",
    )

    assert jvm_parser.parse_jvm_file(tmp_path, "Main.java", "java").has_main_guard is True


def test_java_main_not_detected_without_both_modifiers(tmp_path: Path):
    (tmp_path / "NotMain.java").write_text(
        "package com.example;\n\n"
        "public class NotMain {\n"
        "    static void main(String[] args) {\n"
        "    }\n"
        "}\n",
        encoding="utf-8",
    )

    assert jvm_parser.parse_jvm_file(tmp_path, "NotMain.java", "java").has_main_guard is False


def test_kotlin_main_detected(tmp_path: Path):
    (tmp_path / "main.kt").write_text("fun main() {\n}\n", encoding="utf-8")

    assert jvm_parser.parse_jvm_file(tmp_path, "main.kt", "kotlin").has_main_guard is True


def test_kotlin_no_main_function(tmp_path: Path):
    (tmp_path / "helper.kt").write_text("fun doWork() {\n}\n", encoding="utf-8")

    assert jvm_parser.parse_jvm_file(tmp_path, "helper.kt", "kotlin").has_main_guard is False


def test_unreadable_file_sets_parse_error(tmp_path: Path):
    info = jvm_parser.parse_jvm_file(tmp_path, "missing.java", "java")

    assert info.parse_error is not None
    assert info.classes == []
