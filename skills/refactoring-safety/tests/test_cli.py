import json
import subprocess
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/report.py",
            "docstring": "Builds the report.",
            "functions": ["build_report"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {"fan_in": {}, "fan_out": {}, "hotspots": []},
}


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "engine.cli", *args],
        cwd=ENGINE_ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_requires_ci_report_flag():
    result = _run_cli(["-"])
    assert result.returncode != 0
    assert "--ci-report" in result.stderr


def test_cli_errors_on_missing_ci_report(tmp_path):
    refactor = tmp_path / "refactor.txt"
    refactor.write_text("Rename `report.py` to `builder.py`.", encoding="utf-8")
    result = _run_cli(
        [str(refactor), "--ci-report", str(tmp_path / "does-not-exist.json")]
    )
    assert result.returncode == 1
    assert "error:" in result.stderr


def test_cli_errors_on_missing_refactor_path(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    result = _run_cli(
        [str(tmp_path / "no-such-file.txt"), "--ci-report", str(report_path)]
    )
    assert result.returncode == 1
    assert "does not exist" in result.stderr


def test_cli_writes_json_and_markdown_to_out_dir(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    refactor = tmp_path / "refactor.txt"
    refactor.write_text("Rename `report.py` to `builder.py`.", encoding="utf-8")
    out_dir = tmp_path / "out"

    result = _run_cli(
        [str(refactor), "--ci-report", str(report_path), "--format", "both", "--out", str(out_dir)]
    )

    assert result.returncode == 0
    json_path = out_dir / "refactoring-safety-report.json"
    md_path = out_dir / "refactoring-safety-report.md"
    assert json_path.exists()
    assert md_path.exists()
    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert parsed["targets"][0]["resolved_module_path"] == "engine/report.py"


def test_cli_reads_refactor_from_stdin():
    result = subprocess.run(
        [sys.executable, "-m", "engine.cli", "-", "--ci-report", "does-not-matter.json"],
        cwd=ENGINE_ROOT,
        input="Rename `report.py` to `builder.py`.",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "error:" in result.stderr
