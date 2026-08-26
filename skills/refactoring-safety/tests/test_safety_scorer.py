from engine.models import CallerModule, TargetAssessment
from engine.safety_scorer import score_target, score_targets


def _target(**overrides) -> TargetAssessment:
    base = dict(
        target_name="foo",
        resolved_module_path="engine/foo.py",
        fan_in=0,
        fan_out=0,
        is_hotspot=False,
        caller_modules=[],
        test_coverage_modules=[],
    )
    base.update(overrides)
    return TargetAssessment(**base)


def test_boundary_op_with_high_fan_in_is_high_risk():
    tier, flag = score_target("rename", _target(fan_in=8))
    assert tier == "high"
    assert flag is not None
    assert flag.category == "untested-blast-radius"


def test_boundary_op_with_hotspot_is_high_risk_even_with_low_fan_in():
    tier, _ = score_target("delete", _target(fan_in=0, is_hotspot=True))
    assert tier == "high"


def test_boundary_op_with_some_fan_in_is_medium_risk():
    tier, flag = score_target("move", _target(fan_in=1))
    assert tier == "medium"
    assert flag is not None


def test_boundary_op_with_zero_fan_in_is_low_risk():
    tier, flag = score_target("rename", _target(fan_in=0))
    assert tier == "low"
    assert flag is None


def test_internal_op_ignores_fan_in_unless_hotspot():
    tier, flag = score_target("extract", _target(fan_in=20, is_hotspot=False))
    assert tier == "low"
    assert flag is None


def test_internal_op_on_hotspot_with_fan_in_is_medium():
    tier, flag = score_target("inline", _target(fan_in=2, is_hotspot=True))
    assert tier == "medium"
    assert flag is not None


def test_covered_target_produces_no_untested_flag():
    tier, flag = score_target("rename", _target(fan_in=8, test_coverage_modules=["tests/test_foo.py"]))
    assert tier == "high"
    assert flag is None


def test_generic_refactor_scored_conservatively():
    tier, _ = score_target("refactor", _target(fan_in=6))
    assert tier == "high"


def test_score_targets_skips_unresolved_targets():
    unresolved = _target(resolved_module_path=None)
    flags = score_targets("rename", [unresolved])
    assert flags == []
    assert unresolved.risk_tier == "low"


def test_score_targets_collects_flags_across_targets():
    high_risk = _target(target_name="a", fan_in=10)
    low_risk = _target(target_name="b", resolved_module_path="engine/b.py", fan_in=0)
    flags = score_targets("delete", [high_risk, low_risk])
    assert len(flags) == 1
    assert "a" in flags[0].matched_text
