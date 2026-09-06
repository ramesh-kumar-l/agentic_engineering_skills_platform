"""Executes an agent-authored test file against the target repo via
subprocess (TEP Phase 5c) -- this platform's first execution capability.
Every other skill, and every TEP package before this one, is pure static
analysis; this module is not.

Explicit disclosure, not a claim of secure isolation: this provides a
process-level timeout only. It does not sandbox the filesystem or network
-- executing a generated test here carries exactly the same risk as
running that same file inside the target repo's own CI, no additional
isolation is added.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

from .models import ValidationOutcome

DEFAULT_TIMEOUT_SECONDS = 30
_EXCERPT_CHARS = 2000

_PYTEST_EXTENSIONS = {".py"}
_JVM_EXTENSIONS = {".java", ".kt"}


def _build_command(test_file: Path) -> list[str] | None:
    if test_file.suffix in _PYTEST_EXTENSIONS:
        return [sys.executable, "-m", "pytest", str(test_file), "-q"]
    if test_file.suffix in _JVM_EXTENSIONS:
        # No build-system invocation attempted here -- a real Maven/Gradle
        # run needs the target repo's own build file, out of scope for a
        # single loose test file. Disclosed as unsupported, not guessed at.
        return None
    return None


def run_validation(
    test_file: Path,
    repo_root: str,
    framework: str | None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> ValidationOutcome:
    # Resolve to absolute paths up front: the subprocess below runs with
    # cwd set to test_file.parent, so a relative test_file or repo_root
    # (e.g. "." from the caller's own cwd) would silently resolve against
    # the wrong directory once cwd changes -- a real bug this project's
    # own dogfooding caught (see examples/test-validation/example-run.md).
    test_file = Path(test_file).resolve()
    repo_root = str(Path(repo_root).resolve())

    command = _build_command(test_file)
    if command is None:
        return ValidationOutcome(
            test_file=str(test_file),
            framework=framework,
            command=[],
            exit_code=None,
            passed=False,
            timed_out=False,
            stdout_excerpt="",
            stderr_excerpt=(
                f"no supported runner for {test_file.suffix} files — "
                "only Python (pytest) is executed in this version"
            ),
            duration_ms=0,
        )

    env = dict(os.environ)
    env["PYTHONPATH"] = repo_root + os.pathsep + env.get("PYTHONPATH", "")

    start = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=str(test_file.parent),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return ValidationOutcome(
            test_file=str(test_file),
            framework=framework,
            command=command,
            exit_code=result.returncode,
            passed=result.returncode == 0,
            timed_out=False,
            stdout_excerpt=result.stdout[-_EXCERPT_CHARS:],
            stderr_excerpt=result.stderr[-_EXCERPT_CHARS:],
            duration_ms=int((time.monotonic() - start) * 1000),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return ValidationOutcome(
            test_file=str(test_file),
            framework=framework,
            command=command,
            exit_code=None,
            passed=False,
            timed_out=True,
            stdout_excerpt=stdout[-_EXCERPT_CHARS:],
            stderr_excerpt=stderr[-_EXCERPT_CHARS:],
            duration_ms=int((time.monotonic() - start) * 1000),
        )
