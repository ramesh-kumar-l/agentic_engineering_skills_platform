import json

import pytest

from test_generation.naming_convention import (
    NamingConventionError,
    infer_naming_convention,
    load_naming_convention_override,
)


def test_infers_majority_python_pattern(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_foo.py").write_text("", encoding="utf-8")
    (tmp_path / "tests" / "test_bar.py").write_text("", encoding="utf-8")
    (tmp_path / "tests" / "baz_test.py").write_text("", encoding="utf-8")

    convention = infer_naming_convention(str(tmp_path))

    assert convention.pattern == "test_*.py"
    assert convention.source == "inferred"


def test_infers_jvm_pattern(tmp_path):
    (tmp_path / "src" / "test").mkdir(parents=True)
    (tmp_path / "src" / "test" / "FooTest.java").write_text("", encoding="utf-8")
    (tmp_path / "src" / "test" / "BarTest.java").write_text("", encoding="utf-8")

    convention = infer_naming_convention(str(tmp_path))

    assert convention.pattern == "*Test.java"


def test_no_test_files_returns_platform_default(tmp_path):
    (tmp_path / "mod.py").write_text("", encoding="utf-8")

    convention = infer_naming_convention(str(tmp_path))

    assert convention.source == "platform-default"
    assert convention.pattern == "test_*.py"


def test_nonexistent_repo_root_returns_platform_default(tmp_path):
    convention = infer_naming_convention(str(tmp_path / "does-not-exist"))

    assert convention.source == "platform-default"


def test_load_override_returns_convention_with_override_source(tmp_path):
    path = tmp_path / "convention.json"
    path.write_text(
        json.dumps({"pattern": "*_test.py", "example": "foo_test.py"}),
        encoding="utf-8",
    )

    convention = load_naming_convention_override(path)

    assert convention.pattern == "*_test.py"
    assert convention.source == "override"


def test_load_override_missing_file_raises_error(tmp_path):
    with pytest.raises(NamingConventionError):
        load_naming_convention_override(tmp_path / "missing.json")


def test_load_override_missing_field_raises_error(tmp_path):
    path = tmp_path / "convention.json"
    path.write_text(json.dumps({"pattern": "*_test.py"}), encoding="utf-8")

    with pytest.raises(NamingConventionError):
        load_naming_convention_override(path)
