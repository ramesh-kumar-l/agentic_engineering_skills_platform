from engine.models import CiDependencyGraph, CiModule, CiReportContext, RefactorTarget
from engine.target_resolver import resolve_target, resolve_targets


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
            hotspots=[],
        ),
    )


def test_resolves_by_module_stem():
    target = RefactorTarget(name="report.py")
    assessment = resolve_target(target, _ci_report())
    assert assessment.resolved_module_path == "engine/report.py"


def test_resolves_by_function_name():
    target = RefactorTarget(name="build_report")
    assessment = resolve_target(target, _ci_report())
    assert assessment.resolved_module_path == "engine/report.py"
    assert "build_report" in assessment.matched_functions


def test_resolves_by_class_name():
    target = RefactorTarget(name="Widget")
    assessment = resolve_target(target, _ci_report())
    assert assessment.resolved_module_path == "engine/unrelated.py"
    assert "Widget" in assessment.matched_classes


def test_unresolved_target_has_no_module_path():
    target = RefactorTarget(name="does_not_exist_anywhere")
    assessment = resolve_target(target, _ci_report())
    assert assessment.resolved_module_path is None
    assert assessment.caller_modules == []


def test_finds_callers_via_imports():
    target = RefactorTarget(name="report.py")
    assessment = resolve_target(target, _ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/cli.py" in caller_paths
    assert "engine/unrelated.py" not in caller_paths


def test_resolve_targets_resolves_each_independently():
    targets = [RefactorTarget(name="report.py"), RefactorTarget(name="nope")]
    assessments = resolve_targets(targets, _ci_report())
    assert assessments[0].resolved_module_path == "engine/report.py"
    assert assessments[1].resolved_module_path is None


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
    """Regression test for L14/L19/L21/L23: a "scanner" target must not pick
    up "testability_scanner.py" as a caller just because "scanner" is a
    substring of its stem."""
    target = RefactorTarget(name="scanner.py")
    assessment = resolve_target(target, _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/testability_scanner.py" not in caller_paths


def test_caller_list_still_includes_a_real_dotted_import_match():
    target = RefactorTarget(name="scanner.py")
    assessment = resolve_target(target, _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/cli.py" in caller_paths
