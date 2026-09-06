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

import importlib.util
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .models import ValidationOutcome

DEFAULT_TIMEOUT_SECONDS = 30
_EXCERPT_CHARS = 2000
_TAIL_READ_BYTES = _EXCERPT_CHARS * 4  # utf-8 multi-byte margin before the char slice

_PYTEST_EXTENSIONS = {".py"}
_JVM_EXTENSIONS = {".java", ".kt"}


class PytestUnavailableError(Exception):
    """Raised when pytest is not importable by sys.executable but a .py test needs it."""


def ensure_pytest_available() -> None:
    if importlib.util.find_spec("pytest") is None:
        raise PytestUnavailableError(
            f"pytest is not installed for this interpreter ({sys.executable}) — "
            "required at runtime to execute .py test files"
        )


def _tail_text(f) -> str:
    # Read back only the tail bytes needed for the excerpt, not the whole
    # file -- keeps excerpt extraction itself memory-bounded too.
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(max(0, size - _TAIL_READ_BYTES))
    return f.read().decode("utf-8", errors="replace")[-_EXCERPT_CHARS:]


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
    # stdout/stderr are redirected to disk-backed temp files rather than
    # captured in memory (capture_output=True) -- a runaway test printing
    # unbounded output before the timeout fires would otherwise exhaust
    # parent-process memory. By the time TimeoutExpired is raised the
    # child has already been killed and reaped, so these files safely
    # hold whatever was written before the kill.
    with tempfile.TemporaryFile() as out_f, tempfile.TemporaryFile() as err_f:
        try:
            result = subprocess.run(
                command,
                cwd=str(test_file.parent),
                env=env,
                stdout=out_f,
                stderr=err_f,
                timeout=timeout_seconds,
            )
            timed_out, exit_code = False, result.returncode
        except subprocess.TimeoutExpired:
            timed_out, exit_code = True, None

        return ValidationOutcome(
            test_file=str(test_file),
            framework=framework,
            command=command,
            exit_code=exit_code,
            passed=(not timed_out and exit_code == 0),
            timed_out=timed_out,
            stdout_excerpt=_tail_text(out_f),
            stderr_excerpt=_tail_text(err_f),
            duration_ms=int((time.monotonic() - start) * 1000),
        )
