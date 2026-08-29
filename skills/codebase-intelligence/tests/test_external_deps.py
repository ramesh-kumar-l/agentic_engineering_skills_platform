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


def test_parses_pom_xml_dependencies(tmp_path: Path):
    (tmp_path / "pom.xml").write_text(
        "<project>\n"
        "  <dependencies>\n"
        "    <dependency>\n"
        "      <groupId>com.google.guava</groupId>\n"
        "      <artifactId>guava</artifactId>\n"
        "      <version>31.1-jre</version>\n"
        "    </dependency>\n"
        "  </dependencies>\n"
        "</project>\n",
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    assert len(deps) == 1
    assert deps[0].name == "com.google.guava:guava"
    assert deps[0].version == "31.1-jre"
    assert deps[0].source_file == "pom.xml"


def test_parses_namespaced_pom_xml_dependencies(tmp_path: Path):
    (tmp_path / "pom.xml").write_text(
        '<project xmlns="http://maven.apache.org/POM/4.0.0">\n'
        "  <dependencies>\n"
        "    <dependency>\n"
        "      <groupId>junit</groupId>\n"
        "      <artifactId>junit</artifactId>\n"
        "      <version>4.13.2</version>\n"
        "    </dependency>\n"
        "  </dependencies>\n"
        "</project>\n",
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    names = {d.name for d in deps}
    assert names == {"junit:junit"}


def test_parses_gradle_groovy_dependencies(tmp_path: Path):
    (tmp_path / "build.gradle").write_text(
        "dependencies {\n"
        "    implementation 'com.google.guava:guava:31.1-jre'\n"
        "    testImplementation 'junit:junit:4.13.2'\n"
        "}\n",
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    names = {d.name for d in deps}
    assert names == {"com.google.guava:guava", "junit:junit"}
    assert all(d.source_file == "build.gradle" for d in deps)


def test_parses_gradle_kts_dependencies(tmp_path: Path):
    (tmp_path / "build.gradle.kts").write_text(
        'dependencies {\n'
        '    implementation("com.google.guava:guava:31.1-jre")\n'
        "}\n",
        encoding="utf-8",
    )

    deps = external_deps.parse_external_dependencies(tmp_path)

    assert len(deps) == 1
    assert deps[0].version == "31.1-jre"
    assert deps[0].source_file == "build.gradle.kts"
