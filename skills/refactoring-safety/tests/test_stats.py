from engine.models import SafetyFlag, TargetAssessment
from engine.stats import compute_stats


def test_computes_word_and_target_counts():
    targets = [
        TargetAssessment(target_name="a", resolved_module_path="engine/a.py"),
        TargetAssessment(target_name="b", resolved_module_path=None),
    ]
    flags = [
        SafetyFlag("p1", "cat", "high", "desc", ""),
        SafetyFlag("p2", "cat", "low", "desc", ""),
    ]
    stats = compute_stats("Rename a to b please", targets, flags)

    assert stats.word_count == 5
    assert stats.target_count == 2
    assert stats.resolved_target_count == 1
    assert stats.flag_count == 2
    assert stats.high_severity_flag_count == 1
