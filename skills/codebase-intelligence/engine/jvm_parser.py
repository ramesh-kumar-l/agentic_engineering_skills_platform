"""Regex-based structural parsing for Java and Kotlin files.

Java and Kotlin share enough package/import/type-declaration syntax that
one module serves both languages — the same "one engine, language param"
shape as generic_parser.py. Unlike generic_parser.py's import-only regex,
this module also extracts the real `package` declaration and top-level
type/function names, needed both for the FQN index (graph.py's JVM
resolver, ADR-022) and for entry-point detection (report.py).

KNOWN LIMITATION (see project-memory-bank/12-known-limitations.md, L32):
this is regex-based, not a real parser — it does not track brace depth. A
nested/inner class or interface is indistinguishable from a top-level one,
so it can be mis-recorded into the FQN index as if it were top-level.
Treat its output as a hint, not ground truth — same standing caveat as
generic_parser.py.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import ModuleInfo

_PACKAGE = re.compile(r"^\s*package\s+([\w.]+)\s*;?\s*$", re.MULTILINE)
_IMPORT = re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+(?:\.\*)?)\s*;?\s*$", re.MULTILINE)

# Top-level class/interface/enum/object declarations. Deliberately does NOT
# track brace depth (regex, not a real parser) -- see module known limitation.
_TYPE_DECL = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|open|abstract|final|"
    r"sealed|data|annotation)\s+)*"
    r"(?:class|interface|enum(?:\s+class)?|object)\s+(\w+)",
    re.MULTILINE,
)

# Kotlin top-level function declarations (needed for `fun main()` entry-point
# detection and for completeness of the module's "functions" list).
_KOTLIN_FUN_DECL = re.compile(
    r"^\s*(?:(?:public|private|internal|protected|suspend|inline|override)\s+)*"
    r"fun\s+(\w+)\s*\(",
    re.MULTILINE,
)

_JAVA_MAIN = re.compile(
    r"^\s*(?:(?:public|static|final)\s+){2,}void\s+main\s*\(\s*String",
    re.MULTILINE,
)
_KOTLIN_MAIN = re.compile(
    r"^\s*(?:(?:public|private|internal)\s+)*fun\s+main\s*\(",
    re.MULTILINE,
)


def parse_jvm_file(root: Path, relative_path: str, language: str) -> ModuleInfo:
    full_path = root / relative_path
    try:
        source = full_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return ModuleInfo(path=relative_path, language=language, docstring=None,
                           parse_error=f"{type(exc).__name__}: {exc}")

    package_match = _PACKAGE.search(source)
    package = package_match.group(1) if package_match else None

    imports = _IMPORT.findall(source)
    classes = _TYPE_DECL.findall(source)
    functions = _KOTLIN_FUN_DECL.findall(source) if language == "kotlin" else []

    main_regex = _JAVA_MAIN if language == "java" else _KOTLIN_MAIN
    has_main = bool(main_regex.search(source))

    return ModuleInfo(
        path=relative_path,
        language=language,
        docstring=None,
        functions=functions,
        classes=classes,
        imports=imports,
        has_main_guard=has_main,
        package=package,
    )
