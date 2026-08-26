import json
import subprocess
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/foo.py",
            "docstring": "Foo helper.",
            "functions": ["bar"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {"fan_in": {}, "fan_out": {}, "hotspots": []},
}

DIFF = """diff --git a/engine/foo.py b/engine/foo.py
--- a/engine/foo.py
+++ b/engine/foo.py
@@ -1,2 +1,2 @@
-def bar():
+def bar(x):
     pass
"""


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
    diff_file = tmp_path / "diff.txt"
    diff_file.write_text(DIFF, encoding="utf-8")
    result = _run_cli(
        [str(diff_file), "--ci-report", str(tmp_path / "does-not-exist.json")]
    )
    assert result.returncode == 1
    assert "error:" in result.stderr


def test_cli_errors_on_missing_diff_path(tmp_path):
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
    diff_file = tmp_path / "diff.txt"
    diff_file.write_text(DIFF, encoding="utf-8")
    out_dir = tmp_path / "out"

    result = _run_cli(
        [str(diff_file), "--ci-report", str(report_path), "--format", "both", "--out", str(out_dir)]
    )

    assert result.returncode == 0
    json_path = out_dir / "release-readiness-report.json"
    md_path = out_dir / "release-readiness-report.md"
    assert json_path.exists()
    assert md_path.exists()
    parsed = json.loads(json_path.read_text(encoding="utf-8"))
    assert parsed["files"][0]["structural"]["resolved_module_path"] == "engine/foo.py"
    assert "overall_verdict" in parsed


def test_cli_reads_diff_from_stdin():
    result = subprocess.run(
        [sys.executable, "-m", "engine.cli", "-", "--ci-report", "does-not-matter.json"],
        cwd=ENGINE_ROOT,
        input=DIFF,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "error:" in result.stderr


def test_cli_accepts_optional_regression_and_security_report_flags(tmp_path):
    report_path = tmp_path / "ci-report.json"
    report_path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    diff_file = tmp_path / "diff.txt"
    diff_file.write_text(DIFF, encoding="utf-8")
    regression_path = tmp_path / "regression-report.json"
    regression_path.write_text(json.dumps({"files": []}), encoding="utf-8")
    security_path = tmp_path / "security-report.json"
    security_path.write_text(
        json.dumps({"classification": {"sensitivity": "low", "suggested_verdict": "AUTHORIZE"}}),
        encoding="utf-8",
    )

    result = _run_cli(
        [
            str(diff_file),
            "--ci-report", str(report_path),
            "--regression-report", str(regression_path),
            "--security-report", str(security_path),
            "--format", "json",
        ]
    )
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert parsed["security_report_composed"] is True
