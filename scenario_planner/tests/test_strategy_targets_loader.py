import json

import pytest

from scenario_planner.strategy_targets_loader import (
    StrategyReportError,
    load_strategy_report,
)

_VALID = {
    "repo_root": "/tmp/target",
    "targets": [
        {
            "file": "pkg/module.py",
            "priority": "high",
            "reason": "reason text",
            "risk_tier": "high",
            "generation_feasible": True,
            "feasibility_note": "note",
            "recommended_framework": "pytest",
        }
    ],
}


def test_loads_target_summaries(tmp_path):
    path = tmp_path / "strategy.json"
    path.write_text(json.dumps(_VALID), encoding="utf-8")

    ctx = load_strategy_report(path)

    assert ctx.repo_root == "/tmp/target"
    assert len(ctx.targets) == 1
    target = ctx.targets[0]
    assert target.file == "pkg/module.py"
    assert target.priority == "high"
    assert target.generation_feasible is True
    assert target.recommended_framework == "pytest"


def test_missing_file_raises_strategy_report_error(tmp_path):
    with pytest.raises(StrategyReportError):
        load_strategy_report(tmp_path / "missing.json")


def test_missing_required_key_raises_strategy_report_error(tmp_path):
    path = tmp_path / "strategy.json"
    path.write_text(json.dumps({"repo_root": "/tmp/target"}), encoding="utf-8")

    with pytest.raises(StrategyReportError):
        load_strategy_report(path)


def test_target_missing_required_field_raises_strategy_report_error(tmp_path):
    path = tmp_path / "strategy.json"
    bad = {"repo_root": "/tmp/target", "targets": [{"file": "pkg/module.py"}]}
    path.write_text(json.dumps(bad), encoding="utf-8")

    with pytest.raises(StrategyReportError):
        load_strategy_report(path)
