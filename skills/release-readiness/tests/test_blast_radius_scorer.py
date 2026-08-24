from engine.blast_radius_scorer import structural_tier
from engine.models import StructuralAssessment


def _structural(**overrides) -> StructuralAssessment:
    base = dict(resolved_module_path="engine/foo.py", fan_in=0, fan_out=0, is_hotspot=False)
    base.update(overrides)
    return StructuralAssessment(**base)


def test_unresolved_is_low():
    assert structural_tier(StructuralAssessment()) == "low"


def test_hotspot_is_high():
    assert structural_tier(_structural(is_hotspot=True)) == "high"


def test_high_fan_in_is_high():
    assert structural_tier(_structural(fan_in=5)) == "high"


def test_some_fan_in_is_medium():
    assert structural_tier(_structural(fan_in=1)) == "medium"


def test_zero_fan_in_is_low():
    assert structural_tier(_structural(fan_in=0)) == "low"
