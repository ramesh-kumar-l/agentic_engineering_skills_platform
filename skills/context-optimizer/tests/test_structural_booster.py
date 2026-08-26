from engine.models import CiDependencyGraph
from engine.structural_booster import (
    HIGH_FAN_IN_BOOST,
    HIGH_FAN_IN_THRESHOLD,
    HOTSPOT_BOOST,
    apply_structural_boost,
)


def test_hotspot_gets_hotspot_boost():
    graph = CiDependencyGraph(hotspots=["engine/scanner.py"])
    assert apply_structural_boost(3, "engine/scanner.py", graph) == 3 + HOTSPOT_BOOST


def test_high_fan_in_non_hotspot_gets_fan_in_boost():
    graph = CiDependencyGraph(fan_in={"engine/scanner.py": HIGH_FAN_IN_THRESHOLD})
    assert apply_structural_boost(3, "engine/scanner.py", graph) == 3 + HIGH_FAN_IN_BOOST


def test_below_threshold_fan_in_gets_no_boost():
    graph = CiDependencyGraph(fan_in={"engine/scanner.py": HIGH_FAN_IN_THRESHOLD - 1})
    assert apply_structural_boost(3, "engine/scanner.py", graph) == 3


def test_unrecognized_path_gets_no_boost():
    graph = CiDependencyGraph()
    assert apply_structural_boost(3, "engine/scanner.py", graph) == 3


def test_hotspot_boost_wins_over_fan_in_boost_when_both_apply():
    graph = CiDependencyGraph(
        hotspots=["engine/scanner.py"], fan_in={"engine/scanner.py": 99}
    )
    assert apply_structural_boost(3, "engine/scanner.py", graph) == 3 + HOTSPOT_BOOST
