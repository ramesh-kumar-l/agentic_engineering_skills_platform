"""A tiny fixture module used only by workflow-composer's real-execution test."""


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(add(1, 2))
