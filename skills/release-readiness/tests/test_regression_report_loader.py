import json

from engine.regression_report_loader import load_regression_evidence

SAMPLE = {
    "files": [
        {
            "file": "engine/foo.py",
            "overall_risk_tier": "high",
            "diff_pattern_flags": [{"pattern_id": "removed-exception-handling"}],
        },
        {"file": "engine/bar.py", "overall_risk_tier": "low", "diff_pattern_flags": []},
    ]
}


def test_none_path_yields_no_evidence_no_warning():
    evidence, warnings = load_regression_evidence(None)
    assert evidence == {}
    assert warnings == []


def test_missing_path_yields_warning_not_failure(tmp_path):
    evidence, warnings = load_regression_evidence(tmp_path / "nope.json")
    assert evidence == {}
    assert warnings
    assert "does not exist" in warnings[0]


def test_malformed_json_yields_warning_not_failure(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    evidence, warnings = load_regression_evidence(path)
    assert evidence == {}
    assert "not valid JSON" in warnings[0]


def test_loads_per_file_evidence(tmp_path):
    path = tmp_path / "regression-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    evidence, warnings = load_regression_evidence(path)

    assert warnings == []
    assert evidence["engine/foo.py"].available is True
    assert evidence["engine/foo.py"].overall_risk_tier == "high"
    assert evidence["engine/foo.py"].diff_pattern_flag_count == 1
    assert evidence["engine/bar.py"].diff_pattern_flag_count == 0


def test_empty_files_list_yields_warning(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text(json.dumps({"files": []}), encoding="utf-8")
    evidence, warnings = load_regression_evidence(path)
    assert evidence == {}
    assert warnings
