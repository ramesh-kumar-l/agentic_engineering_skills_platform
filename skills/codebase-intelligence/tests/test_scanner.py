from pathlib import Path

from engine import scanner


def test_scan_finds_python_files(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.py").write_text("y = 2\n", encoding="utf-8")

    files, excluded_dirs, skipped, warnings = scanner.scan(tmp_path)

    paths = {f.path for f in files}
    assert paths == {"a.py", "sub/b.py"}
    assert excluded_dirs == 0
    assert skipped == 0
    assert warnings == []


def test_scan_excludes_default_dirs(tmp_path: Path):
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "lib.js").write_text("module.exports = {};\n", encoding="utf-8")
    (tmp_path / "app.js").write_text("console.log(1);\n", encoding="utf-8")

    files, excluded_dirs, _, _ = scanner.scan(tmp_path)

    assert {f.path for f in files} == {"app.js"}
    assert excluded_dirs == 1


def test_scan_skips_secret_shaped_files_without_reading_content(tmp_path: Path):
    (tmp_path / ".env").write_text("SECRET_KEY=super-secret-value\n", encoding="utf-8")
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")

    files, _, skipped, warnings = scanner.scan(tmp_path)

    assert {f.path for f in files} == {"app.py"}
    assert skipped == 1
    assert any("secret-shaped" in w for w in warnings)
    assert all("super-secret-value" not in w for w in warnings)


def test_scan_skips_oversized_files(tmp_path: Path):
    big = tmp_path / "big.py"
    big.write_text("x = 1\n" * 100, encoding="utf-8")

    files, _, skipped, warnings = scanner.scan(tmp_path, max_file_size_bytes=10)

    assert files == []
    assert skipped == 1
    assert any("oversized" in w for w in warnings)


def test_detect_language():
    assert scanner.detect_language(Path("a.py")) == "python"
    assert scanner.detect_language(Path("a.ts")) == "typescript"
    assert scanner.detect_language(Path("a.xyz")) == "unknown"
