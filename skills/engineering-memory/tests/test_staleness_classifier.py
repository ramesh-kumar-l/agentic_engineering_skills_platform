from engine.models import MemoryRecord, ModuleFlag, RecordStatus
from engine.staleness_classifier import classify_staleness


def _record(status):
    return MemoryRecord(
        record_id="L1", record_type="limitation", title="t", body="b",
        source_file="x.md", source_line=1, status=status,
    )


def test_fixed_status_flags_stale():
    flag = classify_staleness(_record(RecordStatus.FIXED), [])
    assert flag.is_stale is True
    assert "FIXED" in flag.reason


def test_superseded_status_flags_stale():
    flag = classify_staleness(_record(RecordStatus.SUPERSEDED), [])
    assert flag.is_stale is True
    assert "SUPERSEDED" in flag.reason


def test_active_with_no_module_flags_is_not_stale():
    flag = classify_staleness(_record(RecordStatus.ACTIVE), [])
    assert flag.is_stale is False


def test_active_with_missing_module_flags_stale():
    flags = [ModuleFlag(module_path="gone.py", exists=False)]
    flag = classify_staleness(_record(RecordStatus.ACTIVE), flags)
    assert flag.is_stale is True
    assert "gone.py" in flag.reason


def test_active_with_existing_module_is_not_stale():
    flags = [ModuleFlag(module_path="real.py", exists=True, fan_in=3)]
    flag = classify_staleness(_record(RecordStatus.ACTIVE), flags)
    assert flag.is_stale is False


def test_fixed_status_wins_over_existing_module():
    flags = [ModuleFlag(module_path="real.py", exists=True, fan_in=3)]
    flag = classify_staleness(_record(RecordStatus.FIXED), flags)
    assert flag.is_stale is True
    assert "FIXED" in flag.reason
