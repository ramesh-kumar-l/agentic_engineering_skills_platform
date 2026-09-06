import pytest

from test_validation.generated_tests_loader import GeneratedTestsError, list_generated_tests


def test_lists_files_in_directory(tmp_path):
    (tmp_path / "test_a.py").write_text("", encoding="utf-8")
    (tmp_path / "test_b.py").write_text("", encoding="utf-8")

    files = list_generated_tests(tmp_path)

    assert [f.name for f in files] == ["test_a.py", "test_b.py"]


def test_lists_files_in_nested_subdirectories(tmp_path):
    sub = tmp_path / "pkg"
    sub.mkdir()
    (sub / "test_nested.py").write_text("", encoding="utf-8")

    files = list_generated_tests(tmp_path)

    assert len(files) == 1
    assert files[0].name == "test_nested.py"


def test_missing_directory_raises_error(tmp_path):
    with pytest.raises(GeneratedTestsError):
        list_generated_tests(tmp_path / "does-not-exist")


def test_empty_directory_returns_empty_list(tmp_path):
    assert list_generated_tests(tmp_path) == []


def test_filters_out_pytest_cache_artifacts(tmp_path):
    # Regression test for a real bug found via dogfooding: a prior run's
    # own .pytest_cache/ directory (created as a side effect of executing
    # pytest inside generated_tests_dir) was being listed as a "generated
    # test file" and reported as a bogus, non-executable outcome.
    (tmp_path / "test_real.py").write_text("", encoding="utf-8")
    cache_dir = tmp_path / ".pytest_cache" / "v" / "cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "nodeids").write_text("[]", encoding="utf-8")
    (tmp_path / ".pytest_cache" / "CACHEDIR.TAG").write_text("", encoding="utf-8")

    files = list_generated_tests(tmp_path)

    assert [f.name for f in files] == ["test_real.py"]


def test_filters_out_unrecognized_extensions(tmp_path):
    (tmp_path / "test_real.py").write_text("", encoding="utf-8")
    (tmp_path / "README.md").write_text("", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")

    files = list_generated_tests(tmp_path)

    assert [f.name for f in files] == ["test_real.py"]


def test_recognizes_jvm_extensions(tmp_path):
    (tmp_path / "FooTest.java").write_text("", encoding="utf-8")
    (tmp_path / "BarSpec.kt").write_text("", encoding="utf-8")

    files = list_generated_tests(tmp_path)

    assert {f.name for f in files} == {"FooTest.java", "BarSpec.kt"}
