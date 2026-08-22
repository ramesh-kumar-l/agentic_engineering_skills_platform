"""Parses unified diff text (git-style or plain) into a structured DiffContext.

Deterministic and stdlib-only. Does not interpret meaning — that is the
agent's job per the SKILL.md adversarial workflow.
"""

from __future__ import annotations

import re

from .models import DiffContext, DiffFile, Hunk, LineChange

_FILE_HEADER = re.compile(r"^diff --git a/(?P<old>.+) b/(?P<new>.+)$")
_OLD_PATH = re.compile(r"^--- (?P<path>.+)$")
_NEW_PATH = re.compile(r"^\+\+\+ (?P<path>.+)$")
_HUNK_HEADER = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@"
)


def _strip_prefix(path: str) -> str | None:
    path = path.strip()
    if path == "/dev/null":
        return None
    if path.startswith(("a/", "b/")):
        return path[2:]
    return path


def parse_diff(text: str) -> DiffContext:
    lines = text.splitlines()
    files: list[DiffFile] = []
    warnings: list[str] = []
    current_file: DiffFile | None = None
    current_hunk: Hunk | None = None
    old_lineno = 0
    new_lineno = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        header_match = _FILE_HEADER.match(line)
        if header_match:
            current_file = DiffFile(old_path=None, new_path=None)
            files.append(current_file)
            current_hunk = None
            i += 1
            continue

        old_match = _OLD_PATH.match(line)
        if old_match and current_file is not None:
            current_file.old_path = _strip_prefix(old_match.group("path"))
            i += 1
            continue

        new_match = _NEW_PATH.match(line)
        if new_match and current_file is not None:
            current_file.new_path = _strip_prefix(new_match.group("path"))
            if current_file.old_path is None:
                current_file.is_new_file = True
            if current_file.new_path is None:
                current_file.is_deleted_file = True
            i += 1
            continue

        hunk_match = _HUNK_HEADER.match(line)
        if hunk_match:
            if current_file is None:
                warnings.append(f"hunk header found before any file header: {line!r}")
                i += 1
                continue
            old_start = int(hunk_match.group("old_start"))
            new_start = int(hunk_match.group("new_start"))
            current_hunk = Hunk(
                old_start=old_start,
                old_count=int(hunk_match.group("old_count") or 1),
                new_start=new_start,
                new_count=int(hunk_match.group("new_count") or 1),
            )
            current_file.hunks.append(current_hunk)
            old_lineno = old_start
            new_lineno = new_start
            i += 1
            continue

        if current_hunk is not None and line.startswith("\\"):
            i += 1
            continue

        if current_hunk is not None and line.startswith("+"):
            current_hunk.lines.append(
                LineChange(kind="add", content=line[1:], new_lineno=new_lineno)
            )
            new_lineno += 1
            i += 1
            continue

        if current_hunk is not None and line.startswith("-"):
            current_hunk.lines.append(
                LineChange(kind="remove", content=line[1:], old_lineno=old_lineno)
            )
            old_lineno += 1
            i += 1
            continue

        if current_hunk is not None and line.startswith(" "):
            current_hunk.lines.append(
                LineChange(
                    kind="context",
                    content=line[1:],
                    old_lineno=old_lineno,
                    new_lineno=new_lineno,
                )
            )
            old_lineno += 1
            new_lineno += 1
            i += 1
            continue

        i += 1

    return DiffContext(files=files, warnings=warnings)
