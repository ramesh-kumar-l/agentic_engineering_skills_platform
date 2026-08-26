from engine.models import ResolvedLocation
from engine.priority_scorer import HIGH_FAN_IN_THRESHOLD, compute_priority


def test_unresolved_fails_closed_to_medium_not_low():
    assert compute_priority(None, ci_has_warning=False) == "MEDIUM"


def test_ci_warning_fails_closed_to_medium_even_if_resolved():
    resolved = ResolvedLocation(module_path="engine/scanner.py", fan_in=0, is_hotspot=False)
    assert compute_priority(resolved, ci_has_warning=True) == "MEDIUM"


def test_resolved_hotspot_scores_high():
    resolved = ResolvedLocation(module_path="engine/scanner.py", fan_in=0, is_hotspot=True)
    assert compute_priority(resolved, ci_has_warning=False) == "HIGH"


def test_resolved_high_fan_in_scores_high():
    resolved = ResolvedLocation(
        module_path="engine/scanner.py", fan_in=HIGH_FAN_IN_THRESHOLD, is_hotspot=False
    )
    assert compute_priority(resolved, ci_has_warning=False) == "HIGH"


def test_resolved_low_fan_in_non_hotspot_scores_medium_not_low():
    resolved = ResolvedLocation(
        module_path="engine/stats.py", fan_in=HIGH_FAN_IN_THRESHOLD - 1, is_hotspot=False
    )
    assert compute_priority(resolved, ci_has_warning=False) == "MEDIUM"


def test_resolved_zero_fan_in_non_hotspot_scores_medium_not_low():
    """LOW is a defined band (models.py) this scorer deliberately never
    assigns — this is the exact case that could be LOW and isn't, by
    design. See priority_scorer.py's module docstring."""
    resolved = ResolvedLocation(module_path="engine/stats.py", fan_in=0, is_hotspot=False)
    assert compute_priority(resolved, ci_has_warning=False) == "MEDIUM"
