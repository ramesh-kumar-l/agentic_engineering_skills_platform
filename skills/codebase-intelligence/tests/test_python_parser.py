from pathlib import Path

from engine import python_parser


def test_parses_imports_defs_classes_docstring(tmp_path: Path):
    (tmp_path / "mod.py").write_text(
        '"""Module docstring."""\n'
        "import os\n"
        "from collections import Counter\n"
        "\n"
        "def foo():\n"
        "    pass\n"
        "\n"
        "class Bar:\n"
        "    pass\n",
        encoding="utf-8",
    )

    info = python_parser.parse_python_file(tmp_path, "mod.py")

    assert info.docstring == "Module docstring."
    assert info.functions == ["foo"]
    assert info.classes == ["Bar"]
    assert "os" in info.imports
    assert "collections" in info.imports
    assert info.parse_error is None


def test_handles_syntax_error_gracefully(tmp_path: Path):
    (tmp_path / "broken.py").write_text("def foo(:\n", encoding="utf-8")

    info = python_parser.parse_python_file(tmp_path, "broken.py")

    assert info.parse_error is not None
    assert info.functions == []


def test_relative_imports_captured(tmp_path: Path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "mod.py").write_text("from . import sibling\nfrom .. import other\n", encoding="utf-8")

    info = python_parser.parse_python_file(tmp_path, "pkg/mod.py")

    assert ".sibling" in info.imports
    assert "..other" in info.imports


def test_has_main_guard_detects_real_guard(tmp_path: Path):
    (tmp_path / "with_main.py").write_text("if __name__ == '__main__':\n    pass\n", encoding="utf-8")
    (tmp_path / "without_main.py").write_text("x = 1\n", encoding="utf-8")

    assert python_parser.parse_python_file(tmp_path, "with_main.py").has_main_guard is True
    assert python_parser.parse_python_file(tmp_path, "without_main.py").has_main_guard is False


def test_has_main_guard_ignores_string_mentions(tmp_path: Path):
    # A file that merely CONTAINS the text '__name__ == "__main__"' inside a
    # docstring/string literal must NOT be misclassified as an entry point.
    (tmp_path / "mentions_it.py").write_text(
        '"""Docs mention __name__ == \'__main__\' as an example."""\n'
        "PATTERN = \"__name__ == '__main__'\"\n",
        encoding="utf-8",
    )

    info = python_parser.parse_python_file(tmp_path, "mentions_it.py")

    assert info.has_main_guard is False
