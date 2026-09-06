"""Best-effort git commit lookup, without shelling out to a `git` binary.

Reads `.git/HEAD` and refs directly (pure stdlib, no subprocess dependency
on git being installed — consistent with ADR-006's stdlib-only default).
Returns (commit_sha, warning) — never raises; an unresolvable commit is
reported as a warning in the provenance record, not hidden or guessed.
"""

from __future__ import annotations

from pathlib import Path

_HEX40 = set("0123456789abcdef")


def get_git_commit(repo_root: Path) -> tuple[str | None, str | None]:
    git_dir = repo_root / ".git"
    head_file = git_dir / "HEAD"
    if not head_file.is_file():
        return None, f"no .git/HEAD found under {repo_root}"

    try:
        head = head_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return None, f"could not read .git/HEAD: {exc}"

    if head.startswith("ref: "):
        return _resolve_ref(git_dir, head[len("ref: "):].strip())

    if len(head) == 40 and set(head.lower()) <= _HEX40:
        return head, None  # detached HEAD: HEAD file holds the SHA directly

    return None, "unrecognized .git/HEAD format"


def _resolve_ref(git_dir: Path, ref_name: str) -> tuple[str | None, str | None]:
    loose_ref = git_dir / ref_name
    if loose_ref.is_file():
        try:
            return loose_ref.read_text(encoding="utf-8").strip(), None
        except OSError as exc:
            return None, f"could not read {loose_ref}: {exc}"

    packed = git_dir / "packed-refs"
    if packed.is_file():
        try:
            for line in packed.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.endswith(ref_name) and not line.startswith("#"):
                    return line.split()[0], None
        except OSError as exc:
            return None, f"could not read {packed}: {exc}"

    return None, f"ref {ref_name} not found in loose or packed refs"
