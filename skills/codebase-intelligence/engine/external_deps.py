"""Parses external (third-party) dependency manifests.

Stdlib-only by design: uses a small manual TOML scan instead of `tomllib`
so the engine works on Python 3.10+ without a version-dependent import.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .models import ExternalDependency

_REQUIREMENTS_LINE = re.compile(r"^([A-Za-z0-9_.\-]+)\s*([<>=!~]=?[\w.\*]+)?")
_PYPROJECT_DEP_LINE = re.compile(r'^\s*"?([A-Za-z0-9_.\-]+)\s*([<>=!~]=?[\w.\*,\s]*)?"?\s*,?\s*$')

# Common single-line string-notation Gradle dependency declaration, e.g.
#   implementation("com.google.guava:guava:31.1-jre")
#   testImplementation 'junit:junit:4.13.2'
# Deliberately scoped to this one common shape — version catalogs
# (libs.versions.toml), map-notation, variable interpolation, and
# multi-module settings.gradle coordination are out of scope (see
# project-memory-bank/12-known-limitations.md, L33).
_GRADLE_DEP = re.compile(
    r'^\s*(?:implementation|api|compileOnly|runtimeOnly|testImplementation|'
    r'testRuntimeOnly|annotationProcessor|kapt|ksp|androidTestImplementation)'
    r'[\s(]+["\']([\w.\-]+):([\w.\-]+):([\w.\-+]+)["\']',
    re.MULTILINE,
)


def parse_external_dependencies(root: Path) -> list[ExternalDependency]:
    deps: list[ExternalDependency] = []
    deps.extend(_parse_requirements_txt(root))
    deps.extend(_parse_pyproject_toml(root))
    deps.extend(_parse_package_json(root))
    deps.extend(_parse_pom_xml(root))
    deps.extend(_parse_gradle(root))
    return deps


def _parse_requirements_txt(root: Path) -> list[ExternalDependency]:
    path = root / "requirements.txt"
    if not path.exists():
        return []
    deps = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        match = _REQUIREMENTS_LINE.match(line)
        if match:
            deps.append(ExternalDependency(
                name=match.group(1), version=match.group(2), source_file="requirements.txt"
            ))
    return deps


def _parse_pyproject_toml(root: Path) -> list[ExternalDependency]:
    path = root / "pyproject.toml"
    if not path.exists():
        return []
    deps = []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    in_deps_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dependencies") and "=" in stripped and "[" in stripped:
            in_deps_block = True
            continue
        if in_deps_block:
            if stripped.startswith("]"):
                in_deps_block = False
                continue
            match = _PYPROJECT_DEP_LINE.match(stripped)
            if match and match.group(1):
                deps.append(ExternalDependency(
                    name=match.group(1),
                    version=(match.group(2) or "").strip() or None,
                    source_file="pyproject.toml",
                ))
    return deps


def _parse_package_json(root: Path) -> list[ExternalDependency]:
    path = root / "package.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except (json.JSONDecodeError, OSError):
        return []
    deps = []
    for section in ("dependencies", "devDependencies"):
        for name, version in data.get(section, {}).items():
            deps.append(ExternalDependency(name=name, version=version, source_file="package.json"))
    return deps


def _parse_pom_xml(root: Path) -> list[ExternalDependency]:
    """Parses the project's direct <dependencies> block only — not
    <dependencyManagement> (version declarations, not necessarily-used
    dependencies) and not <profiles>/.../<dependencies> (conditionally
    active) — the same "scope to the primary block, disclose the rest"
    precedent _parse_pyproject_toml set for [project.dependencies] alone.
    See project-memory-bank/12-known-limitations.md, L33.
    """
    path = root / "pom.xml"
    if not path.exists():
        return []
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return []
    deps = []
    # `{*}` wildcard namespace match (ElementTree, Python 3.8+) handles both
    # namespaced (xmlns="http://maven.apache.org/POM/4.0.0") and bare pom.xml
    # fixtures without manually stripping the namespace.
    for dep_el in tree.getroot().findall("./{*}dependencies/{*}dependency"):
        group_id = _pom_child_text(dep_el, "groupId")
        artifact_id = _pom_child_text(dep_el, "artifactId")
        version = _pom_child_text(dep_el, "version")
        if not artifact_id:
            continue
        name = f"{group_id}:{artifact_id}" if group_id else artifact_id
        deps.append(ExternalDependency(name=name, version=version, source_file="pom.xml"))
    return deps


def _pom_child_text(parent: ET.Element, local_name: str) -> str | None:
    el = parent.find(f"{{*}}{local_name}")
    return el.text.strip() if el is not None and el.text else None


def _parse_gradle(root: Path) -> list[ExternalDependency]:
    """Root-level build.gradle/build.gradle.kts only; single-line
    string-notation dependencies on common configuration names only — see
    _GRADLE_DEP's docstring and L33 for the full scope boundary.
    """
    deps: list[ExternalDependency] = []
    for filename in ("build.gradle", "build.gradle.kts"):
        path = root / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for group_id, artifact_id, version in _GRADLE_DEP.findall(text):
            deps.append(ExternalDependency(
                name=f"{group_id}:{artifact_id}", version=version, source_file=filename,
            ))
    return deps
