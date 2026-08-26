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
            CiModule(path="engine/models.py", docstring="", functions=[], classes=[], imports=[]),
            CiModule(
                path="engine/cache.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["shared_models_cache"],
            ),
            CiModule(
                path="engine/report.py",
                docstring="",
                functions=[],
                classes=[],
                imports=["engine.models"],
            ),
        ],
        dependency_graph=CiDependencyGraph(),
    )


def test_caller_list_excludes_module_whose_import_merely_embeds_the_stem_substring():
    """Regression test for L24's embedded-substring manifestation: a
    "models" target must not pick up "shared_models_cache" as a caller
    just because "models" is a substring of that identifier."""
    assessment = resolve_file("engine/models.py", _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/cache.py" not in caller_paths


def test_caller_list_still_includes_a_real_dotted_import_match():
    assessment = resolve_file("engine/models.py", _stem_collision_ci_report())
    caller_paths = [c.path for c in assessment.caller_modules]
    assert "engine/report.py" in caller_paths
