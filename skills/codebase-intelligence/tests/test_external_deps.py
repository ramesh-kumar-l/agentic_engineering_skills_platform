import json
from pathlib import Path

from engine import external_deps


def test_parses_requirements_txt(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text(
        "requests==2.31.0\n# a comment\n\nflask>=2.0\nnoversion\n", encoding="utf-8"
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    names = {d.name for d in deps}
    assert names == {"requests", "flask", "noversion"}
    assert all(d.source_file == "requirements.txt" for d in deps)


def test_parses_package_json(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"dependencies": {"react": "^18.0.0"}, "devDependencies": {"jest": "^29.0.0"}}),
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    names = {d.name for d in deps}
    assert names == {"react", "jest"}


def test_no_manifests_returns_empty(tmp_path: Path):
    assert external_deps.parse_external_dependencies(tmp_path) == []


def test_parses_pyproject_toml_dependencies(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = [\n    "requests>=2.0",\n    "click",\n]\n',
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    names = {d.name for d in deps}
    assert names == {"requests", "click"}
