"""Orchestrates scanner + parsers + graph + external_deps into one report.

This is the only module that knows the full pipeline order; every other
module is independently testable in isolation.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from . import external_deps, generic_parser, graph, python_parser, scanner
from .models import CodebaseIntelligenceReport, DocCoverage, EntryPoint, FileInfo, ModuleInfo

PARSEABLE_LANGUAGES = {"python", "javascript", "typescript", "java"}


def build_report(root: Path) -> CodebaseIntelligenceReport:
    root = root.resolve()
    files, excluded_dir_count, skipped_file_count, warnings = scanner.scan(root)

    modules = _parse_modules(root, files)
    dep_graph = graph.build_graph(modules)
    ext_deps = external_deps.parse_external_dependencies(root)
    entry_points = _find_entry_points(root, modules)
    doc_coverage = _compute_doc_coverage(files)
    language_breakdown = dict(Counter(f.language for f in files))

    return CodebaseIntelligenceReport(
        root_path=str(root),
        generated_at=datetime.now(UTC).isoformat(),
        file_count=len(files),
        language_breakdown=language_breakdown,
        files=files,
        modules=modules,
        entry_points=entry_points,
        dependency_graph=dep_graph,
        external_dependencies=ext_deps,
        doc_coverage=doc_coverage,
        excluded_dir_count=excluded_dir_count,
        skipped_file_count=skipped_file_count,
        warnings=warnings,
    )


def _parse_modules(root: Path, files: list[FileInfo]) -> list[ModuleInfo]:
    modules: list[ModuleInfo] = []
    for f in files:
        if f.language == "python":
            modules.append(python_parser.parse_python_file(root, f.path))
        elif f.language in PARSEABLE_LANGUAGES:
            modules.append(generic_parser.parse_generic_file(root, f.path, f.language))
    return modules


def _find_entry_points(root: Path, modules: list[ModuleInfo]) -> list[EntryPoint]:
    entry_points: list[EntryPoint] = []
    for m in modules:
        if m.language == "python" and m.has_main_guard:
            entry_points.append(EntryPoint(path=m.path, reason="if __name__ == '__main__'"))

    package_json = root / "package.json"
    if package_json.exists():
        import json
        try:
            data = json.loads(package_json.read_text(encoding="utf-8", errors="ignore"))
            bin_field = data.get("bin")
            main_field = data.get("main")
            if bin_field:
                entry_points.append(EntryPoint(path=str(bin_field), reason="package.json bin"))
            if main_field:
                entry_points.append(EntryPoint(path=str(main_field), reason="package.json main"))
        except (ValueError, OSError):
            pass
    return entry_points


def _compute_doc_coverage(files: list[FileInfo]) -> DocCoverage:
    dirs_with_files: set[str] = set()
    dirs_with_readme: set[str] = set()
    for f in files:
        parent = PurePosixPath(f.path).parent.as_posix()
        parent = "" if parent == "." else parent
        dirs_with_files.add(parent)
        if PurePosixPath(f.path).name.lower().startswith("readme"):
            dirs_with_readme.add(parent)
    dirs_without = sorted(dirs_with_files - dirs_with_readme)
    return DocCoverage(dirs_with_readme=sorted(dirs_with_readme), dirs_without_readme=dirs_without)
