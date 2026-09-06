import json

import pytest

from scenario_planner.regression_flags_loader import (
    RegressionFlagsError,
    load_regression_flags,
)

_VALID = {
    "files": [
        {
            "file": "pkg/module.py",
            "diff_pattern_flags": [
                {
                    "pattern_id": "modified-signature-no-test-change",
                    "category": "diff-pattern",
                    "severity": "medium",
                    "file": "pkg/module.py",
                    "line": 10,
                    "description": "signature changed, no test change",
                    "matched_text": "",
                }
            ],
        },
        {"file": "pkg/other.py", "diff_pattern_flags": []},
    ]
}


def test_loads_flags_grouped_by_file(tmp_path):
    path = tmp_path / "reg.json"
    path.write_text(json.dumps(_VALID), encoding="utf-8")

    flags_by_file = load_regression_flags(path)

    assert len(flags_by_file["pkg/module.py"]) == 1
    flag = flags_by_file["pkg/module.py"][0]
    assert flag.pattern_id == "modified-signature-no-test-change"
    assert flag.severity == "medium"
    assert "signature changed" in flag.description
    assert flags_by_file["pkg/other.py"] == []


def test_missing_file_raises_regression_flags_error(tmp_path):
    with pytest.raises(RegressionFlagsError):
        load_regression_flags(tmp_path / "missing.json")


def test_missing_files_key_raises_regression_flags_error(tmp_path):
    path = tmp_path / "reg.json"
    path.write_text(json.dumps({}), encoding="utf-8")

    with pytest.raises(RegressionFlagsError):
        load_regression_flags(path)


def test_flag_missing_required_field_raises_regression_flags_error(tmp_path):
    path = tmp_path / "reg.json"
    bad = {"files": [{"file": "pkg/module.py", "diff_pattern_flags": [{"pattern_id": "x"}]}]}
    path.write_text(json.dumps(bad), encoding="utf-8")

    with pytest.raises(RegressionFlagsError):
        load_regression_flags(path)
