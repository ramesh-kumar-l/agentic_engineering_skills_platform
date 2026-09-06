from project_intelligence.ci_report_loader import CiExternalDependency, CiReportContext
from project_intelligence.detect import (
    detect_build_systems,
    detect_coverage_tools,
    detect_mock_frameworks,
    detect_test_frameworks,
)


def _ctx(deps, top_level_filenames=()) -> CiReportContext:
    return CiReportContext(
        root_path="/tmp/target",
        language_breakdown={"python": 1},
        external_dependencies=deps,
        top_level_filenames=list(top_level_filenames),
    )


def test_pytest_detected_as_test_framework_not_confused_with_pytest_mock():
    ctx = _ctx([
        CiExternalDependency(name="pytest", source_file="pyproject.toml"),
        CiExternalDependency(name="pytest-mock", source_file="pyproject.toml"),
    ])

    test_frameworks = detect_test_frameworks(ctx)
    mock_frameworks = detect_mock_frameworks(ctx)

    assert [f.name for f in test_frameworks] == ["pytest"]
    assert [f.name for f in mock_frameworks] == ["pytest-mock"]


def test_maven_coordinate_matches_via_artifact_id():
    ctx = _ctx([CiExternalDependency(name="org.mockito:mockito-core", source_file="pom.xml")])

    findings = detect_mock_frameworks(ctx)

    assert len(findings) == 1
    assert findings[0].name == "Mockito"
    assert findings[0].evidence == ["org.mockito:mockito-core"]


def test_coverage_tool_detection():
    ctx = _ctx([CiExternalDependency(name="pytest-cov", source_file="pyproject.toml")])

    findings = detect_coverage_tools(ctx)

    assert [f.name for f in findings] == ["pytest-cov"]


def test_build_system_dependency_confirmed_when_deps_present():
    ctx = _ctx([CiExternalDependency(name="pytest", source_file="pyproject.toml")])

    findings = detect_build_systems(ctx)

    assert len(findings) == 1
    assert findings[0].name == "python (pyproject.toml)"
    assert findings[0].confidence == "dependency-confirmed"
    assert findings[0].evidence == ["pytest"]


def test_build_system_manifest_only_when_manifest_present_but_no_deps():
    ctx = _ctx([], top_level_filenames=["pyproject.toml"])

    findings = detect_build_systems(ctx)

    assert len(findings) == 1
    assert findings[0].name == "python (pyproject.toml)"
    assert findings[0].confidence == "manifest-only"
    assert findings[0].evidence == ["pyproject.toml"]


def test_build_system_absent_when_no_manifest_and_no_deps():
    ctx = _ctx([])

    findings = detect_build_systems(ctx)

    assert findings == []


def test_no_findings_when_no_matching_dependencies():
    ctx = _ctx([CiExternalDependency(name="some-unrelated-lib", source_file="requirements.txt")])

    assert detect_test_frameworks(ctx) == []
    assert detect_mock_frameworks(ctx) == []
    assert detect_coverage_tools(ctx) == []
