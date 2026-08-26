"""Builds and runs a single step's real CLI invocation.

Owns the only `subprocess.run` call in this engine. Each step's skill is
invoked as `python -m engine.cli ...` with `cwd` set to that skill's own
directory (all skills are stdlib-only per ADR-006, so this needs no
install step beyond the repo already being checked out — disclosed as an
assumption that breaks silently if a future skill ever gains an external
dependency).

The first step in every template is always `codebase-intelligence`, whose
positional argument is the target repo *directory*, not a task-text file
— callers pass that path straight through as `positional_arg`. Every
downstream step's positional argument is a task/requirement text file,
built by `prepare_downstream_input` first.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from .models import StepResult, StepStatus, WiringMode, WorkflowStep

DEFAULT_TIMEOUT_SECONDS = 120


def prepare_downstream_input(
    step: WorkflowStep,
    task_text: str,
    upstream_output_path: Path | None,
    step_out_dir: Path,
) -> Path:
    """Writes this step's task/requirement text file, appending a
    codebase-intelligence excerpt when the step's wiring mode is
    TEXT_APPEND (reproduces Phase 3's real Pilot B composition, since
    acceptance-test-engineer's CLI has no --ci-report-style flag)."""
    step_out_dir.mkdir(parents=True, exist_ok=True)
    input_text = task_text
    if step.wiring_mode == WiringMode.TEXT_APPEND and upstream_output_path is not None:
        input_text = _append_ci_excerpt(task_text, upstream_output_path)
    task_file = step_out_dir / "input.txt"
    task_file.write_text(input_text, encoding="utf-8")
    return task_file


def _append_ci_excerpt(original_task_text: str, upstream_output_path: Path) -> str:
    try:
        data = json.loads(upstream_output_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return original_task_text

    file_count = data.get("file_count", "unknown")
    hotspots = data.get("dependency_graph", {}).get("hotspots", [])
    entry_points = [ep.get("path", "") for ep in data.get("entry_points", [])]

    excerpt_lines = [
        "",
        "## Codebase Intelligence context",
        f"- file_count: {file_count}",
        f"- hotspots: {', '.join(hotspots) if hotspots else '(none)'}",
        f"- entry_points: {', '.join(entry_points) if entry_points else '(none)'}",
        "",
    ]
    return original_task_text + "\n".join(excerpt_lines)


def build_argv(
    step: WorkflowStep,
    *,
    positional_arg: str,
    upstream_output_path: Path | None,
    step_out_dir: Path,
) -> list[str]:
    argv = [sys.executable, "-m", "engine.cli", positional_arg]
    if step.wiring_mode == WiringMode.CLI_FLAG and upstream_output_path is not None:
        if step.wiring_flag is None:
            raise ValueError(f"step {step.skill_name} declares CLI_FLAG with no flag name")
        argv += [step.wiring_flag, str(upstream_output_path)]
    argv += ["--format", "json", "--out", str(step_out_dir)]
    return argv


def run_step(
    step: WorkflowStep,
    *,
    skill_dir: Path,
    positional_arg: str,
    upstream_output_path: Path | None,
    step_out_dir: Path,
    dry_run: bool,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> StepResult:
    step_out_dir.mkdir(parents=True, exist_ok=True)
    argv = build_argv(
        step,
        positional_arg=positional_arg,
        upstream_output_path=upstream_output_path,
        step_out_dir=step_out_dir,
    )

    if dry_run:
        return StepResult(step=step, status=StepStatus.PENDING, output_path=None)

    start = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(skill_dir),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return StepResult(
            step=step,
            status=StepStatus.FAILED,
            duration_seconds=time.monotonic() - start,
            stderr_excerpt=f"timed out after {timeout_seconds}s",
        )
    duration = time.monotonic() - start

    output_path = step_out_dir / step.output_filename
    if proc.returncode != 0 or not output_path.exists():
        return StepResult(
            step=step,
            status=StepStatus.FAILED,
            exit_code=proc.returncode,
            duration_seconds=duration,
            stderr_excerpt=(proc.stderr or "")[-500:],
        )

    try:
        json.loads(output_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return StepResult(
            step=step,
            status=StepStatus.FAILED,
            exit_code=proc.returncode,
            duration_seconds=duration,
            stderr_excerpt=f"output was not valid JSON: {exc}",
        )

    return StepResult(
        step=step,
        status=StepStatus.OK,
        exit_code=proc.returncode,
        output_path=str(output_path),
        duration_seconds=duration,
    )
