from engine.duplicate_detector import find_duplicate_conflicts
from engine.models import CiExternalDependency


def test_flags_same_name_conflicting_versions_across_manifests():
    deps = [
        CiExternalDependency(name="requests", version="==2.28.0", source_file="requirements.txt"),
        CiExternalDependency(name="requests", version=">=2.31", source_file="pyproject.toml"),
    ]
    flags = find_duplicate_conflicts(deps)
    assert len(flags) == 1
    assert flags[0].category == "duplicate-version"
    assert flags[0].dependency_name == "requests"


def test_no_flag_when_versions_agree():
    deps = [
        CiExternalDependency(name="requests", version="2.28.0", source_file="requirements.txt"),
        CiExternalDependency(name="requests", version="2.28.0", source_file="pyproject.toml"),
    ]
    assert find_duplicate_conflicts(deps) == []


def test_no_flag_for_single_declaration():
    deps = [CiExternalDependency(name="requests", version="2.28.0", source_file="requirements.txt")]
    assert find_duplicate_conflicts(deps) == []


def test_name_matching_is_case_insensitive():
    deps = [
        CiExternalDependency(name="Flask", version="2.0.0", source_file="requirements.txt"),
        CiExternalDependency(name="flask", version="3.0.0", source_file="pyproject.toml"),
    ]
    flags = find_duplicate_conflicts(deps)
    assert len(flags) == 1
