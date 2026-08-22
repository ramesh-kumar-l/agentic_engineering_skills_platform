"""Shared data schema for the Codebase Intelligence report.

Every other engine module produces or consumes these types. Keeping the
schema in one file means the JSON/Markdown renderers and the evaluation
harness all agree on the same contract without importing each other.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FileInfo:
    path: str  # POSIX-style, relative to scan root
    language: str  # e.g. "python", "javascript", "unknown"
    size_bytes: int
    line_count: int


@dataclass
class ModuleInfo:
    path: str
    language: str
    docstring: str | None
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)  # raw import targets, as written
    has_main_guard: bool = False  # top-level `if __name__ == "__main__":` — AST-verified, not text search
    parse_error: str | None = None  # set when the file couldn't be parsed


@dataclass
class EntryPoint:
    path: str
    reason: str  # e.g. "if __name__ == '__main__'", "package.json bin"


@dataclass
class ExternalDependency:
    name: str
    version: str | None
    source_file: str


@dataclass
class DependencyEdge:
    source: str  # module path
    target: str  # module path


@dataclass
class DependencyGraph:
    edges: list[DependencyEdge] = field(default_factory=list)
    fan_in: dict[str, int] = field(default_factory=dict)
    fan_out: dict[str, int] = field(default_factory=dict)
    hotspots: list[str] = field(default_factory=list)  # top modules by fan_in+fan_out


@dataclass
class DocCoverage:
    dirs_with_readme: list[str] = field(default_factory=list)
    dirs_without_readme: list[str] = field(default_factory=list)


@dataclass
class CodebaseIntelligenceReport:
    root_path: str
    generated_at: str  # ISO 8601 UTC
    file_count: int
    language_breakdown: dict[str, int]
    files: list[FileInfo]
    modules: list[ModuleInfo]
    entry_points: list[EntryPoint]
    dependency_graph: DependencyGraph
    external_dependencies: list[ExternalDependency]
    doc_coverage: DocCoverage
    excluded_dir_count: int
    skipped_file_count: int
    warnings: list[str] = field(default_factory=list)
