"""Best-effort real-source excerpt for a named symbol (TEP Phase 5c).

Not a real parser: a bounded line-scan around the first textual occurrence
of `def <symbol>` / `class <symbol>` / `fun <symbol>`, falling back to a
bare occurrence of the symbol name. "A hint, not ground truth" -- the same
honesty standard already applied to jvm_parser.py's own regex-based
extraction. Deliberately does not attempt real brace/indent-depth parsing;
the authoring agent is expected to read the excerpt as a starting point,
not a guaranteed-complete symbol body. Read-only against the target repo,
same as every other engine in this portfolio.
"""

from __future__ import annotations

from pathlib import Path

_EXCERPT_LINES = 40
_DEF_NEEDLES = ("def {0}", "class {0}", "fun {0}")


def read_source_excerpt(repo_root: str, file: str, symbol: str | None) -> str | None:
    if symbol is None:
        return None

    path = Path(repo_root) / file
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None

    needles = [n.format(symbol) for n in _DEF_NEEDLES]
    start = None
    for i, line in enumerate(lines):
        if any(needle in line for needle in needles):
            start = i
            break

    if start is None:
        for i, line in enumerate(lines):
            if symbol in line:
                start = i
                break

    if start is None:
        return None

    end = min(len(lines), start + _EXCERPT_LINES)
    return "\n".join(lines[start:end])
