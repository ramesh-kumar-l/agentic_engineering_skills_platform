# 19 — Evidence Foundation: run-provenance schema

This file documents the schema implemented in `evidence/schema.py` for TEP
Phase 2 ([[18-test-engineering-platform-contract]]), and the rationale for
each field. See [[11-decisions|ADR-024]] for the architectural decision and
`examples/evidence/example-run.md` for a real, non-fixture demonstration.

## What this is and is not

A `RunProvenance` record answers: *which skill, at which version, analyzed
which repo commit, did it actually succeed, and when.* It is metadata about
a run's execution, not a claim about the run's usefulness. Nothing in this
schema, or in [[16-assumptions-and-validation]], licenses a claim like
"this generated a useful test" — that requires Trust Ladder Level 4+
evidence (mutation testing), which does not exist yet.

## Fields

| Field | Why it exists |
|---|---|
| `schema_version` | Lets a future reader (or a future schema migration) know which shape they're looking at — the master prompt's own evidence architecture assumes schemas evolve. |
| `run_id` | Unique key for the record; also the filename under `evidence/runs/<skill>/`. |
| `skill_name`, `skill_version` | The two fields the contract names explicitly — which skill, which version, read from that skill's own `pyproject.toml` (never guessed). |
| `repo_root`, `repo_commit` | The contract's "repo/commit" — which target repository, at which commit, was actually analyzed. `repo_commit` is best-effort: `None` with a disclosed warning if `.git/HEAD` can't be resolved (see [[12-known-limitations]] precedent: disclose, don't hide). |
| `started_at`, `finished_at`, `duration_ms` | The contract's "timestamp" — start/end rather than one instant, so duration is derived, not estimated. |
| `exit_code`, `status` | Without these, a provenance record would be an unfalsifiable claim that a run happened — this is what makes it *evidence* rather than metadata, matching this project's existing actual-vs-expected evaluation discipline ([[05-evaluation-framework]]). |
| `output_sha256`, `output_relpath` | Tamper-evidence: proves which exact output bytes this record refers to, without requiring every provenance record to carry a full copy of a (potentially large) report. |
| `model`, `prompt_version` | Named explicitly in the contract for a future AI-driven generation phase (TEP Phase 5+). Always `None` today — every skill's engine is deterministic (ADR-005/006), there is no model call to record. Kept as reserved fields rather than omitted, so a future phase extends this schema instead of replacing it. |
| `warnings` | Anything that didn't resolve cleanly (unresolvable commit, missing output, subprocess stderr) — disclosed inline rather than silently dropped. |

## Deliberately excluded (considered, rejected)

- **`repo_dirty`** (uncommitted local changes): would require re-implementing
  real `git status` logic (index + working-tree diff) in pure stdlib to stay
  consistent with `git_info.py`'s no-subprocess approach — a disproportionate
  amount of new logic for one boolean this phase's exit criteria doesn't
  require. Not added speculatively (ADR-006/009 precedent).
- **`platform_commit`** (which commit of *this* platform repo, as opposed to
  the analyzed target repo, produced the record): the contract's own field
  list names one commit, and `skill_version` already identifies which
  version of the skill ran — a second commit field would duplicate that
  without new information today.
- **`environment`** (Python/OS version): no consumer needs it yet; add only
  when a real cross-environment reproducibility question shows up.

## Storage layout

`evidence/runs/<skill_name>/<run_id>.json` — mirrors the existing
`evaluations/<skill>/` per-skill layout convention. Gitignored (regenerates
every run; would be pure diff noise), matching the precedent set by
`evaluations/workflow-composer/_run/`. A curated, committed example lives
at `examples/evidence/example-run.md` instead — the same pattern
`examples/feature-planner/example-run.md` already established for a real
dogfood run.

## Status

Implemented and demonstrated (2026-09-06) via `evidence/` — see ADR-024.
Not yet consumed by any other skill; that consumption (if any) is future
scope, not part of TEP Phase 2's exit criteria.
