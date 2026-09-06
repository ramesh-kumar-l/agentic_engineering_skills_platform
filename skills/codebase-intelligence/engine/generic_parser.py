"""Heuristic (regex-based) import extraction for non-Python, non-JVM languages.

KNOWN LIMITATION (see project-memory-bank/12-known-limitations.md): this is
not a real parser. It pattern-matches common import syntaxes for JS/TS and
Go. It will miss dynamic imports, re-exports, and unusual formatting. Treat
its output as a hint, not ground truth. Java/Kotlin are parsed separately by
jvm_parser.py, which also extracts package declarations and type names.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import ModuleInfo

_JS_IMPORT = re.compile(r"""(?:import\s+.*?from\s+|require\()\s*['"]([^'"]+)['"]""")
_GO_IMPORT = re.compile(r'"([\w./-]+)"')

PATTERNS_BY_LANGUAGE = {
    "javascript": _JS_IMPORT,
    "typescript": _JS_IMPORT,
}


def parse_generic_file(root: Path, relative_path: str, language: str) -> ModuleInfo:
    full_path = root / relative_path
    try:
        source = full_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return ModuleInfo(path=relative_path, language=language, docstring=None,
                           parse_error=f"{type(exc).__name__}: {exc}")

    pattern = PATTERNS_BY_LANGUAGE.get(language)
    imports = pattern.findall(source) if pattern else []

    return ModuleInfo(
        path=relative_path,
        language=language,
        docstring=None,
        imports=imports,
    )
