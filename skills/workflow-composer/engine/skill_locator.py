"""Resolves a registry skill name to its real, on-disk engine directory.

Fails closed: a registry-named skill directory that doesn't exist raises
rather than letting the executor silently skip or fabricate a step.
"""

from __future__ import annotations

from pathlib import Path


class SkillNotFoundError(Exception):
    pass


def _platform_root() -> Path:
    # skills/workflow-composer/engine/skill_locator.py -> platform root
    return Path(__file__).resolve().parents[3]


def resolve_skill_dir(skill_name: str, platform_root: Path | None = None) -> Path:
    root = platform_root if platform_root is not None else _platform_root()
    skill_dir = root / "skills" / skill_name
    if not (skill_dir / "engine" / "cli.py").exists():
        raise SkillNotFoundError(
            f"skill '{skill_name}' not found under {root / 'skills'} "
            f"(expected engine/cli.py)"
        )
    return skill_dir
