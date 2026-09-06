"""The real end-to-end test for this skill: builds a minimal, real git repo
with one staged change and runs engine.cli against it for real -- no mocking,
no stubbed pipeline stages. Proves the 6-stage subprocess chain (each stage's
--out threaded into the next) is wired correctly, without touching
test_generation/ or any other existing package's internals.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from engine.cli import main


def _git(repo: Path, *args: str) -> None:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def _build_repo(repo: Path) -> None:
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    calc = repo / "calc.py"
    calc.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    _git(repo, "add", "calc.py")
    _git(repo, "commit", "-m", "initial")

    calc.write_text(
        "def add(a, b):\n    return a + b\n\n\ndef subtract(a, b):\n    return a - b\n",
        encoding="utf-8",
    )
    _git(repo, "add", "calc.py")  # staged, not committed


def test_pipeline_runs_end_to_end_against_a_staged_change(tmp_path):
    repo = tmp_path / "fixture-repo"
    _build_repo(repo)

    out_dir = tmp_path / "out"
    exit_code = main([str(repo), "--out", str(out_dir)])
    assert exit_code == 0

    report_path = out_dir / "tg" / "generation-plan-report.json"
    assert report_path.exists()

    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(data["specs"]) >= 1
    assert any(spec["target_symbol"] == "subtract" for spec in data["specs"])
    subtract_spec = next(s for s in data["specs"] if s["target_symbol"] == "subtract")
    assert subtract_spec["positive_slot"]["kind"] == "positive"
    assert len(subtract_spec["negative_slots"]) == 5
