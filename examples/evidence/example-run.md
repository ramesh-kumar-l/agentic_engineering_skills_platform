# Evidence Foundation — real dogfood run

This is a genuine, non-fixture demonstration of TEP Phase 2's exit
criteria ([[18-test-engineering-platform-contract]]): the run-provenance
schema, defined in [[19-evidence-provenance-schema]] and implemented in
`evidence/`, applied to one real run of an *existing* skill
(`codebase-intelligence`) against this repository's own current state —
not a synthetic fixture.

## Command

```
python -m evidence.cli codebase-intelligence .
```

Run from the repository root. This invokes `codebase-intelligence`'s own
documented CLI as a subprocess (exactly as a human or agent would), times
it, resolves the analyzed repo's real git commit by reading `.git/HEAD`
directly, hashes the produced `report.json`, and writes both the report
and this provenance record to disk.

## Result

`provenance-record.json` (in this directory) is the actual record produced
by that run, copied here as committed evidence — the operational copy
under `evidence/runs/` is gitignored (regenerates every run, would be pure
diff noise on every commit, same reasoning as
`evaluations/workflow-composer/_run/`).

Verified by hand against this run:
- `repo_commit` matches `git rev-parse HEAD` at the time of the run exactly.
- `skill_version` (`0.2.0`) matches `skills/codebase-intelligence/pyproject.toml`.
- `status: "success"`, `exit_code: 0` — the subprocess actually ran and
  actually produced output; this is not asserted, it's the real
  `returncode`.
- `output_sha256` is a real SHA-256 of the actual `report.json` bytes
  produced by that run (not committed here — it's identical in content to
  `examples/codebase-intelligence/report.json`'s purpose, and committing a
  second full copy would just duplicate it; the hash is what makes this
  record independently checkable without re-committing the report).
- `model` and `prompt_version` are `null`, honestly — `codebase-intelligence`
  is a deterministic engine with no model call inside it. These fields
  stay reserved for a future AI-driven generation phase, not backfilled.

## What this does and does not prove

Proves: this platform can now produce a verifiable, timestamped record of
*which* skill, *which* version, *which* target commit, and *whether it
actually succeeded* — for a real run, not a description of one.

Does not prove: nothing about whether any skill's output is *useful* —
that claim requires Trust Ladder Level 4+ evidence (mutation testing),
which does not exist yet and is explicitly out of scope for this phase
(see the contract's non-goals).
