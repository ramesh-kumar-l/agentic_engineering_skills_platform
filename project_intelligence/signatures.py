"""Detection signature tables for TEP Phase 3 and TEP Phase 4.

General-purpose Python/JS/JVM signatures (Phase 3) plus a dedicated
Android test-framework table (Phase 4, `ANDROID_TEST_FRAMEWORK_SIGNATURES`)
covering exactly the trio TEP Phase 4's exit criteria names — JUnit,
Robolectric, Espresso. Kept as its own table/category rather than merged
into `TEST_FRAMEWORK_SIGNATURES`, so the profile can report presence/absence
of each of the three by name, not just "some test framework exists."

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

# TEP Phase 4 — the exact trio named in the exit criteria. "junit" also
# matches TEST_FRAMEWORK_SIGNATURES; that overlap is intentional (two
# separate lenses over the same evidence, same as build_systems/
# test_frameworks already can overlap on one dependency).
ANDROID_TEST_FRAMEWORK_SIGNATURES: dict[str, str] = {
    "junit": "JUnit",
    "robolectric": "Robolectric",
    "espresso-core": "Espresso",
    "espresso-contrib": "Espresso",
    "espresso-intents": "Espresso",
    "espresso-idling-resource": "Espresso",
    "espresso-web": "Espresso",
    "espresso-remote": "Espresso",
}

# Single source of truth for the named trio, used to compute explicit
# per-framework absence — never inferred from the signature table's keys,
# since that table has multiple keys per label (Espresso).
ANDROID_TARGET_FRAMEWORKS: tuple[str, ...] = ("JUnit", "Robolectric", "Espresso")
