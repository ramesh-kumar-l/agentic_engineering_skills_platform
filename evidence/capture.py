"""Runs an existing skill's real CLI and captures a RunProvenance record.

The skill is invoked exactly as a human or agent would invoke it today
(`python -m engine.cli <target> --format json --out <dir>`, run as a
subprocess from the skill's own directory) — this module never imports a
skill's engine code directly, so capturing evidence never couples this
platform-level component to any one skill's internals.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from . import git_info, skill_info
from .schema import SCHEMA_VERSION, RunProvenance

_STDERR_EXCERPT_LIMIT = 500


def capture_run(skill_name: str, target_path: Path, skills_root: Path, artifacts_root: Path) -> RunProvenance:
    skill_dir = skill_info.resolve_skill_dir(skills_root, skill_name)
    skill_version = skill_info.get_skill_version(skill_dir)

    target_path = target_path.resolve()
    repo_commit, git_warning = git_info.get_git_commit(target_path)

    run_id = uuid.uuid4().hex
    output_dir = artifacts_root / skill_name / run_id
    started_at = datetime.now(UTC)

    proc = subprocess.run(
        [sys.executable, "-m", "engine.cli", str(target_path), "--format", "json", "--out", str(output_dir)],
        cwd=skill_dir,
        capture_output=True,
        text=True,
    )

    finished_at = datetime.now(UTC)
    duration_ms = int((finished_at - started_at).total_seconds() * 1000)

    warnings: list[str] = []
    if git_warning:
        warnings.append(git_warning)

    output_file = output_dir / "report.json"
    output_sha256: str | None = None
    output_relpath: str | None = None
    if output_file.is_file():
        output_sha256 = hashlib.sha256(output_file.read_bytes()).hexdigest()
        output_relpath = str(output_file.relative_to(artifacts_root).as_posix())
    elif proc.returncode == 0:
        warnings.append(f"exit code 0 but expected output file missing: {output_file}")

    if proc.returncode != 0 and proc.stderr:
        warnings.append(f"stderr: {proc.stderr.strip()[:_STDERR_EXCERPT_LIMIT]}")

    return RunProvenance(
        schema_version=SCHEMA_VERSION,
        run_id=run_id,
        skill_name=skill_name,
        skill_version=skill_version,
        repo_root=str(target_path),
        repo_commit=repo_commit,
        started_at=started_at.isoformat(),
        finished_at=finished_at.isoformat(),
        duration_ms=duration_ms,
        exit_code=proc.returncode,
        status="success" if proc.returncode == 0 else "failure",
        output_sha256=output_sha256,
        output_relpath=output_relpath,
        warnings=warnings,
    )
