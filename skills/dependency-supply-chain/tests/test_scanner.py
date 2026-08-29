from engine.models import CiExternalDependency
from engine.scanner import build_dependency_records, scan


def test_build_dependency_records_sets_pin_status():
    deps = [CiExternalDependency(name="a", version="1.0.0", source_file="requirements.txt")]
    records = build_dependency_records(deps)
    assert records[0].pin_status == "pinned"


def test_scan_flags_unpinned_dependency():
    deps = [CiExternalDependency(name="a", version=">=1.0", source_file="requirements.txt")]
    records, flags = scan(deps)
    assert len(records) == 1
    assert any(f.category == "unpinned-version" for f in flags)


def test_scan_flags_wildcard_as_high_severity():
    deps = [CiExternalDependency(name="a", version="*", source_file="requirements.txt")]
    _, flags = scan(deps)
    wildcard_flags = [f for f in flags if f.category == "wildcard-version"]
    assert len(wildcard_flags) == 1
    assert wildcard_flags[0].severity == "high"


def test_scan_flags_known_risk_name():
    deps = [CiExternalDependency(name="request", version="2.0.0", source_file="package.json")]
    _, flags = scan(deps)
    assert any(f.category == "known-risk-name" for f in flags)


def test_scan_flags_duplicate_conflicting_versions():
    deps = [
        CiExternalDependency(name="requests", version="==2.28.0", source_file="requirements.txt"),
        CiExternalDependency(name="requests", version=">=2.31", source_file="pyproject.toml"),
    ]
    _, flags = scan(deps)
    assert any(f.category == "duplicate-version" for f in flags)


def test_scan_produces_no_flags_for_clean_pinned_dependency():
    deps = [CiExternalDependency(name="totally-fine", version="1.0.0", source_file="requirements.txt")]
    _, flags = scan(deps)
    assert flags == []


def test_build_dependency_records_classifies_maven_range_via_ecosystem():
    deps = [CiExternalDependency(name="com.example:lib", version="[1.0,2.0)", source_file="pom.xml")]
    records = build_dependency_records(deps)
    assert records[0].pin_status == "range"


def test_build_dependency_records_classifies_gradle_dynamic_via_ecosystem():
    deps = [CiExternalDependency(name="com.example:lib", version="31.+", source_file="build.gradle")]
    records = build_dependency_records(deps)
    assert records[0].pin_status == "wildcard"
