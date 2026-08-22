from engine import graph
from engine.models import ModuleInfo


def test_resolves_internal_python_import():
    modules = [
        ModuleInfo(path="pkg/a.py", language="python", docstring=None, imports=["pkg.b"]),
        ModuleInfo(path="pkg/b.py", language="python", docstring=None, imports=[]),
    ]

    g = graph.build_graph(modules)

    assert len(g.edges) == 1
    assert g.edges[0].source == "pkg/a.py"
    assert g.edges[0].target == "pkg/b.py"
    assert g.fan_in["pkg/b.py"] == 1
    assert g.fan_out["pkg/a.py"] == 1


def test_ignores_external_python_import():
    modules = [ModuleInfo(path="a.py", language="python", docstring=None, imports=["numpy"])]

    g = graph.build_graph(modules)

    assert g.edges == []


def test_resolves_relative_python_import():
    modules = [
        ModuleInfo(path="pkg/a.py", language="python", docstring=None, imports=[".b"]),
        ModuleInfo(path="pkg/b.py", language="python", docstring=None, imports=[]),
    ]

    g = graph.build_graph(modules)

    assert len(g.edges) == 1
    assert g.edges[0].target == "pkg/b.py"


def test_resolves_relative_js_import():
    modules = [
        ModuleInfo(path="src/a.js", language="javascript", docstring=None, imports=["./b"]),
        ModuleInfo(path="src/b.js", language="javascript", docstring=None, imports=[]),
    ]

    g = graph.build_graph(modules)

    assert len(g.edges) == 1
    assert g.edges[0].target == "src/b.js"


def test_ignores_bare_js_specifier():
    modules = [ModuleInfo(path="a.js", language="javascript", docstring=None, imports=["react"])]

    g = graph.build_graph(modules)

    assert g.edges == []


def test_hotspots_ranks_by_combined_degree():
    modules = [
        ModuleInfo(path="core.py", language="python", docstring=None, imports=[]),
        ModuleInfo(path="a.py", language="python", docstring=None, imports=["core"]),
        ModuleInfo(path="b.py", language="python", docstring=None, imports=["core"]),
        ModuleInfo(path="c.py", language="python", docstring=None, imports=["core"]),
    ]

    g = graph.build_graph(modules)

    assert g.hotspots[0] == "core.py"
