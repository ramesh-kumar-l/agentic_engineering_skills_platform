# Example run — dogfooding against a real, already-shipped CLI

This is a real (non-synthetic) dogfood run: the requirement text below
describes the actual `--format`/`--out`/stdin behavior already implemented in
`skills/adversarial-diff-reviewer/engine/cli.py` (Phase 2), read directly from
that source file, not invented.

## Step 1 — Requirement text fed to the engine

```
The adversarial-diff-reviewer CLI accepts a path to a diff file or a dash for stdin.
It accepts a format flag with choices json, markdown, or both, defaulting to both.
It accepts an optional out directory.
If the path does not exist and is not a dash, the CLI exits with a non-zero status and an error message.
If out is provided, output files are written to that directory.
If out is not provided, output is printed to stdout.
```

## Step 1 output — deterministic engine

`python -m engine.cli requirement.txt` produced 6 parsed sentences, 0 vague
terms, 0 weak modals, and exactly one testability flag:
`no-boundary-signal` (whole document — expected and acceptable here: this
requirement genuinely has no numeric boundary concept, a known shape of
over-flagging documented in `project-memory-bank/12-known-limitations.md`).

## Step 3 — Acceptance cases derived against the coverage checklist

- **happy-path**: valid diff file path, `--format both`, no `--out` → both
  reports printed to stdout.
- **boundary/edge-value**: N/A — no numeric bound in this requirement (stated
  explicitly rather than silently skipped).
- **invalid-input-error-handling**: nonexistent path (not `-`) → CLI exits
  non-zero with a stderr message containing "does not exist".
- **empty/missing/null state**: `--out` omitted → output goes to stdout, not
  a file.
- **duplicate/repeat**: N/A — CLI is stateless per invocation.
- **concurrent access**: N/A — no shared state between invocations.
- **authorization boundary**: N/A — no auth concept in this CLI.
- **non-functional constraint**: none stated.
- **assumption-flag**: none needed — the requirement text is fully
  specific here (it's a literal restatement of real, already-implemented
  code, not a genuine unresolved product requirement).
- **additional case surfaced during derivation**: stdin (`-`) as the path
  argument must read the diff from stdin, not attempt to open a file
  literally named `-`.

## Step 4 outcome — real gap found and fixed

Cross-checking these derived acceptance cases against
`skills/adversarial-diff-reviewer/tests/` (5 files, 19 tests as of Phase 2)
found **zero** test coverage of `cli.py` itself — no test invoked `main()`,
checked an exit code, read from stdin, or verified `--out` file writing. The
diff-parsing/risk-scanning engine was thoroughly tested; its CLI wrapper was
not.

This is a real, actionable finding, not a synthetic one — the same
"dogfooding surfaces something real" pattern as Phase 1's `has_main_guard`
false positive and Phase 2's L5/L6 redaction bugs. Fixed immediately:
`skills/adversarial-diff-reviewer/tests/test_cli.py` added (4 tests) directly
from the derived acceptance cases — nonexistent-path exit code, stdin
reading, `--out` writing both files, `--format json` writing only the JSON
file. Full suite: 23/23 passing (was 19/19).

## Honesty note

This dogfood run is still self-authored: the same agent wrote the
requirement text, derived the acceptance cases, and wrote the resulting
tests. The value here is that the requirement text and the resulting test
gap are both objectively checkable against real source code — unlike the
8 synthetic evaluation fixtures, this one isn't graded against
self-authored ground truth, it's graded against "did real test files exist
before this run." They didn't; now they do.
