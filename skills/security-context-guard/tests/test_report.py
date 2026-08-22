import json

from engine.report import build_report


def test_build_report_clean_input_authorizes():
    report = build_report("Ordinary content.", "Read the README file.", [])
    assert report.classification.suggested_verdict == "AUTHORIZE"
    assert report.warnings == []


def test_build_report_flags_secret_in_content():
    report = build_report('api_key = "sk_live_abcdef123456"', "Read a file.", [])
    assert report.stats.secret_count == 1
    assert report.classification.sensitivity == "high"


def test_build_report_warns_on_fully_empty_input():
    report = build_report("", "", [])
    assert any("nothing to classify" in w.lower() for w in report.warnings)


def test_build_report_with_no_ci_report_produces_no_hotspot_note():
    report = build_report("content", "Read a file.", ["engine/report.py"], ci_report_path=None)
    assert not any("hotspot" in w.lower() for w in report.warnings)


def test_build_report_with_unreadable_ci_report_warns_but_does_not_fail(tmp_path):
    missing_path = str(tmp_path / "does-not-exist.json")
    report = build_report("content", "Read a file.", ["engine/report.py"], ci_report_path=missing_path)
    assert any("could not read" in w.lower() for w in report.warnings)
    assert report.classification is not None


def test_build_report_with_ci_report_flags_touched_hotspot(tmp_path):
    ci_report_path = tmp_path / "report.json"
    ci_report_path.write_text(
        json.dumps({"dependency_graph": {"hotspots": ["engine/report.py"]}}), encoding="utf-8"
    )
    report = build_report("content", "Read a file.", ["engine/report.py"], ci_report_path=str(ci_report_path))
    assert any("hotspot" in w.lower() for w in report.warnings)
