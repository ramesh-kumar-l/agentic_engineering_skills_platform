import pytest

from engine.skill_locator import SkillNotFoundError, resolve_skill_dir


def test_resolves_a_real_skill_directory():
    skill_dir = resolve_skill_dir("codebase-intelligence")
    assert skill_dir.name == "codebase-intelligence"
    assert (skill_dir / "engine" / "cli.py").exists()


def test_raises_on_unknown_skill_name():
    with pytest.raises(SkillNotFoundError):
        resolve_skill_dir("does-not-exist-skill")


def test_raises_when_engine_cli_missing(tmp_path):
    (tmp_path / "skills" / "empty-skill").mkdir(parents=True)
    with pytest.raises(SkillNotFoundError):
        resolve_skill_dir("empty-skill", platform_root=tmp_path)


def test_uses_explicit_platform_root(tmp_path):
    skill_dir = tmp_path / "skills" / "fake-skill" / "engine"
    skill_dir.mkdir(parents=True)
    (skill_dir / "cli.py").write_text("", encoding="utf-8")
    resolved = resolve_skill_dir("fake-skill", platform_root=tmp_path)
    assert resolved == tmp_path / "skills" / "fake-skill"
