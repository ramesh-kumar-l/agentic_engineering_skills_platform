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


def test_excludes_test_module_whose_import_merely_embeds_the_stem_substring():
    """Regression test for L24's dogfood finding: a "models" target must
    not be marked has_coverage-worthy by a test module whose import list
    merely contains "models" embedded inside a longer, unrelated
    identifier (e.g. "shared_models_cache"), not a real import of the
    target module itself."""
    ci_report = CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/models.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="tests/test_cache.py",
                docstring="",
                functions=["test_cache_behavior"],
                classes=[],
                imports=["shared_models_cache"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )
    assert find_test_coverage("engine/models.py", ci_report) == []


def test_still_finds_real_dotted_import_coverage_for_a_common_stem():
    ci_report = CiReportContext(
        root_path="/repo",
        modules=[
            CiModule(path="engine/models.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="tests/test_models.py",
                docstring="",
                functions=["test_model_fields"],
                classes=[],
                imports=["engine.models"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )
    assert find_test_coverage("engine/models.py", ci_report) == ["tests/test_models.py"]
