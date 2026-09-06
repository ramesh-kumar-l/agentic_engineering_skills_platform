# Dependency / Supply Chain

## Metadata
- Version: 0.2.0
- Status: EXPERIMENTAL
- Author: Agentic Engineering Skills Platform
- Maturity: Level 2 — Evaluated Skill (see `evaluations/dependency-supply-chain/RESULTS.md`)
- Compatible Runtimes: Any agent runtime with Bash/shell tool access, Python 3.10+,
  and the ability to judge whether a mechanically-flagged dependency risk
  actually matters for THIS project (this skill's core value is judgment —
  is an unpinned range dangerous here, is a known-risk name still in active
  use, is a duplicate version conflict a real problem — not just deterministic
  pattern matching)

## Purpose
Given a real `codebase-intelligence` report for a repo, produce a
deterministic **Dependency Risk Report** — pin status, known-risk name
matches, duplicate/conflicting version declarations, and dependency surface
area, each kept as an explicit, separate field — that an agent uses to
assess supply-chain hygiene risk before a human decides whether it matters
for this release. This is the eleventh skill in the portfolio, and the
seventh to compose on a required `codebase-intelligence` report (ADR-010).

## Problem
Dependency risk is usually either ignored entirely (no one looks at
`requirements.txt` until something breaks) or handled by an external SaaS
vulnerability scanner this project deliberately doesn't have (no network
calls — stdlib-only, offline, ADR-006). Between those two extremes is real,
offline-checkable signal: is a version pinned at all, does the same package
get declared with two different versions in two different manifests, does a
declared name match a well-documented deprecation/abandonment history. None
of that requires a live CVE feed, and none of it existed anywhere in this
project before this skill.

## When to Use
- Before merging a dependency bump, or periodically, to see which direct
  dependencies are unpinned, duplicated with conflicting versions, or match
  a known-risk name pattern — as leads for a human to verify, not verdicts.
- As a genuine, mandatory composition point on `codebase-intelligence`'s
  `external_dependencies` field — this skill never re-parses manifests
  itself (see Known Limitations for why, and what that means for coverage).
- As one input alongside a real dependency-audit process (e.g. `pip-audit`,
  `npm audit`, or a paid SCA tool) — this skill does not replace live
  vulnerability-database lookups, it only covers what's checkable offline.

## When NOT to Use
- **As a vulnerability scanner.** This skill has no CVE/advisory database
  and makes no network calls. It cannot tell you a specific installed
  version is exploitable. If you need that, use a real SCA tool
  (`pip-audit`, `npm audit`, Dependabot, Snyk, etc.) — this skill is a
  complement, not a substitute.
- **As a license-compliance tool.** Per-dependency license data is not
  available from manifest declarations alone (a manifest's own `license`
  field describes the *project's* license, not each dependency's) — this
  skill deliberately does not attempt to fabricate a "license risk" signal
  from data it doesn't have. See Known Limitations.
- On a repository with no `codebase-intelligence` report yet — run that
  skill first; this skill refuses to run without one (ADR-010, reused a
  seventh time) rather than silently guessing a dependency list.
- As proof "zero dependencies found" means a clean supply chain — it may
  mean the repo's manifests live somewhere `codebase-intelligence`'s
  `external_deps.py` doesn't look (non-root-level, or a format it doesn't
  parse — Pipfile, poetry's own dependency table). The engine emits an
  explicit warning and fails closed to `REQUIRES_REVIEW` in this case,
  never a silent `CLEAR`.
- As proof a dependency NOT flagged by `risk_patterns.py`'s known-risk table
  is safe — that table is five entries, explicitly non-exhaustive, each
  citing a specific public incident so the flag is verifiable.

## Preconditions
- A `codebase-intelligence` `report.json` already generated for the target
  repo (**hard precondition** — ADR-010, reused a seventh time; run
  `python -m engine.cli <path> --format json --out <dir>` from
  `skills/codebase-intelligence/` first).

## Inputs
- `--ci-report <path>` (required): path to the `report.json` above.

## Required Context
The full `codebase-intelligence` report's `external_dependencies` list
(name/version/source_file per declared dependency) — this is the entire
grounding surface; the engine derives nothing about the target repo beyond
that field.

## Context Completeness
`codebase-intelligence`'s `external_deps.py` parses root-level
`requirements.txt`, `pyproject.toml` (`[project.dependencies]` block only),
`package.json` (`dependencies`/`devDependencies`), and — since ADR-022 —
root-level Maven `pom.xml` (direct `<dependencies>` block only, not
`<dependencyManagement>` or profile-scoped dependencies) and Gradle
`build.gradle`/`build.gradle.kts` (common single-line string-notation
dependency declarations only) — see [[12-known-limitations]] L2, L33. This
engine inherits that scope exactly: no transitive/lockfile resolution, no
non-root manifests, no `Pipfile` or poetry-native
`[tool.poetry.dependencies]` support, no Gradle version catalogs or
map-notation. `classify_pin_status` additionally recognizes Maven version
ranges, Gradle dynamic versions, and unresolved Maven `${property}`
placeholders (a fourth pin-status, `"unresolved"`, distinct from
range/wildcard) when the source manifest is `pom.xml`/`build.gradle[.kts]`.
A zero-dependency result triggers an explicit warning rather than being
treated as a clean bill of health.

## Security Constraints
- Read-only. Never installs, upgrades, removes, or executes any dependency.
- Never fetches anything over the network — pattern tables are static,
  bundled data, not a live feed.
- `suggested_risk_level` is always advisory (ADR-011 precedent) — the
  engine never blocks a merge or install itself; only a human, via the
  agent's workflow, makes that call.

## Workflow
1. **Gather inputs** — confirm a `codebase-intelligence` report.json exists
   for the target repo; generate one first if not (hard precondition).
2. **Run the engine** — `python -m engine.cli --ci-report <path> --format both`.
3. **Agent walks the Dependency Risk Checklist** (see
   [[05-evaluation-framework]]):
   ```
   1. Manifest completeness (via CI report — note any zero-dependency warning)
   2. Pin status assessment (which unpinned/wildcard deps matter here)
   3. Known-risk pattern matches (verify each against its cited incident)
   4. License risk — NOT available this version; state that explicitly
      rather than guessing (see Known Limitations)
   5. Duplicate/conflicting version declarations
   6. Surface-area assessment (unpinned %, manifest breakdown)
   7. Recommendation (advisory risk level + rationale) — framed as advice
      to a human, never a self-executed gate
   8. Explicit uncertainty flag — if evidence is inconclusive (e.g. very
      few dependencies found, or the CI report warned), say so and default
      toward REQUIRES_REVIEW; never silently CLEAR
   ```

## Agent Responsibilities
Verify each flagged known-risk name against its cited public incident
before repeating it as fact; weigh whether an unpinned range is actually
dangerous for this project's release cadence; never claim a license-risk
finding this version doesn't produce.

## Tool Permissions
Read-only filesystem access to the CI report and (optionally) to write
output files. No network access, no package-manager invocation.

## Human Checkpoints
A human (or the calling agent on the human's behalf) decides whether to
act on `suggested_risk_level` — e.g. block a merge, request a manifest
fix, or accept the risk. The engine's output is a recommendation only.

## Outputs
`DependencySupplyChainReport` (JSON and/or Markdown) — see `engine/models.py`.

## Verification
Every claim traces to a specific dependency record or flag in the report;
run `pytest` in this skill's directory (46 tests) to confirm deterministic
behavior on the fixtures in `tests/`.

## Evaluation
See `evaluations/dependency-supply-chain/RESULTS.md`. Deterministic layer:
unit tests per engine module. Judgment layer: 8 hand-authored fixtures,
scored the same self-authored/single-rater way as every other judgment
skill in this project (L8) — disclosed as such, not overclaimed.

## Failure Conditions
Hard-fails (non-zero exit, `CiReportError`) on a missing or malformed
`codebase-intelligence` report — never proceeds on a guessed dependency list.

## Known Limitations
- No live CVE/vulnerability-database lookup — offline-only scope decision,
  not a bug. Use a real SCA tool alongside this skill for that.
- No per-dependency license-risk detection in this version — manifest
  `license` fields describe the project's own license, not each
  dependency's; real per-dependency license data needs installed-package
  metadata inspection, which this skill does not do (see `scanner.py`
  module docstring). Named as a future-evolution item, not silently dropped.
- No lockfile-based exact-pin resolution — inherits `codebase-intelligence`'s
  manifest-only, root-level-only parsing (L2).
- `risk_patterns.py`'s known-risk name table is five entries, explicitly
  non-exhaustive — absence of a match proves nothing.

## Examples
See `examples/dependency-supply-chain/example-run.md` — a real dogfood run
against this repo's own root manifest.

## Provenance
Built in Phase 11, composing on `codebase-intelligence` (Phase 1) per
ADR-010's established pattern, following the mentor-review pause documented
in `project-memory-bank/active-context.md` (2026-08-26) — started at the
user's explicit direction, not because A2/A5 moved off `UNKNOWN`.

## Changelog
- 0.1.0 (2026-08-26): Initial release.
- 0.2.0: Maven/Gradle-aware pin-status classification (ADR-022, user-directed
  cross-cutting scope, not a new roadmap phase) — `classify_pin_status` gains
  an `ecosystem` parameter and a fourth status, `"unresolved"`, for an
  unresolved Maven `${property}` version. 9 new tests (46 → 55).
