from pathlib import Path

from engine.report import build_report


def test_build_report_basic_shape(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "import helper\n\nif __name__ == '__main__':\n    pass\n", encoding="utf-8"
    )
    (tmp_path / "helper.py").write_text('"""Helper module."""\ndef util():\n    pass\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("# Project\n", encoding="utf-8")

    report = build_report(tmp_path)

    assert report.file_count == 3
    assert report.language_breakdown.get("python") == 2
    assert any(m.path == "helper.py" and m.docstring == "Helper module." for m in report.modules)
    assert any(ep.path == "main.py" for ep in report.entry_points)
    assert report.dependency_graph.edges  # main.py -> helper.py
    assert "" in report.doc_coverage.dirs_with_readme


def test_build_report_on_empty_dir(tmp_path: Path):
    report = build_report(tmp_path)

    assert report.file_count == 0
    assert report.modules == []
    assert report.dependency_graph.edges == []
    assert report.entry_points == []
