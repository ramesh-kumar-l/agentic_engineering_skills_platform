from pathlib import Path

from evidence.git_info import get_git_commit


def test_no_git_dir_returns_none_with_warning(tmp_path: Path):
    commit, warning = get_git_commit(tmp_path)
    assert commit is None
    assert "no .git/HEAD" in warning


def test_detached_head_sha_read_directly(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    sha = "a" * 40
    (tmp_path / ".git" / "HEAD").write_text(sha, encoding="utf-8")

    commit, warning = get_git_commit(tmp_path)

    assert commit == sha
    assert warning is None


def test_symbolic_ref_resolved_via_loose_ref(tmp_path: Path):
    git_dir = tmp_path / ".git"
    (git_dir / "refs" / "heads").mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    sha = "b" * 40
    (git_dir / "refs" / "heads" / "main").write_text(sha + "\n", encoding="utf-8")

    commit, warning = get_git_commit(tmp_path)

    assert commit == sha
    assert warning is None


def test_symbolic_ref_resolved_via_packed_refs(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    sha = "c" * 40
    (git_dir / "packed-refs").write_text(f"# comment\n{sha} refs/heads/main\n", encoding="utf-8")

    commit, warning = get_git_commit(tmp_path)

    assert commit == sha
    assert warning is None


def test_unresolvable_ref_reports_warning(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/missing\n", encoding="utf-8")

    commit, warning = get_git_commit(tmp_path)

    assert commit is None
    assert "not found" in warning
