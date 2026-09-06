from pathlib import Path

import pytest

from evidence.skill_info import UnknownSkillError, get_skill_version, resolve_skill_dir


def _make_skill(skills_root: Path, name: str, version: str | None) -> Path:
    skill_dir = skills_root / name
    (skill_dir / "engine").mkdir(parents=True)
    (skill_dir / "engine" / "cli.py").write_text("", encoding="utf-8")
    if version is not None:
        (skill_dir / "pyproject.toml").write_text(
            f'[project]\nname = "{name}"\nversion = "{version}"\n', encoding="utf-8"
        )
    return skill_dir


def test_resolve_skill_dir_finds_real_skill(tmp_path: Path):
    _make_skill(tmp_path, "fake-skill", "0.3.1")

    skill_dir = resolve_skill_dir(tmp_path, "fake-skill")

    assert skill_dir == tmp_path / "fake-skill"


def test_resolve_skill_dir_rejects_unknown_skill(tmp_path: Path):
    with pytest.raises(UnknownSkillError):
        resolve_skill_dir(tmp_path, "does-not-exist")


def test_get_skill_version_reads_pyproject(tmp_path: Path):
    skill_dir = _make_skill(tmp_path, "fake-skill", "0.3.1")

    assert get_skill_version(skill_dir) == "0.3.1"


def test_get_skill_version_missing_pyproject_returns_none(tmp_path: Path):
    skill_dir = _make_skill(tmp_path, "fake-skill", None)

    assert get_skill_version(skill_dir) is None
