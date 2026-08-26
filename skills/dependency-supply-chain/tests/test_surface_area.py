from engine.models import DependencyRecord
from engine.surface_area import compute_surface_area


def test_empty_list_produces_zeroed_stats():
    stats = compute_surface_area([])
    assert stats.total_dependencies == 0
    assert stats.unpinned_count == 0
    assert stats.unpinned_percentage == 0.0


def test_counts_and_percentage():
    records = [
        DependencyRecord(name="a", version="1.0.0", source_file="requirements.txt", pin_status="pinned"),
        DependencyRecord(name="b", version=">=1.0", source_file="requirements.txt", pin_status="range"),
        DependencyRecord(name="c", version=None, source_file="pyproject.toml", pin_status="missing"),
        DependencyRecord(name="d", version="1.0.0", source_file="pyproject.toml", pin_status="pinned"),
    ]
    stats = compute_surface_area(records)
    assert stats.total_dependencies == 4
    assert stats.unpinned_count == 2
    assert stats.unpinned_percentage == 50.0
    assert stats.manifest_breakdown == {"requirements.txt": 2, "pyproject.toml": 2}
