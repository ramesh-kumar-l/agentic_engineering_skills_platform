"""Chains the 6-stage TEP pipeline into one call: codebase-intelligence ->
regression-hunter -> project_intelligence -> test_strategy -> scenario_planner
-> test_generation. Each stage is invoked exactly as already documented in
AndroidGuide.md, as a real subprocess against this platform's own checkout --
this module orchestrates the existing CLIs, it never reimplements or imports
their internals directly, and none of those packages are modified by it.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


class PipelineStageError(Exception):
    pass


def _platform_root() -> Path:
    env = os.environ.get("TEP_PLATFORM_ROOT")
    if env:
        return Path(env)
    # engine/pipeline.py -> test-case-generator -> skills -> platform root
    return Path(__file__).resolve().parents[3]


def _run(argv: list[str], cwd: Path, input_text: str | None = None) -> None:
    result = subprocess.run(
        argv, cwd=cwd, input=input_text, text=True, capture_output=True
    )
    if result.returncode != 0:
        raise PipelineStageError(
            f"stage failed ({' '.join(argv)}) in {cwd}:\n{result.stderr.strip()}"
        )


def run_pipeline(repo_path: Path, diff_text: str, out_dir: Path) -> Path:
    root = _platform_root()
    ci_out = out_dir / "ci"
    rh_out = out_dir / "rh"
    pi_out = out_dir / "pi"
    ts_out = out_dir / "ts"
    sp_out = out_dir / "sp"
    tg_out = out_dir / "tg"

    _run(
        [sys.executable, "-m", "engine.cli", str(repo_path),
         "--format", "json", "--out", str(ci_out)],
        cwd=root / "skills" / "codebase-intelligence",
    )
    ci_report = ci_out / "report.json"

    _run(
        [sys.executable, "-m", "engine.cli", "-", "--ci-report", str(ci_report),
         "--format", "json", "--out", str(rh_out)],
        cwd=root / "skills" / "regression-hunter",
        input_text=diff_text,
    )
    rh_report = rh_out / "regression-hunter-report.json"

    _run(
        [sys.executable, "-m", "project_intelligence.cli", str(ci_report),
         "--out", str(pi_out)],
        cwd=root,
    )
    pi_report = pi_out / "test-environment-profile.json"

    _run(
        [sys.executable, "-m", "test_strategy.cli", str(rh_report), str(pi_report),
         "--out", str(ts_out)],
        cwd=root,
    )
    ts_report = ts_out / "test-strategy-report.json"

    _run(
        [sys.executable, "-m", "scenario_planner.cli", str(ts_report), str(rh_report),
         str(ci_report), "--out", str(sp_out)],
        cwd=root,
    )
    sp_report = sp_out / "scenario-plan-report.json"

    _run(
        [sys.executable, "-m", "test_generation.cli", str(sp_report), str(repo_path),
         "--out", str(tg_out)],
        cwd=root,
    )
    return tg_out / "generation-plan-report.json"
