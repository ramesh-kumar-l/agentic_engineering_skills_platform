"""Fixed keyword table for the six high-risk action categories named
verbatim in project-memory-bank/06-security-model.md.

Leads, not verdicts — matching a keyword doesn't guarantee the described
action is actually high-risk in context, and the absence of a match doesn't
guarantee it's safe. The agent's Step 3 judgment (SKILL.md) makes the real
authorization recommendation; this table only surfaces candidates.

Categories with a verb+object shape (e.g. "push ... origin") are matched by
same-sentence co-occurrence, not a fixed character-distance window. A real
dogfood run (examples/security-context-guard/example-run.md) found that
realistic phrasing often puts a parenthetical object list between the verb
and its target ("push the new X, Y, Z files ... to the shared origin
repository", 150+ characters apart) — a fixed window (even a generous one)
missed it entirely, while same-sentence matching catches it without needing
to guess a magic distance. See project-memory-bank/12-known-limitations.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


@dataclass(frozen=True)
class ActionPattern:
    pattern_id: str
    category: str
    description: str
    regex: re.Pattern[str] | None = None
    verb_regex: re.Pattern[str] | None = None
    object_regex: re.Pattern[str] | None = None

    def matches(self, text: str) -> re.Match[str] | None:
        if self.regex is not None:
            return self.regex.search(text)
        for sentence in _SENTENCE_SPLIT.split(text):
            verb_match = self.verb_regex.search(sentence)
            object_match = self.object_regex.search(sentence)
            if verb_match and object_match:
                return verb_match
        return None


PATTERNS: list[ActionPattern] = [
    ActionPattern(
        "production-modification", "Production modifications",
        "Mentions modifying/deploying to production.",
        verb_regex=re.compile(r"(?i)\b(deploy|release|modify|update|change)\b"),
        object_regex=re.compile(r"(?i)\bprod(?:uction)?\b"),
    ),
    ActionPattern(
        "destructive-operation", "Destructive operations",
        "Mentions a destructive operation.",
        regex=re.compile(r"(?i)\b(delete|drop|rm -rf|force[- ]?push|truncate|wipe|destroy)\b"),
    ),
    ActionPattern(
        "credential-handling", "Credentials",
        "Mentions handling credentials.",
        verb_regex=re.compile(r"(?i)\b(rotate|generate|reset|reveal|expose)\b"),
        object_regex=re.compile(r"(?i)\b(credential|password|secret|token|api[_ -]?key)\b"),
    ),
    ActionPattern(
        "security-control-change", "Security controls",
        "Mentions changing a security control.",
        verb_regex=re.compile(r"(?i)\b(disable|bypass|weaken|turn off)\b"),
        object_regex=re.compile(r"(?i)\b(auth(?:entication|orization)?|firewall|permission|access control|security)\b"),
    ),
    ActionPattern(
        "database-migration", "Database migrations",
        "Mentions a database migration/schema change.",
        regex=re.compile(r"(?i)\b(migrat(?:e|ion)|alter table|drop table|schema change)\b"),
    ),
    ActionPattern(
        "publishing", "Publishing",
        "Mentions publishing/pushing to a shared destination.",
        regex=re.compile(r"(?i)\bpublish\b|\brelease to\b|\bship to\b"),
    ),
    ActionPattern(
        "publishing-push", "Publishing",
        "Mentions pushing to a shared remote destination.",
        verb_regex=re.compile(r"(?i)\bpush\b"),
        object_regex=re.compile(r"(?i)\b(origin|main|shared|remote|repository|repo)\b"),
    ),
    ActionPattern(
        "external-communication", "External communications",
        "Mentions sending data to an external destination.",
        regex=re.compile(r"(?i)\bwebhook\b"),
    ),
    ActionPattern(
        "external-communication-send", "External communications",
        "Mentions sending data to an external destination.",
        verb_regex=re.compile(r"(?i)\b(send|post|email|notify)\b"),
        object_regex=re.compile(r"(?i)\b(external|customer|third[- ]?party|outside)\b"),
    ),
]
