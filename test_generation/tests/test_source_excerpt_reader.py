from test_generation.source_excerpt_reader import read_source_excerpt


def test_finds_def_and_returns_excerpt(tmp_path):
    (tmp_path / "mod.py").write_text(
        "x = 1\n\ndef foo(a, b):\n    return a + b\n", encoding="utf-8"
    )

    excerpt = read_source_excerpt(str(tmp_path), "mod.py", "foo")

    assert excerpt is not None
    assert "def foo(a, b):" in excerpt


def test_finds_class_and_returns_excerpt(tmp_path):
    (tmp_path / "mod.py").write_text(
        "class Baz:\n    def method(self):\n        pass\n", encoding="utf-8"
    )

    excerpt = read_source_excerpt(str(tmp_path), "mod.py", "Baz")

    assert excerpt is not None
    assert "class Baz:" in excerpt


def test_symbol_none_returns_none(tmp_path):
    (tmp_path / "mod.py").write_text("x = 1\n", encoding="utf-8")

    assert read_source_excerpt(str(tmp_path), "mod.py", None) is None


def test_missing_file_returns_none(tmp_path):
    assert read_source_excerpt(str(tmp_path), "missing.py", "foo") is None


def test_symbol_not_found_returns_none(tmp_path):
    (tmp_path / "mod.py").write_text("x = 1\n", encoding="utf-8")

    assert read_source_excerpt(str(tmp_path), "mod.py", "nonexistent") is None


def test_falls_back_to_bare_occurrence(tmp_path):
    (tmp_path / "mod.py").write_text(
        "SOME_CONSTANT = foo_related_value\n", encoding="utf-8"
    )

    excerpt = read_source_excerpt(str(tmp_path), "mod.py", "foo_related_value")

    assert excerpt is not None
    assert "foo_related_value" in excerpt
