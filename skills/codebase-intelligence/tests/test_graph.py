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


def test_resolves_jvm_import_via_package_index():
    modules = [
        ModuleInfo(path="src/main/java/com/example/App.java", language="java", docstring=None,
                   package="com.example", classes=["App"], imports=["com.example.Helper"]),
        ModuleInfo(path="src/main/java/com/example/Helper.java", language="java", docstring=None,
                   package="com.example", classes=["Helper"], imports=[]),
    ]

    g = graph.build_graph(modules)

    assert len(g.edges) == 1
    assert g.edges[0].source == "src/main/java/com/example/App.java"
    assert g.edges[0].target == "src/main/java/com/example/Helper.java"


def test_resolves_jvm_import_regardless_of_directory_layout():
    # Package-declaration index (ADR-022) must resolve correctly even when
    # the on-disk path does NOT mirror the package -- the exact failure mode
    # a directory-convention-guessing resolver would get wrong.
    modules = [
        ModuleInfo(path="weird/location/App.java", language="java", docstring=None,
                   package="com.example", classes=["App"], imports=["com.example.Helper"]),
        ModuleInfo(path="another/odd/spot/Helper.kt", language="kotlin", docstring=None,
                   package="com.example", classes=["Helper"], imports=[]),
    ]

    g = graph.build_graph(modules)

    assert len(g.edges) == 1
    assert g.edges[0].target == "another/odd/spot/Helper.kt"


def test_resolves_jvm_wildcard_import_to_every_class_in_package():
    modules = [
        ModuleInfo(path="App.java", language="java", docstring=None,
                   package="com.example", classes=["App"], imports=["com.example.models.*"]),
        ModuleInfo(path="models/Foo.java", language="java", docstring=None,
                   package="com.example.models", classes=["Foo"], imports=[]),
        ModuleInfo(path="models/Bar.kt", language="kotlin", docstring=None,
                   package="com.example.models", classes=["Bar"], imports=[]),
    ]

    g = graph.build_graph(modules)

    targets = {e.target for e in g.edges}
    assert targets == {"models/Foo.java", "models/Bar.kt"}


def test_ignores_unresolved_jvm_import():
    modules = [
        ModuleInfo(path="App.java", language="java", docstring=None,
                   package="com.example", classes=["App"], imports=["java.util.List"]),
    ]

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
