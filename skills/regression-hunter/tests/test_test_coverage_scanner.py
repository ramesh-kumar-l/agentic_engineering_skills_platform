from engine.models import CiDependencyGraph, CiModule, CiReportContext
from engine.test_coverage_scanner import find_test_coverage


def _ci_report():
    return CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/report.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="tests/test_report.py",
                docstring="",
                functions=["test_build_report"],
                classes=[],
                imports=["engine.report"],
            ),
            CiModule(
                path="tests/test_unrelated.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["engine.cli"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )


def test_finds_covering_test_module():
    covering = find_test_coverage("engine/report.py", _ci_report())
    assert covering == ["tests/test_report.py"]


def test_none_when_no_test_imports_target():
    covering = find_test_coverage("engine/lonely.py", _ci_report())
    assert covering == []


def test_none_when_target_unresolved():
    assert find_test_coverage(None, _ci_report()) == []


def test_ignores_non_test_modules_even_if_they_import_target():
    ci_report = CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/report.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="engine/cli.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["engine.report"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )
    assert find_test_coverage("engine/report.py", ci_report) == []
