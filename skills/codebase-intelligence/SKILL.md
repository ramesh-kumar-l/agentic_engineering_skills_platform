# Codebase Intelligence

## Metadata
- Version: 0.1.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/codebase-intelligence/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access and Python 3.10+ available

## Purpose
Produce a condensed, structural map of an unfamiliar repository — file inventory,
module structure, internal dependency graph, entry points, external dependencies,
and documentation coverage — so an agent can orient itself without reading the
whole repository.

## Problem
Agents commonly default to dumping large portions of a repository into context,
or re-derive structure ad hoc via repeated Grep/Read calls on every task. Both
are expensive, slow, and produce inconsistent understanding across runs. This
skill produces a single, deterministic, repeatable "engineered context object"
instead (see `project-memory-bank/02-requirements.md`, NFR2).

## When to Use
- Before planning a feature or reviewing a diff in a repository the agent has
  not already analyzed in this session.
- When an agent needs to know which files are most central (highest blast
  radius) before making a change.
- As a prerequisite step for other skills in this platform (diff review,
  feature planning, security review) that need repo structure as input.

## When NOT to Use
- On a repository already fully understood in the current session (re-running
  wastes tokens for no new information).
- As a substitute for reading the actual code being changed — this skill gives
  structure, not semantics or correctness.
- On repositories containing code the agent is not authorized to access.

## Preconditions
- A local, readable path to the target repository.
- Python 3.10+ available in the execution environment.

## Inputs
- `path` (required): path to the repository or subdirectory to analyze.
- `--format` (optional): `json`, `markdown`, or `both` (default).
- `--out` (optional): directory to write report files to (default: stdout).

## Required Context
None beyond the target path. This skill does not require the agent's existing
conversation context — it is meant to reduce reliance on that.

## Context Completeness
The report is structural, not semantic: it captures imports/defs/classes and
file-level relationships, not runtime behavior, business logic correctness, or
cross-language type resolution. Treat it as a map, not full understanding.

## Security Constraints
- Read-only: the engine never writes to, modifies, or deletes files in the
  target repository.
- Never reads or emits the contents of secret-shaped files (`.env`, `*.pem`,
  `*.key`, `credentials.json`, `secrets.yaml`, SSH private keys) — these are
  recorded only as a filename-only warning. See `engine/scanner.py`.
- Only structural metadata (imports, def/class names, docstrings, file sizes)
  is extracted — full file contents are never included in the report.
- No network access; no external calls.

## Workflow
### Step 1 — Invoke the engine
Run via Bash: `python -m engine.cli <path> --format both --out <output-dir>`
(from `skills/codebase-intelligence/`).

### Step 2 — Read the Markdown report first
`report.md` is the condensed, minimum-sufficient-context view — read this
before the JSON unless full detail (e.g. every file/edge) is specifically needed.

### Step 3 — Consult report.json only for specifics
Use the JSON output when a downstream task needs the full file list, full
dependency edge list, or per-module docstrings/defs not summarized in the
Markdown.

### Step 4 — Treat warnings as signal
The `warnings` section lists skipped secret-shaped files and oversized files —
review it before assuming the report is complete.

## Agent Responsibilities
- Do not paste raw file contents from the target repo into the report or
  onward into unrelated context.
- Distinguish what the report OBSERVED (structural facts) from anything the
  agent subsequently INFERS about the codebase's purpose or quality.
- Re-run the skill if the repository has changed since the last report.

## Tool Permissions
- Bash (to invoke `python -m engine.cli`) — read-only usage only.
- Read (to consume the generated `report.md` / `report.json`).
No write, network, or credential-accessing permissions are required or granted.

## Human Checkpoints
None required for normal use — this is a read-only, non-destructive analysis
step. (Per `project-memory-bank/06-security-model.md`, human approval is
reserved for high-risk actions; running a local read-only scan is not one.)

## Outputs
- `report.json` — full-detail machine-readable report (see `engine/models.py`
  for the exact schema: `CodebaseIntelligenceReport`).
- `report.md` — condensed human/agent-readable summary.

## Verification
- `pytest` (22 unit/integration tests as of v0.1.0) — see `tests/`.
- `evaluations/codebase-intelligence/run_evaluation.py` against 4 fixture repos —
  see `evaluations/codebase-intelligence/RESULTS.md` for actual scores.

## Evaluation
See `evaluations/codebase-intelligence/` for the full case set and
`project-memory-bank/05-evaluation-framework.md` for the scoring method. Current
status: 4 evaluation cases run, scores recorded in `RESULTS.md` — not yet used
on real-world engineering work by a second party, so Maturity remains capped at
Level 2 and Trust Status at EXPERIMENTAL pending that evidence.

## Failure Conditions
- Path does not exist or is not readable → CLI exits non-zero with a clear
  stderr message; no partial report is silently treated as complete.
- Python syntax errors in a scanned file → that file's `ModuleInfo.parse_error`
  is set; the file is still counted in inventory but excluded from def/class
  extraction. This does not fail the whole run.
- Non-Python/JS/Java files are inventoried (path/size/language) but not parsed
  for imports — this is expected, not a failure.

## Known Limitations
See `project-memory-bank/12-known-limitations.md`. Summary: non-Python import
extraction is regex-based, not a real parser, and will miss dynamic imports and
re-exports; no cross-file type resolution; no semantic/business-logic
understanding; dependency graph resolution for JS is limited to relative
(`./`, `../`) specifiers, not bundler path aliases.

## Examples
See `examples/codebase-intelligence/example-run.md` for a real run of this
engine against this platform's own repository.

## Provenance
Built in Phase 1 of the Agentic Engineering Skills Platform roadmap
(`project-memory-bank/08-roadmap.md`, ADR-004/005/006 in
`project-memory-bank/11-decisions.md`). Stdlib-only Python engine (no runtime
third-party dependencies) for portability (NFR1).

## Changelog
- 0.1.0 — Initial implementation: scanner, Python AST parser, JS/TS/Java
  heuristic parser, internal dependency graph with hotspot detection, external
  dependency parsing (requirements.txt/pyproject.toml/package.json), JSON and
  Markdown renderers, CLI, evaluation harness with 4 fixtures.
