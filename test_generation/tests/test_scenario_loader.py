import json

import pytest

from test_generation.scenario_loader import ScenarioPlanError, load_scenario_plan

_SCENARIO_REPORT = {
    "repo_root": "/tmp/target",
    "plans": [
        {
            "file": "pkg/module.py",
            "recommended_framework": "pytest",
            "scenarios": [
                {
                    "scenario_name": "exercise function `foo`",
                    "symbol_kind": "function",
                    "rationale": "rationale text",
                    "source": "structural-listing",
                    "target_symbol": "foo",
                }
            ],
        }
    ],
}


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_loads_candidates_with_parent_file_and_framework(tmp_path):
    path = _write(tmp_path / "scenario.json", _SCENARIO_REPORT)

    ctx = load_scenario_plan(path)

    assert ctx.repo_root == "/tmp/target"
    assert len(ctx.candidates) == 1
    candidate = ctx.candidates[0]
    assert candidate.file == "pkg/module.py"
    assert candidate.recommended_framework == "pytest"
    assert candidate.target_symbol == "foo"
    assert candidate.source == "structural-listing"


def test_missing_file_raises_error(tmp_path):
    with pytest.raises(ScenarioPlanError):
        load_scenario_plan(tmp_path / "missing.json")


def test_missing_plans_key_raises_error(tmp_path):
    path = _write(tmp_path / "scenario.json", {"repo_root": "/tmp/target"})

    with pytest.raises(ScenarioPlanError):
        load_scenario_plan(path)


def test_scenario_entry_missing_field_raises_error(tmp_path):
    bad_report = {
        "repo_root": "/tmp/target",
        "plans": [
            {
                "file": "pkg/module.py",
                "recommended_framework": "pytest",
                "scenarios": [{"scenario_name": "x"}],
            }
        ],
    }
    path = _write(tmp_path / "scenario.json", bad_report)

    with pytest.raises(ScenarioPlanError):
        load_scenario_plan(path)
