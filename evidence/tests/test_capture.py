from pathlib import Path

from evidence.capture import capture_run

_FAKE_CLI_SUCCESS = """
import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("--format")
parser.add_argument("--out", type=Path)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
(args.out / "report.json").write_text(json.dumps({"analyzed": str(args.path)}), encoding="utf-8")
"""

_FAKE_CLI_FAILURE = """
import sys
print("something went wrong", file=sys.stderr)
sys.exit(1)
"""


def _make_fake_skill(skills_root: Path, name: str, cli_source: str) -> None:
    engine_dir = skills_root / name / "engine"
    engine_dir.mkdir(parents=True)
    (engine_dir / "__init__.py").write_text("", encoding="utf-8")
    (engine_dir / "cli.py").write_text(cli_source, encoding="utf-8")


def test_capture_run_success_records_output_hash(tmp_path: Path):
    skills_root = tmp_path / "skills"
    target = tmp_path / "target-repo"
    target.mkdir()
    artifacts_root = tmp_path / "artifacts"
    _make_fake_skill(skills_root, "fake-skill", _FAKE_CLI_SUCCESS)

    record = capture_run("fake-skill", target, skills_root, artifacts_root)

    assert record.status == "success"
    assert record.exit_code == 0
    assert record.output_sha256 is not None
    assert record.output_relpath is not None
    assert (artifacts_root / record.output_relpath).is_file()
    assert record.repo_commit is None  # no .git under target
    assert any("no .git/HEAD" in w for w in record.warnings)


def test_capture_run_failure_records_stderr(tmp_path: Path):
    skills_root = tmp_path / "skills"
    target = tmp_path / "target-repo"
    target.mkdir()
    artifacts_root = tmp_path / "artifacts"
    _make_fake_skill(skills_root, "fake-skill", _FAKE_CLI_FAILURE)

    record = capture_run("fake-skill", target, skills_root, artifacts_root)

    assert record.status == "failure"
    assert record.exit_code == 1
    assert record.output_sha256 is None
    assert any("something went wrong" in w for w in record.warnings)
