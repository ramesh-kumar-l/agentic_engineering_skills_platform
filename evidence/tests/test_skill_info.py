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


def test_resolve_skill_dir_rejects_dot_dot_traversal(tmp_path: Path):
    skills_root = tmp_path / "skills"
    skills_root.mkdir()
    _make_skill(tmp_path, "secret", "0.0.1")  # sibling of skills_root, not under it

    with pytest.raises(UnknownSkillError):
        resolve_skill_dir(skills_root, "../secret")


def test_resolve_skill_dir_rejects_absolute_path_skill_name(tmp_path: Path):
    skills_root = tmp_path / "skills"
    skills_root.mkdir()
    secret_dir = _make_skill(tmp_path, "secret", "0.0.1")

    with pytest.raises(UnknownSkillError):
        resolve_skill_dir(skills_root, str(secret_dir))


def test_resolve_skill_dir_rejects_symlink_escape(tmp_path: Path):
    skills_root = tmp_path / "skills"
    skills_root.mkdir()
    secret_dir = _make_skill(tmp_path, "secret", "0.0.1")
    link = skills_root / "linked-skill"
    try:
        link.symlink_to(secret_dir, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation not permitted in this environment")

    with pytest.raises(UnknownSkillError):
        resolve_skill_dir(skills_root, "linked-skill")
