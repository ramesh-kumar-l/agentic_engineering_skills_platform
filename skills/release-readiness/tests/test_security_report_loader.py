import json

from engine.security_report_loader import load_security_evidence

SAMPLE = {
    "classification": {
        "sensitivity": "high",
        "suggested_verdict": "REQUIRES_HUMAN_APPROVAL",
    }
}


def test_none_path_yields_unavailable_evidence_no_warning():
    evidence, warnings = load_security_evidence(None)
    assert evidence.available is False
    assert warnings == []


def test_missing_path_yields_warning_not_failure(tmp_path):
    evidence, warnings = load_security_evidence(tmp_path / "nope.json")
    assert evidence.available is False
    assert warnings
    assert "does not exist" in warnings[0]


def test_malformed_json_yields_warning_not_failure(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    evidence, warnings = load_security_evidence(path)
    assert evidence.available is False
    assert "not valid JSON" in warnings[0]


def test_missing_classification_field_yields_warning(tmp_path):
    path = tmp_path / "no-classification.json"
    path.write_text(json.dumps({"stats": {}}), encoding="utf-8")
    evidence, warnings = load_security_evidence(path)
    assert evidence.available is False
    assert warnings


def test_loads_classification(tmp_path):
    path = tmp_path / "security-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    evidence, warnings = load_security_evidence(path)

    assert warnings == []
    assert evidence.available is True
    assert evidence.sensitivity == "high"
    assert evidence.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"
    assert evidence.source_path == str(path)
