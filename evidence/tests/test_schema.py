from evidence.schema import SCHEMA_VERSION, RunProvenance


def _make_record(**overrides) -> RunProvenance:
    defaults = dict(
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
    defaults.update(overrides)
    return RunProvenance(**defaults)


def test_model_and_prompt_version_default_to_none():
    record = _make_record()
    assert record.model is None
    assert record.prompt_version is None


def test_round_trip_through_dict():
    record = _make_record(warnings=["a warning"])

    restored = RunProvenance.from_dict(record.to_dict())

    assert restored == record


def test_from_dict_ignores_unknown_fields():
    data = _make_record().to_dict()
    data["future_field_not_yet_defined"] = "should be ignored"

    restored = RunProvenance.from_dict(data)

    assert not hasattr(restored, "future_field_not_yet_defined")
