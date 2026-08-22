"""Fixed table of mechanically-detectable risk patterns for added diff lines.

These are *leads*, not verdicts — a regex hit does not mean a defect exists,
and the absence of a hit does not mean the line is safe. The agent's
adversarial reasoning (SKILL.md Step 3) is what actually judges the diff; see
[[12-known-limitations]] for this layer's documented false-positive/negative
rate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str
    redact: bool = False


PATTERNS: list[RiskPattern] = [
    RiskPattern(
        pattern_id="hardcoded-secret",
        category="security-issue",
        severity="high",
        regex=re.compile(
            r"(?i)\b(api[_-]?key|secret|password|passwd|token|"
            r"access[_-]?key)\b\s*[:=]\s*[\"'][^\"']{6,}[\"']"
        ),
        description="Line looks like a hardcoded secret/credential literal.",
        redact=True,
    ),
    RiskPattern(
        pattern_id="dangerous-eval-exec",
        category="security-issue",
        severity="high",
        regex=re.compile(r"\b(eval|exec)\s*\("),
        description="Use of eval()/exec() on added line — arbitrary code execution risk.",
    ),
    RiskPattern(
        pattern_id="dangerous-pickle-loads",
        category="security-issue",
        severity="high",
        regex=re.compile(r"\bpickle\.loads\s*\("),
        description="pickle.loads() on added line — unsafe deserialization risk.",
    ),
    RiskPattern(
        pattern_id="dangerous-shell-true",
        category="security-issue",
        severity="high",
        regex=re.compile(r"subprocess\.\w+\([^)]*shell\s*=\s*True"),
        description="subprocess call with shell=True — shell injection risk.",
    ),
    RiskPattern(
        pattern_id="dangerous-os-system",
        category="security-issue",
        severity="medium",
        regex=re.compile(r"\bos\.system\s*\("),
        description="os.system() on added line — shell injection / portability risk.",
    ),
    RiskPattern(
        pattern_id="sql-string-concat",
        category="security-issue",
        severity="high",
        regex=re.compile(r"\.execute\s*\(\s*[\"'][^\"']*[\"']\s*\+"),
        description="SQL query built via string concatenation before execute() — injection risk.",
    ),
    RiskPattern(
        pattern_id="sql-fstring",
        category="security-issue",
        severity="high",
        regex=re.compile(
            r"(?i)f[\"'][^\"']*\b(select|insert|update|delete)\b[^\"']*\{"
        ),
        description="SQL keyword inside an f-string with interpolation — injection risk.",
    ),
    RiskPattern(
        pattern_id="broad-except-bare",
        category="obvious-bug",
        severity="medium",
        regex=re.compile(r"^\s*except\s*:\s*$"),
        description="Bare except: swallows all exceptions, including KeyboardInterrupt/SystemExit.",
    ),
    RiskPattern(
        pattern_id="broad-except-exception",
        category="subtle-bug",
        severity="low",
        regex=re.compile(r"^\s*except\s+Exception\s*:\s*$"),
        description="Broad except Exception: may hide unrelated errors.",
    ),
    RiskPattern(
        pattern_id="debug-leftover",
        category="correct-but-unusual",
        severity="low",
        regex=re.compile(
            r"\bconsole\.log\s*\(|\bpdb\.set_trace\s*\(|"
            r"\bdebugger\s*;|\bbreakpoint\s*\("
        ),
        description="Debug statement left in added code.",
    ),
    RiskPattern(
        pattern_id="todo-marker",
        category="incorrect-requirement",
        severity="low",
        regex=re.compile(r"(?:#|//)\s*(TODO|FIXME|XXX)\b"),
        description="TODO/FIXME/XXX left in new code — possibly incomplete requirement.",
    ),
]
