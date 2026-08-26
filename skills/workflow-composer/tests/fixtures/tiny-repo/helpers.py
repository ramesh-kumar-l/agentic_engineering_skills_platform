"""A tiny fixture module used only by workflow-composer's real-execution test."""

from main import add


def double_sum(a: int, b: int) -> int:
    return add(a, b) * 2
