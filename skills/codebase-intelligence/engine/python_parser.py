"""AST-based structural parsing for Python files.

Only structure is extracted (imports, def/class names, docstrings) — never
full file contents — so downstream consumers get a condensed context object,
not a repo dump (see NFR2 in project-memory-bank/02-requirements.md).
"""

from __future__ import annotations

import ast
from pathlib import Path

from .models import ModuleInfo


def parse_python_file(root: Path, relative_path: str) -> ModuleInfo:
    full_path = root / relative_path
    try:
        source = full_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source, filename=relative_path)
    except (SyntaxError, ValueError, OSError) as exc:
        return ModuleInfo(
            path=relative_path,
            language="python",
            docstring=None,
            parse_error=f"{type(exc).__name__}: {exc}",
        )

    docstring = ast.get_docstring(tree)
    functions: list[str] = []
    classes: list[str] = []
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            if _is_top_level(node, tree):
                functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            if _is_top_level(node, tree):
                classes.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            if node.module:
                imports.append(f"{prefix}{node.module}")
            else:
                # "from . import sibling" — the imported names ARE the targets
                imports.extend(f"{prefix}{alias.name}" for alias in node.names)

    return ModuleInfo(
        path=relative_path,
        language="python",
        docstring=docstring,
        functions=functions,
        classes=classes,
        imports=imports,
        has_main_guard=_has_main_guard(tree),
    )


def _is_top_level(node: ast.AST, tree: ast.Module) -> bool:
    return node in tree.body


def _has_main_guard(tree: ast.Module) -> bool:
    """AST-verified `if __name__ == "__main__":` at module top level.

    Deliberately NOT a text/substring search: a file that merely mentions
    `__main__` in a docstring, comment, or string literal (e.g. this very
    module, or a test asserting on that string) must not be misclassified
    as an entry point. Caught by dogfooding the engine on its own repo.
    """
    for node in tree.body:
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not isinstance(test, ast.Compare) or len(test.ops) != 1:
            continue
        if not isinstance(test.ops[0], ast.Eq):
            continue
        left, right = test.left, test.comparators[0]
        names = {left, right}
        has_dunder_name = any(isinstance(n, ast.Name) and n.id == "__name__" for n in names)
        has_main_literal = any(
            isinstance(n, ast.Constant) and n.value == "__main__" for n in names
        )
        if has_dunder_name and has_main_literal:
            return True
    return False
