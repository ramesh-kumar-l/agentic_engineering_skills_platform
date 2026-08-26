from engine.models import CiDependencyGraph, CiModule, CiReportContext
from engine.target_resolver import resolve_file


def _ci_report():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(
                path="engine/report.py",
                docstring="Builds the report.",
                functions=["build_report"],
                classes=[],
                imports=[],
            ),
            CiModule(
                path="engine/cli.py",
                docstring="CLI entry point.",
                functions=["main"],
                classes=[],
                imports=["engine.report"],
            ),
            CiModule(
                path="engine/unrelated.py",
                docstring="Unrelated module.",
                functions=[],
                classes=["Widget"],
                imports=[],
            ),
        ],
        dependency_graph=CiDependencyGraph(
            fan_in={"engine/report.py": 1},
            fan_out={"engine/cli.py": 1},
            hotspots=["engine/unrelated.py"],
        ),
    )


def test_resolves_by_exact_path():
    assessment = resolve_file("engine/report.py", _ci_report())
    assert assessment.resolved_module_path == "engine/report.py"
    assert assessment.fan_in == 1


def test_resolves_by_stem_fallback_for_renamed_path():
    assessment = resolve_file("somewhere/else/report.py", _ci_report())
    assert assessment.resolved_module_path == "engine/report.py"


def test_unresolved_path_yields_default_assessment():
    assessment = resolve_file("does/not/exist.py", _ci_report())
    assert assessment.resolved_module_path is None
    assert assessment.fan_in == 0
    assert assessment.caller_modules == []


def test_none_path_yields_default_assessment():
    assessment = resolve_file(None, _ci_report())
    assert assessment.resolved_module_path is None


def test_finds_callers_via_imports():
    assessment = resolve_file("engine/report.py", _ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/cli.py" in caller_paths
    assert "engine/unrelated.py" not in caller_paths


def test_hotspot_flag_set_correctly():
    assessment = resolve_file("engine/unrelated.py", _ci_report())
    assert assessment.is_hotspot is True


def _stem_collision_ci_report():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/scanner.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="engine/testability_scanner.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["engine.decision_scanner"],
            ),
            CiModule(
                path="engine/cli.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["engine.scanner"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )


def test_caller_list_excludes_unrelated_module_that_merely_shares_a_stem_substring():
    """Regression test for L23's exact dogfood finding: a "scanner" target
    must not pick up "testability_scanner.py" as a caller just because
    "scanner" is a substring of its stem."""
    assessment = resolve_file("engine/scanner.py", _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/testability_scanner.py" not in caller_paths


def test_caller_list_still_includes_a_real_dotted_import_match():
    assessment = resolve_file("engine/scanner.py", _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/cli.py" in caller_paths
