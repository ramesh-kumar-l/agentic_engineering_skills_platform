"""The run-provenance schema for TEP Phase 2 (Evidence Foundation).

One `RunProvenance` record answers, for a single invocation of one existing
skill's CLI: which repo (and commit) was analyzed, which version of the
skill produced the output, whether it actually succeeded, and when. This is
metadata *about* a run, not a claim about the run's usefulness — see
[[19-evidence-provenance-schema]] for the field-by-field rationale and the
explicit boundary against "verified useful" claims (Trust Ladder Level 4+).

`model` and `prompt_version` are always None today: every skill's engine is
a deterministic, stdlib-only pipeline (ADR-005/006) with no model call
inside it. The fields exist because the master prompt's evidence
architecture names them, and a future AI-driven generation phase (TEP Phase
5+) will need them — they are not backfilled with a guess.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class RunProvenance:
    schema_version: str
    run_id: str
    skill_name: str
    skill_version: str | None
    repo_root: str
    repo_commit: str | None
    started_at: str  # ISO 8601 UTC
    finished_at: str  # ISO 8601 UTC
    duration_ms: int
    exit_code: int
    status: str  # "success" | "failure"
    output_sha256: str | None
    output_relpath: str | None
    model: str | None = None
    prompt_version: str | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "RunProvenance":
        known = {f for f in RunProvenance.__dataclass_fields__}
        return RunProvenance(**{k: v for k, v in data.items() if k in known})
