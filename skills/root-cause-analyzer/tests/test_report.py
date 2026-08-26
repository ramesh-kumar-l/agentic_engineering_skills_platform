import json
from pathlib import Path

from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/cart.py",
            "docstring": "Cart total computation.",
            "functions": ["total"],
            "classes": [],
            "imports": [],
        }
    ],
    "dependency_graph": {"fan_in": {}, "fan_out": {}, "hotspots": []},
}


def _write_report(tmp_path: Path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_assembles_stats_flags_and_candidates(tmp_path):
    report = build_report(
        "Expected the cart total to be 10 but got 0 instead. Steps to "
        'reproduce: add an item. Error: File "engine/cart.py", line 12, in total',
        _write_report(tmp_path),
    )
    assert report.stats.word_count > 0
    assert len(report.candidates.candidates) == 1
    assert report.candidates.candidates[0].path == "engine/cart.py"
    assert report.candidates.candidates[0].evidence_tier == "stack-trace"
    assert report.warnings == []


def test_empty_symptom_and_no_matches_produce_warnings(tmp_path):
    report = build_report("", _write_report(tmp_path))
    assert any("empty" in w for w in report.warnings)
    assert any("No modules" in w for w in report.warnings)


def test_stack_frame_with_no_matching_module_produces_warning(tmp_path):
    report = build_report(
        'File "vendor/other_repo/file.py", line 1, in run', _write_report(tmp_path)
    )
    assert any("did not match" in w or "no module" in w.lower() or "different repo" in w for w in report.warnings) or any(
        "none of their paths matched" in w for w in report.warnings
    )
