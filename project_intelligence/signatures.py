"""Detection signature tables for TEP Phase 3.

Deliberately scoped to general-purpose Python/JS/JVM ecosystems only.
Android-specific frameworks (Robolectric, Espresso, AGP) are named in
TEP Phase 4's own exit criteria (project-memory-bank/18-test-engineering-
platform-contract.md) and are intentionally NOT added here — mixing them in
now would blur two separately-scoped phases' evidence.

Matching is exact-key only (see detect.py) against either a dependency's
full name (pip/npm style, e.g. "pytest-mock") or its artifact-id (the part
after the last ':' in a Maven/Gradle "group:artifact" coordinate, e.g.
"mockito-core" from "org.mockito:mockito-core") — never substring
containment, to avoid collisions like "pytest-mock" partially matching a
"pytest" key.
"""

from __future__ import annotations

# Manifest filename -> build system label. Root/scan-root-level presence
# only, matching external_deps.py's own existing scope (L2).
BUILD_SYSTEM_MANIFESTS: dict[str, str] = {
    "requirements.txt": "pip",
    "pyproject.toml": "python (pyproject.toml)",
    "package.json": "npm/yarn/pnpm (package.json)",
    "pom.xml": "Maven",
    "build.gradle": "Gradle",
    "build.gradle.kts": "Gradle (Kotlin DSL)",
}

TEST_FRAMEWORK_SIGNATURES: dict[str, str] = {
    "pytest": "pytest",
    "nose": "nose",
    "nose2": "nose2",
    "unittest2": "unittest2",
    "jest": "Jest",
    "mocha": "Mocha",
    "jasmine": "Jasmine",
    "ava": "AVA",
    "vitest": "Vitest",
    "junit": "JUnit",
    "junit-jupiter": "JUnit 5",
    "junit-jupiter-api": "JUnit 5",
    "testng": "TestNG",
}

MOCK_FRAMEWORK_SIGNATURES: dict[str, str] = {
    "mock": "mock (backport)",
    "pytest-mock": "pytest-mock",
    "responses": "responses (HTTP mocking)",
    "sinon": "Sinon.JS",
    "mockito-core": "Mockito",
    "mockito-inline": "Mockito",
    "easymock": "EasyMock",
    "powermock": "PowerMock",
}

COVERAGE_TOOL_SIGNATURES: dict[str, str] = {
    "coverage": "coverage.py",
    "pytest-cov": "pytest-cov",
    "nyc": "nyc (Istanbul)",
    "istanbul": "Istanbul",
    "c8": "c8",
    "jacoco-maven-plugin": "JaCoCo",
}
