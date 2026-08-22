"""Fixed table of path/filename conventions that are sensitive by
convention. Leads, not verdicts — a matching name doesn't guarantee real
secret content, and a non-matching name doesn't guarantee safety.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass


@dataclass(frozen=True)
class SensitivePathPattern:
    pattern_id: str
    glob: str
    description: str


PATTERNS: list[SensitivePathPattern] = [
    SensitivePathPattern("dotenv-file", "*.env", "Environment file — often holds secrets."),
    SensitivePathPattern("pem-key", "*.pem", "PEM key/certificate file."),
    SensitivePathPattern("ssh-private-key", "id_rsa*", "SSH private key file."),
    SensitivePathPattern("credentials-json", "credentials.json", "Conventional credentials filename."),
    SensitivePathPattern("aws-credentials", "credentials", "AWS-style credentials file (check path context)."),
    SensitivePathPattern("secrets-file", "secrets.*", "Conventional secrets filename."),
]


def match_sensitive_paths(paths: list[str]) -> list[tuple[str, SensitivePathPattern]]:
    matches: list[tuple[str, SensitivePathPattern]] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        basename = normalized.rsplit("/", 1)[-1]
        parent = normalized.rsplit("/", 2)[-2] if "/" in normalized else ""
        for pattern in PATTERNS:
            if pattern.pattern_id == "aws-credentials":
                if basename == "credentials" and parent == ".aws":
                    matches.append((path, pattern))
                continue
            if fnmatch.fnmatch(basename, pattern.glob):
                matches.append((path, pattern))
    return matches
