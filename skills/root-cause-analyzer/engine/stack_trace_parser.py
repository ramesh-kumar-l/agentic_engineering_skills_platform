"""Extracts stack-trace/traceback-shaped frames from free-text symptom
input.

This is the strongest deterministic signal this skill has: a file path a
human or a language runtime actually wrote down at the moment of failure is
real evidence, not an inference. It is still not proof of the *root* cause
(the top frame is often a symptom site, not the defect site — see
project-memory-bank/12-known-limitations.md) — the candidate scorer marks
these as a distinct, higher-confidence evidence tier, and the agent's Step 3
investigation is what actually decides whether a stack-trace hit is the real
root cause or just where the failure surfaced.

Two fixed shapes covered, same "small, defensible table" discipline as
every other pattern module in this project:
  1. Python traceback frames: `File "path/to/file.py", line 123, in func`
  2. Generic `path/to/file.ext:123` references (compiler errors, log lines,
     other language tracebacks that follow this common shape).
"""

from __future__ import annotations

import re

from .models import StackFrame

_PYTHON_FRAME = re.compile(
    r'File "(?P<path>[^"]+)", line (?P<line>\d+)(?:, in (?P<symbol>\S+))?'
)
_GENERIC_FRAME = re.compile(
    r"(?P<path>[\w][\w./\\-]*\.[a-zA-Z]{1,10}):(?P<line>\d+)"
)


def parse_stack_frames(symptom_text: str) -> list[StackFrame]:
    frames: list[StackFrame] = []
    seen_spans: list[tuple[int, int]] = []

    for match in _PYTHON_FRAME.finditer(symptom_text):
        frames.append(
            StackFrame(
                path=match.group("path"),
                line=int(match.group("line")),
                symbol=match.group("symbol"),
                raw_text=match.group(0),
            )
        )
        seen_spans.append(match.span())

    def _overlaps(span: tuple[int, int]) -> bool:
        return any(span[0] < end and start < span[1] for start, end in seen_spans)

    for match in _GENERIC_FRAME.finditer(symptom_text):
        if _overlaps(match.span()):
            continue
        frames.append(
            StackFrame(
                path=match.group("path"),
                line=int(match.group("line")),
                symbol=None,
                raw_text=match.group(0),
            )
        )

    return frames
