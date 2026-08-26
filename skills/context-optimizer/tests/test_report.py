import json

from engine.report import build_report


def _write_ci_report(tmp_path, files=None, modules=None, dependency_graph=None):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({
        "root_path": "/repo",
        "files": files if files is not None else [
            {"path": "engine/scanner.py", "language": "python", "size_bytes": 100, "line_count": 20},
        ],
        "modules": modules if modules is not None else [
            {"path": "engine/scanner.py", "docstring": "Scans the repo.",
             "functions": [], "classes": [], "imports": []},
        ],
        "dependency_graph": dependency_graph or {},
    }), encoding="utf-8")
    return path


def test_empty_task_description_produces_no_recommendations_and_a_warning(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    report = build_report("", str(ci_report))
    assert report.recommendations == []
    assert any("empty" in w.lower() for w in report.warnings)


def test_all_stopword_task_produces_warning_about_no_keywords(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    report = build_report("the a of it", str(ci_report))
    assert report.recommendations == []
    assert any("keyword" in w.lower() for w in report.warnings)


def test_zero_files_in_ci_report_produces_explicit_warning(tmp_path):
    ci_report = _write_ci_report(tmp_path, files=[], modules=[])
    report = build_report("scanner work", str(ci_report))
    assert report.recommendations == []
    assert any("zero files" in w.lower() for w in report.warnings)


def test_hotspot_match_lands_in_core_tier(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        dependency_graph={"fan_in": {"engine/scanner.py": 9}, "hotspots": ["engine/scanner.py"]},
    )
    report = build_report("fix the scanner module", str(ci_report))
    assert len(report.recommendations) == 1
    rec = report.recommendations[0]
    assert rec.path == "engine/scanner.py"
    assert rec.tier == "CORE"
    assert rec.is_hotspot is True


def test_low_fan_in_match_lands_in_supporting_tier(tmp_path):
    ci_report = _write_ci_report(
        tmp_path, dependency_graph={"fan_in": {"engine/scanner.py": 1}, "hotspots": []}
    )
    report = build_report("fix the scanner module", str(ci_report))
    assert len(report.recommendations) == 1
    assert report.recommendations[0].tier == "SUPPORTING"


def test_weak_single_field_match_still_recommended_not_dropped(tmp_path):
    """Fail-OPEN discipline (ADR-019): any nonzero score earns at least
    SUPPORTING — there is no secondary noise-reduction cutoff."""
    ci_report = _write_ci_report(
        tmp_path,
        files=[{"path": "engine/report.py", "language": "python", "size_bytes": 10, "line_count": 5}],
        modules=[{"path": "engine/report.py", "docstring": None, "functions": [], "classes": [],
                  "imports": ["engine.scanner"]}],
    )
    report = build_report("something about the scanner", str(ci_report))
    assert len(report.recommendations) == 1
    assert report.recommendations[0].tier == "SUPPORTING"


def test_word_boundary_regression_short_keyword_does_not_spuriously_match(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        files=[{"path": "engine/testability_scanner_utils.py", "language": "python",
                "size_bytes": 10, "line_count": 5}],
        modules=[{"path": "engine/testability_scanner_utils.py", "docstring": None,
                  "functions": [], "classes": [], "imports": []}],
    )
    report = build_report("please scan the repo", str(ci_report))
    assert report.recommendations == []


def test_budget_lines_flags_oversized_file(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        files=[{"path": "engine/scanner.py", "language": "python", "size_bytes": 100, "line_count": 500}],
    )
    report = build_report("scanner work", str(ci_report), budget_lines=50)
    assert len(report.recommendations) == 1
    assert report.recommendations[0].oversized_alone is True
    assert report.recommendations[0].tier != "EXCLUDED"
