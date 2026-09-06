from pathlib import Path

from evidence.schema import SCHEMA_VERSION, RunProvenance
from evidence.store import load, save


def _make_record() -> RunProvenance:
    return RunProvenance(
        schema_version=SCHEMA_VERSION,
        run_id="abc123",
        skill_name="codebase-intelligence",
        skill_version="0.2.0",
        repo_root="/tmp/target",
        repo_commit="deadbeef",
        started_at="2026-09-06T00:00:00+00:00",
        finished_at="2026-09-06T00:00:01+00:00",
        duration_ms=1000,
        exit_code=0,
        status="success",
        output_sha256="hash",
        output_relpath="codebase-intelligence/abc123/report.json",
    )


def test_save_writes_under_skill_subdir(tmp_path: Path):
    record = _make_record()

    out_path = save(record, tmp_path)

    assert out_path == tmp_path / "codebase-intelligence" / "abc123.json"
    assert out_path.is_file()


def test_save_then_load_round_trips(tmp_path: Path):
    record = _make_record()

    out_path = save(record, tmp_path)
    restored = load(out_path)

    assert restored == record
