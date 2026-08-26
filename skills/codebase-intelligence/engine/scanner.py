"""Repo walk: builds the file inventory and applies exclusion/security rules.

Security note: this module NEVER reads the contents of a file it classifies
as secret-shaped (see SECRET_NAME_PATTERNS). Those files are recorded only
as a warning (filename, nothing else) so the rest of the engine can never
leak their contents downstream.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from .models import FileInfo

DEFAULT_EXCLUDED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", "__pycache__",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".tox",
    "target", "vendor", ".idea", ".vscode", "coverage",
}

DEFAULT_MAX_FILE_SIZE_BYTES = 1_000_000  # 1 MB; larger files are skipped, not read

SECRET_NAME_PATTERNS = [
    re.compile(r"^\.env(\..*)?$", re.IGNORECASE),
    re.compile(r".*\.pem$", re.IGNORECASE),
    re.compile(r".*\.key$", re.IGNORECASE),
    re.compile(r"^credentials(\.json)?$", re.IGNORECASE),
    re.compile(r"^secrets?\.ya?ml$", re.IGNORECASE),
    re.compile(r"^id_rsa(\.pub)?$", re.IGNORECASE),
]

EXTENSION_LANGUAGE = {
    ".py": "python",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
    ".c": "c", ".h": "c",
    ".cpp": "cpp", ".hpp": "cpp",
    ".md": "markdown",
    ".json": "json",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".tar", ".gz",
    ".so", ".dll", ".dylib", ".exe", ".pyc", ".woff", ".woff2", ".ttf",
}


def is_secret_shaped(filename: str) -> bool:
    return any(p.match(filename) for p in SECRET_NAME_PATTERNS)


def detect_language(path: Path) -> str:
    return EXTENSION_LANGUAGE.get(path.suffix.lower(), "unknown")


def scan(
    root: Path,
    excluded_dirs: set[str] | None = None,
    max_file_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES,
) -> tuple[list[FileInfo], int, int, list[str]]:
    """Walk `root` and return (files, excluded_dir_count, skipped_file_count, warnings)."""
    excluded = excluded_dirs if excluded_dirs is not None else DEFAULT_EXCLUDED_DIRS
    files: list[FileInfo] = []
    warnings: list[str] = []
    excluded_dir_count = 0
    skipped_file_count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        kept_dirs = [
            d for d in dirnames
            if d not in excluded and not d.endswith(".egg-info")
        ]
        excluded_dir_count += len(dirnames) - len(kept_dirs)
        dirnames[:] = kept_dirs

        for filename in filenames:
            full_path = Path(dirpath) / filename

            if is_secret_shaped(filename):
                warnings.append(f"skipped secret-shaped file (not read): {full_path.relative_to(root).as_posix()}")
                skipped_file_count += 1
                continue

            if full_path.suffix.lower() in BINARY_EXTENSIONS:
                skipped_file_count += 1
                continue

            try:
                size = full_path.stat().st_size
            except OSError:
                skipped_file_count += 1
                continue

            if size > max_file_size_bytes:
                warnings.append(f"skipped oversized file (>{max_file_size_bytes}B): {full_path.relative_to(root).as_posix()}")
                skipped_file_count += 1
                continue

            line_count = _count_lines(full_path)
            files.append(FileInfo(
                path=full_path.relative_to(root).as_posix(),
                language=detect_language(full_path),
                size_bytes=size,
                line_count=line_count,
            ))

    return files, excluded_dir_count, skipped_file_count, warnings


def _count_lines(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0
