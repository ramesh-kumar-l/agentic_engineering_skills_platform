"""Resolves an existing skill's directory and declared version.

Deliberately does not import a skill's `engine` package (ADR-010's
precedent: a consumer defines its own lightweight view rather than coupling
to another component's internals, so every skill stays independently
packaged and versioned, per ADR-006). The skill is treated as a black box
invoked via its own documented CLI (`python -m engine.cli`).
"""

from __future__ import annotations

import re
from pathlib import Path

_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)


class UnknownSkillError(Exception):
    pass


def resolve_skill_dir(skills_root: Path, skill_name: str) -> Path:
    skill_dir = skills_root / skill_name
    cli_module = skill_dir / "engine" / "cli.py"
    if not cli_module.is_file():
        raise UnknownSkillError(
            f"{skill_name!r} has no engine/cli.py under {skills_root} — "
            "not a runnable skill by this platform's own CLI convention"
        )
    return skill_dir


def get_skill_version(skill_dir: Path) -> str | None:
    pyproject = skill_dir / "pyproject.toml"
    if not pyproject.is_file():
        return None
    try:
        text = pyproject.read_text(encoding="utf-8")
    except OSError:
        return None
    match = _VERSION_RE.search(text)
    return match.group(1) if match else None
