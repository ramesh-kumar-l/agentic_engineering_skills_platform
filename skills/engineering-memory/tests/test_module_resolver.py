from engine.models import CiDependencyGraph, CiModule, CiReportContext, ModuleFlag
from engine.module_resolver import resolve_module_mentions


def _ctx(modules, fan_in=None, hotspots=None):
    return CiReportContext(
        root_path="/repo",
        modules=modules,
        dependency_graph=CiDependencyGraph(fan_in=fan_in or {}, hotspots=hotspots or []),
    )


def test_exact_basename_match_resolves():
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    flags = resolve_module_mentions(["engine/scanner.py"], ctx)
    assert flags == [ModuleFlag(module_path="engine/scanner.py", exists=True, is_hotspot=False, fan_in=0)]


def test_basename_only_mention_resolves_to_full_path():
    ctx = _ctx([CiModule(path="skills/x/engine/scanner.py", docstring=None)])
    flags = resolve_module_mentions(["scanner.py"], ctx)
    assert flags[0].exists is True
    assert flags[0].module_path == "skills/x/engine/scanner.py"


def test_no_match_flags_not_exists():
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    flags = resolve_module_mentions(["nonexistent_module.py"], ctx)
    assert flags == [ModuleFlag(module_path="nonexistent_module.py", exists=False)]


def test_substring_does_not_false_match():
    """The L23/L24 class: a short basename must never match via
    containment — `io.py` must not match `studio.py`. This resolver uses
    exact basename equality, so there is no containment check to fail."""
    ctx = _ctx([CiModule(path="engine/studio.py", docstring=None)])
    flags = resolve_module_mentions(["io.py"], ctx)
    assert flags[0].exists is False


def test_hotspot_and_fan_in_surfaced():
    ctx = _ctx(
        [CiModule(path="engine/hot.py", docstring=None)],
        fan_in={"engine/hot.py": 9},
        hotspots=["engine/hot.py"],
    )
    flags = resolve_module_mentions(["hot.py"], ctx)
    assert flags[0].is_hotspot is True
    assert flags[0].fan_in == 9


def test_empty_mentions_returns_empty_list():
    ctx = _ctx([])
    assert resolve_module_mentions([], ctx) == []


def test_multiple_mentions_preserve_order():
    ctx = _ctx([CiModule(path="a/one.py", docstring=None), CiModule(path="b/two.py", docstring=None)])
    flags = resolve_module_mentions(["two.py", "one.py", "missing.py"], ctx)
    assert [f.module_path for f in flags] == ["b/two.py", "a/one.py", "missing.py"]
    assert [f.exists for f in flags] == [True, True, False]
