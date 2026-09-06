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


def test_build_report_java_kotlin_pipeline(tmp_path: Path):
    java_dir = tmp_path / "src" / "main" / "java" / "com" / "example"
    java_dir.mkdir(parents=True)
    (java_dir / "App.java").write_text(
        "package com.example;\n\n"
        "import com.example.Util;\n\n"
        "public class App {\n"
        "    public static void main(String[] args) {\n"
        "        Util.doWork();\n"
        "    }\n"
        "}\n",
        encoding="utf-8",
    )
    kotlin_dir = tmp_path / "src" / "main" / "kotlin" / "com" / "example"
    kotlin_dir.mkdir(parents=True)
    (kotlin_dir / "Util.kt").write_text(
        "package com.example\n\nobject Util {\n}\n\nfun doWork() {\n}\n",
        encoding="utf-8",
    )
    (tmp_path / "build.gradle").write_text(
        "dependencies {\n    implementation 'com.google.guava:guava:31.1-jre'\n}\n",
        encoding="utf-8",
    )

    report = build_report(tmp_path)

    assert report.language_breakdown.get("java") == 1
    assert report.language_breakdown.get("kotlin") == 1
    assert any(ep.reason == "public static void main(String[])" for ep in report.entry_points)
    assert report.dependency_graph.edges  # App.java -> Util.kt via package-index resolution
    assert any(d.name == "com.google.guava:guava" for d in report.external_dependencies)
