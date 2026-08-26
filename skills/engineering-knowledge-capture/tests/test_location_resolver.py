from engine.location_resolver import resolve_mention
from engine.models import CiDependencyGraph, CiModule, CiReportContext


def _ctx(modules, fan_in=None, hotspots=None):
    return CiReportContext(
        root_path="/repo",
        modules=modules,
        dependency_graph=CiDependencyGraph(fan_in=fan_in or {}, hotspots=hotspots or []),
    )


def test_no_modules_returns_none():
    ctx = _ctx([])
    assert resolve_mention("mentions the scanner module", ctx) is None


def test_no_matching_stem_returns_none():
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    assert resolve_mention("a totally unrelated sentence", ctx) is None


def test_matching_stem_resolves():
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    resolved = resolve_mention("the scanner module needs review", ctx)
    assert resolved is not None
    assert resolved.module_path == "engine/scanner.py"


def test_word_boundary_rejects_embedded_substring_match():
    """This is the exact L23 collision shape (project-memory-bank/
    12-known-limitations.md): a short stem embedded inside an unrelated,
    longer identifier must NOT match — the whole point of building this
    resolver with the fix from day one rather than the bare substring
    check the other three copies shipped with first."""
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    resolved = resolve_mention("the testability_scanner_utils helper is unrelated", ctx)
    assert resolved is None


def test_dotted_qualified_mention_still_resolves():
    ctx = _ctx([CiModule(path="engine/scanner.py", docstring=None)])
    resolved = resolve_mention("a bug in engine.scanner surfaced today", ctx)
    assert resolved is not None
    assert resolved.module_path == "engine/scanner.py"


def test_short_stem_below_minimum_length_is_skipped():
    ctx = _ctx([CiModule(path="engine/io.py", docstring=None)])
    resolved = resolve_mention("the io module was fine, no issues", ctx)
    assert resolved is None


def test_multiple_matches_prefers_hotspot():
    ctx = _ctx(
        [
            CiModule(path="engine/models.py", docstring=None),
            CiModule(path="skills/x/engine/models.py", docstring=None),
        ],
        hotspots=["skills/x/engine/models.py"],
    )
    resolved = resolve_mention("the models module needed a fix", ctx)
    assert resolved is not None
    assert resolved.module_path == "skills/x/engine/models.py"
    assert resolved.is_hotspot is True


def test_multiple_matches_prefers_higher_fan_in_when_neither_is_hotspot():
    ctx = _ctx(
        [
            CiModule(path="a/stats.py", docstring=None),
            CiModule(path="b/stats.py", docstring=None),
        ],
        fan_in={"a/stats.py": 1, "b/stats.py": 4},
    )
    resolved = resolve_mention("the stats module needed a fix", ctx)
    assert resolved is not None
    assert resolved.module_path == "b/stats.py"
    assert resolved.fan_in == 4
