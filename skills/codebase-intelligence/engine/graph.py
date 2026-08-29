"""Builds the internal (repo-local) dependency graph from parsed imports.

Only imports that resolve to a file inside the scanned repo become graph
edges. Everything else (stdlib, third-party packages) is left out of the
graph on purpose — external_deps.py handles third-party dependencies
separately, so the graph stays a clean map of internal coupling.
"""

from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath

from .models import DependencyEdge, DependencyGraph, ModuleInfo

HOTSPOT_LIMIT = 10


def build_graph(modules: list[ModuleInfo]) -> DependencyGraph:
    python_index = _build_python_index(modules)
    js_index = {m.path for m in modules if m.language in ("javascript", "typescript")}
    fqn_to_path, package_members = _build_jvm_fqn_index(modules)

    edges: list[DependencyEdge] = []
    for module in modules:
        if module.language in ("java", "kotlin"):
            for raw_import in module.imports:
                for target in _resolve_jvm_import(raw_import, fqn_to_path, package_members):
                    if target != module.path:
                        edges.append(DependencyEdge(source=module.path, target=target))
            continue
        for raw_import in module.imports:
            target = None
            if module.language == "python":
                target = _resolve_python_import(module.path, raw_import, python_index)
            elif module.language in ("javascript", "typescript"):
                target = _resolve_js_import(module.path, raw_import, js_index)
            if target and target != module.path:
                edges.append(DependencyEdge(source=module.path, target=target))

    fan_out = Counter(e.source for e in edges)
    fan_in = Counter(e.target for e in edges)
    combined = Counter()
    for node, count in fan_in.items():
        combined[node] += count
    for node, count in fan_out.items():
        combined[node] += count
    hotspots = [node for node, _ in combined.most_common(HOTSPOT_LIMIT)]

    return DependencyGraph(
        edges=edges,
        fan_in=dict(fan_in),
        fan_out=dict(fan_out),
        hotspots=hotspots,
    )


def _build_python_index(modules: list[ModuleInfo]) -> dict[str, str]:
    """Maps dotted module path -> file relative_path, for Python modules only."""
    index: dict[str, str] = {}
    for m in modules:
        if m.language != "python":
            continue
        parts = PurePosixPath(m.path).with_suffix("").parts
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        dotted = ".".join(parts)
        if dotted:
            index[dotted] = m.path
    return index


def _resolve_python_import(source_path: str, raw_import: str, index: dict[str, str]) -> str | None:
    if raw_import.startswith("."):
        base_parts = list(PurePosixPath(source_path).with_suffix("").parts[:-1])
        level = len(raw_import) - len(raw_import.lstrip("."))
        for _ in range(level - 1):
            if base_parts:
                base_parts.pop()
        remainder = raw_import.lstrip(".")
        candidate_parts = base_parts + ([p for p in remainder.split(".") if p] if remainder else [])
        dotted = ".".join(candidate_parts)
        return index.get(dotted)

    if raw_import in index:
        return index[raw_import]
    # try progressively shorter prefixes (e.g. "pkg.sub.thing" -> "pkg.sub")
    parts = raw_import.split(".")
    while len(parts) > 1:
        parts.pop()
        candidate = ".".join(parts)
        if candidate in index:
            return index[candidate]
    return None


def _resolve_js_import(source_path: str, raw_import: str, known_paths: set[str]) -> str | None:
    if not raw_import.startswith("."):
        return None  # bare specifier -> external package, not internal
    base_dir = PurePosixPath(source_path).parent
    candidate = (base_dir / raw_import).as_posix()
    candidate = _normalize_posix(candidate)

    for suffix in ("", ".js", ".jsx", ".ts", ".tsx", "/index.js", "/index.ts"):
        probe = candidate + suffix
        if probe in known_paths:
            return probe
    return None


def _build_jvm_fqn_index(
    modules: list[ModuleInfo],
) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Maps FQN ("pkg.Class") -> file path, and package -> list of FQNs
    declared in that package, built from each module's real `package`
    declaration (never guessed from directory layout) plus its top-level
    type names — see ADR-022's package-declaration-index decision.

    If two modules declare the same FQN (e.g. a same-named nested type
    mis-attributed as top-level by jvm_parser.py's brace-depth-unaware
    regex — see L32), the later module in scan order wins; this is not
    detected or flagged here.
    """
    fqn_to_path: dict[str, str] = {}
    package_members: dict[str, list[str]] = {}
    for m in modules:
        if m.language not in ("java", "kotlin"):
            continue
        for name in m.classes:
            fqn = f"{m.package}.{name}" if m.package else name
            fqn_to_path[fqn] = m.path
            package_members.setdefault(m.package or "", []).append(fqn)
    return fqn_to_path, package_members


def _resolve_jvm_import(
    raw_import: str,
    fqn_to_path: dict[str, str],
    package_members: dict[str, list[str]],
) -> list[str]:
    """Resolves one Java/Kotlin import statement to zero, one, or many file
    paths. A wildcard import (`import a.b.*`) resolves to every class the
    FQN index knows about in package `a.b` — a genuinely different shape
    from every other language's single-target resolver in this file. An
    import this project's repo doesn't declare (JDK/stdlib, a third-party
    library, or an internal class jvm_parser.py failed to extract) simply
    resolves to an empty list — no warning, no exception — matching this
    file's existing fail-open convention for unresolved Python/JS imports.
    """
    if raw_import.endswith(".*"):
        package = raw_import[:-2]
        return [fqn_to_path[fqn] for fqn in package_members.get(package, [])]
    target = fqn_to_path.get(raw_import)
    return [target] if target else []


def _normalize_posix(path: str) -> str:
    parts: list[str] = []
    for part in path.split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part and part != ".":
            parts.append(part)
    return "/".join(parts)
