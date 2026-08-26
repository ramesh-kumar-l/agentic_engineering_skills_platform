import json

from engine.report import build_report


def _write_ci_report(tmp_path, modules=None, fan_in=None, hotspots=None):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({
        "root_path": "/repo",
        "modules": modules or [],
        "dependency_graph": {"fan_in": fan_in or {}, "hotspots": hotspots or []},
    }), encoding="utf-8")
    return path


def test_clean_narrative_produces_no_candidates_and_no_warnings(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        modules=[{"path": "engine/foo.py", "docstring": None, "functions": [], "classes": [], "imports": []}],
    )
    report = build_report("Status update: nothing new to report.", str(ci_report))
    assert report.candidates == []
    assert report.warnings == []


def test_empty_narrative_warns(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    report = build_report("   ", str(ci_report))
    assert any("empty" in w.lower() for w in report.warnings)


def test_zero_modules_forces_medium_priority_and_warns(tmp_path):
    ci_report = _write_ci_report(tmp_path, modules=[])
    report = build_report("We decided to defer the retry-logic rewrite.", str(ci_report))
    assert len(report.candidates) == 1
    assert report.candidates[0].suggested_capture_priority == "MEDIUM"
    assert report.candidates[0].resolved_module_path is None
    assert any("zero modules" in w for w in report.warnings)


def test_hotspot_mention_resolves_and_scores_high(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        modules=[{"path": "engine/scanner.py", "docstring": None, "functions": [], "classes": [], "imports": []}],
        fan_in={"engine/scanner.py": 8},
        hotspots=["engine/scanner.py"],
    )
    narrative = "We decided that the scanner module's regex table needs periodic review."
    report = build_report(narrative, str(ci_report))
    assert len(report.candidates) == 1
    candidate = report.candidates[0]
    assert candidate.resolved_module_path == "engine/scanner.py"
    assert candidate.suggested_capture_priority == "HIGH"


def test_full_pipeline_stats_match_candidate_count(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    narrative = (
        "We decided to keep things simple.\n"
        "Turns out that decision caused a regression.\n"
    )
    report = build_report(narrative, str(ci_report))
    assert report.stats.candidate_count == len(report.candidates) == 2
