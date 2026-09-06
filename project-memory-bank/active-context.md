# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

**2026-09-06 update**: a newly-proposed pivot (a broader "Project-Aware
Test Engineering Platform" per an externally-supplied master system
prompt, logged as [[11-decisions|ADR-023]]) is now underway, at the user's
explicit direction, **separately from** the closed 15-skill portfolio
below. Its own phase sequence ("TEP Phase N") is unrelated to this
section's Phase 1–15 numbering — see
[[18-test-engineering-platform-contract]]'s naming note. TEP Phase 0
(repository/memory understanding), TEP Phase 1 (Product Contract), TEP
Phase 2 (Evidence Foundation — a new `evidence/` package, see
[[11-decisions|ADR-024]]), TEP Phase 3 (Project Intelligence extensions — a
new `project_intelligence/` package, see [[11-decisions|ADR-025]]), and now
TEP Phase 4 (Test Environment Discovery, Android/JVM specifically —
extends `project_intelligence/` with `android_test_frameworks`/
`android_frameworks_absent`, see [[11-decisions|ADR-026]]), and now TEP
Phase 5a (Test Strategy Engine — a new `test_strategy/` package, see
[[11-decisions|ADR-027]]), TEP Phase 5b's Scenario Planner sub-initiative (a
new `scenario_planner/` package, see [[11-decisions|ADR-028]]), and now TEP
Phase 5c's Test Generation & Independent Validation sub-initiative (two new
packages, `test_generation/` and `test_validation/`, see
[[11-decisions|ADR-029]]), and now TEP Phase 5d's Security/Production
Hardening sub-initiative (path containment, bounded subprocess capture,
resource caps, JSON loader type validation, and a declared `pytest`
runtime dependency — no new package, five existing files hardened, see
[[11-decisions|ADR-030]]) are all complete; TEP Phase 5e and beyond has not
started and requires its own separate, explicit user instruction, per the
master prompt's own hard-stop rule. Separately, a cross-cutting **public-
documentation completion pass** (not a TEP phase — same framing as
ADR-022's Java/Kotlin work) is also now complete: the TEP pipeline is now
described in the root `README.md`/`QuickStarterGuide.md`/`DEPENDENCIES.md`,
a new whole-pipeline overview exists at [[25-tep-pipeline-overview]], and
five new blog posts extend the existing series (see
[[11-decisions|ADR-031]]). See "What TEP Phase 1 built", "What TEP
Phase 2 built", "What TEP Phase 3 built", "What TEP Phase 4 built", "What
TEP Phase 5a built", "What TEP Phase 5b built", "What TEP Phase 5c built",
"What TEP Phase 5d built", and "What the public-documentation pass built"
below. This does not change the status of
the closed 15-skill portfolio described in the rest of this section.

Phase 15 (`engineering-memory`) — COMPLETE. **This completes the
originally-scoped 15-skill portfolio named in [[08-roadmap]] — there is
no Phase 16 in that list.** 2026-08-26 (same day, seven sub-events): (1)
the user requested a mentor-style critique of the whole project, which
found ten phases shipped, zero real external users, A2/A5 still UNKNOWN,
and the L23/L24 substring bug disclosed four times without being fixed —
the user approved pausing new-skill work to fix that bug and scaffold a
measurement harness instead (see "Mentor-review follow-up" below); (2)
the user then explicitly directed starting Phase 11 anyway, with their
own exit criteria ("same bar," first skill composing on
`codebase-intelligence`'s output, "production-level stable") — **this
reopened the freeze at the user's explicit direction, not because A2/A5
moved off UNKNOWN**; (3) Phase 11 shipped, and the operating charter was
checked in as a documentation-only pass (see "Documentation check-in"
below); (4) the user then explicitly directed starting Phase 12, with the
same shape of exit criteria — **a second, one-time reopening of the same
freeze**, and Phase 12 shipped (see "What Phase 12 built" below); (5) the
user then explicitly directed starting Phase 13, with the same shape of
exit criteria — **a THIRD one-time reopening of the same freeze**, and
Phase 13 shipped (see "What Phase 13 built" below); (6) the user then
explicitly directed starting Phase 14, with the same shape of exit
criteria — **a FOURTH one-time reopening of the same freeze, and the
first to also directly override a named, phase-specific decision**
(`16-assumptions-and-validation.md` A10 had explicitly said "do not build
Workflow Composer (Phase 14) until Experiment B can be run"), and Phase
14 shipped (see "What Phase 14 built" below); (7) the user then
explicitly directed starting Phase 15, with the same shape of exit
criteria — **a FIFTH one-time reopening of the same freeze**, but unlike
Phase 14, this one did not override a named phase-specific decision — A8's
own "design only when reached" gate was satisfied simply by reaching
Phase 15 in its designated order — and Phase 15 shipped (see "What Phase
15 built" below). The freeze remains in force for any further skill
work — starting Phase 11 through Phase 15 were each one-time, explicit
exceptions, not a general unfreezing, and Phase 15's completion means any
further skill is a newly-proposed scope, not "the next phase in the
list."

## What TEP Phase 1 built

Wrote [[18-test-engineering-platform-contract]] — the Product Contract for
the master-prompt-directed pivot ([[11-decisions|ADR-023]]): mission,
problem, target user, JTBD, a thesis restated as continuous with this
project's existing ADR-005/007 deterministic-plus-judgment architecture
(not a new philosophy), explicit scope/non-goals, an honest current-maturity
baseline reusing TEP Phase 0's audit (generation and independent validation
both genuinely don't exist yet; Android-framework readiness is zero;
evidence/provenance schema doesn't exist), a proposed-only north-star
metric (Verified Useful Test Rate — zero real measurements, flagged the
same way [[16-assumptions-and-validation]] flags every other unproven
assumption here), and exit criteria for the three phases with enough
information to scope now (TEP Phase 2 Evidence Foundation, TEP Phase 3
Project Intelligence extensions, TEP Phase 4 Android/JVM Test Environment
Discovery) — later phases deliberately left undefined, same
anti-speculation discipline as ADR-006/009. No code written; no skill
touched; no test count changed. ADR-023 updated with an addendum recording
this; still logged as **Proposed, not Adopted** — TEP Phase 2 requires its
own separate, explicit user instruction before starting.

## What TEP Phase 2 built

Implemented [[19-evidence-provenance-schema|the run-provenance schema]] as
a new, independently-packaged component at `evidence/` (own
`pyproject.toml`, stdlib-only, own CI job) — not code inside any existing
skill, not a new skill directory. `evidence/capture.py` invokes a target
skill's real CLI as a subprocess (never imports a skill's `engine`
package directly, following ADR-010's precedent) and produces a
`RunProvenance` record: skill name/version, target repo/commit (read from
`.git/HEAD` directly, no `git` binary dependency), start/end time, real
exit code and status, and a SHA-256 of the actual output produced.
`model`/`prompt_version` stay `None` — no skill's engine makes a model
call today; the fields are reserved for a future AI-driven phase, not
backfilled. Demonstrated on a real, non-fixture run —
`python -m evidence.cli codebase-intelligence .` against this repo's own
current commit — with the result hand-verified and committed at
`examples/evidence/example-run.md` /
`examples/evidence/provenance-record.json`. 16 new unit tests, all
passing; every module in `evidence/` stays under 300 lines (largest is 77).
See [[11-decisions|ADR-024]] for the full decision record, including two
schema fields considered and deliberately rejected (`repo_dirty`,
`platform_commit`).

## What TEP Phase 3 built

Implemented [[20-test-environment-profile-schema|the TestEnvironmentProfile
schema]] as a new, independently-packaged component at
`project_intelligence/` (own `pyproject.toml`, stdlib-only, own CI job) —
not code inside `codebase-intelligence` itself, not a new skill directory.
`ci_report_loader.py` reads a `codebase-intelligence` report.json into its
own lightweight local dataclasses (the exact pattern `feature-planner`'s
`ci_report_loader.py` already established, ADR-010) — never imports
`codebase-intelligence`'s `engine` package. `detect.py` matches
`external_dependencies` entries against exact-key signature tables
(`signatures.py`) to find test frameworks, mock frameworks, and coverage
tools; `detect_build_systems` additionally falls back to checking
already-scanned top-level filenames when a manifest declares zero
dependencies, distinguishing that case as `manifest-only` confidence rather
than claiming it's `dependency-confirmed`. Every finding category is a
list, not a single guessed value, and any category with zero findings is
listed in `unavailable` rather than silently empty. Demonstrated on a real,
non-fixture run — `python -m project_intelligence.cli` against a fresh
`codebase-intelligence` report of `skills/codebase-intelligence` itself —
committed at `examples/project-intelligence/example-run.md`. That run
correctly reported a `manifest-only` build system and all three tooling
categories `unavailable`, and in doing so surfaced a real,
previously-undocumented gap: `external_deps.py` never parses PEP 621
`[project.optional-dependencies]`, so a skill's own genuine `dev =
["pytest>=7.0"]` declaration is invisible to it — now logged as
[[12-known-limitations|L34]]. 20 new unit tests, all passing; every module
in `project_intelligence/` stays under 300 lines (largest is 75). Also
fixed a packaging defect shared with `evidence/`: both packages' flat
`.py`-files-at-root layout broke `pip install -e ".[dev]"` on a clean
checkout (setuptools couldn't resolve automatic package discovery) — fixed
in both `pyproject.toml`s with an explicit `[tool.setuptools] packages`
declaration; left unfixed, both packages' CI jobs would have failed on
every real run. See [[11-decisions|ADR-025]] for the full decision record.

## What TEP Phase 4 built

Extended the existing `project_intelligence/` package (no new package, no
change to `codebase-intelligence`) with Android-specific test-framework
detection: a new `ANDROID_TEST_FRAMEWORK_SIGNATURES` table
(`signatures.py`), one new detector `detect_android_test_frameworks`
(`detect.py`, reusing the existing exact-key matcher unchanged), and two
new `TestEnvironmentProfile` fields — `android_test_frameworks:
list[Finding]` and `android_frameworks_absent: list[str]` (an explicit,
individually-named absence list for exactly the JUnit/Robolectric/Espresso
trio the exit criteria names, computed as a set-difference against matched
labels — never inferred, never guessed). Kept as its own category rather
than merged into Phase 3's generic `test_frameworks`, since the exit
criteria asks about three specific named frameworks individually, which a
category-level flag alone would hide. Demonstrated on a real, non-fixture
Android repo — `android/architecture-samples` (`views` branch), scanned at
the `app/` module level — committed at
`examples/project-intelligence/android-example/example-run.md`. The honest
real result: all three report `unavailable`, **not because they're absent
from the codebase** (the module's real `build.gradle`, quoted in the
example doc, genuinely declares all three) but because every declaration
uses Gradle variable interpolation, which `external_deps.py`'s
literal-string-only regex (L33) cannot resolve. Five other real Android
repos were hand-checked and found to have the identical characteristic —
logged as [[12-known-limitations|L35]]: near-universal real-world
convention, not an edge case. The detection logic's correctness once given
matching data is proven separately via 5 new unit tests
(`test_android_detection.py`) using synthetic fixtures; 5 pre-existing
tests were updated for the new category's effect on `unavailable`. 25
tests total in `project_intelligence/`, all passing; largest module is now
`profile_builder.py` at 81 lines (428 total). See [[11-decisions|ADR-026]]
for the full decision record.

## What TEP Phase 5a built

Given "TEP Phase 5" names eleven distinct, unscoped sub-initiatives, the
user was asked directly which to scope first; chose **Test Strategy
Engine**. Built as a new top-level package, `test_strategy/` (flat layout,
same packaging-fix precedent as `evidence/`/`project_intelligence/`): two
independent lightweight loaders (`regression_report_loader.py` for a
regression-hunter report.json, `profile_loader.py` for a
project_intelligence test-environment-profile.json — no cross-package
import, ADR-010 lineage), `strategy_builder.py` (the decision logic),
`models.py`, `cli.py`. Per the contract's own "extend, not replace ... do
not build a second, competing risk scorer" mandate, `strategy_builder.py`
computes no risk score of its own: priority is copied directly from
regression-hunter's `overall_risk_tier`; the only original logic is
dropping already-covered/deleted files and attaching an environment-
feasibility verdict from the profile's `test_frameworks`. Demonstrated on a
real diff (the historical commit that added `evidence/cli.py`, which
genuinely still has no dedicated test file) against a freshly-generated,
full-repository `codebase-intelligence` report — committed at
`examples/test-strategy/example-run.md`. The honest real result: **zero
targets flagged**, because regression-hunter's own `test_coverage_scanner.py`
falsely reports `evidence/cli.py` as "covered" by nine unrelated skills'
own identically-stemmed `test_cli.py` files — a real, new instance of the
still-open remainder of [[12-known-limitations|L24]], now propagated into
this new consumer by design (reusing the signal rather than re-deriving
it). Logged as [[12-known-limitations|L36]]. The positive "flagged, needs a
test" path — which this real run's own honest data could not exercise — is
proven separately via 8 of the 26 unit tests in `test_strategy/tests/`
using synthetic fixtures. All 6 engine files stay under 300 lines (largest,
`strategy_builder.py`, is 104 lines; 760 total including tests). See
[[11-decisions|ADR-027]] and [[21-test-strategy-report-schema]] for the
full decision record and schema. TEP Phase 5b and beyond requires its own
separate, explicit user instruction before starting.

## What TEP Phase 5b built

Given "TEP Phase 5b" still names ten distinct, unscoped sub-initiatives,
the user was asked directly again which to scope next; chose **Scenario
Planner**. Built as a new top-level package, `scenario_planner/` (same
flat-layout, packaging-fix precedent): three independent lightweight
loaders (`strategy_targets_loader.py` for a test_strategy report.json,
`regression_flags_loader.py` for a regression-hunter report.json,
`ci_module_loader.py` for a codebase-intelligence report.json — no
cross-package import, ADR-010 lineage), `plan_builder.py` (the composition
logic), `models.py`, `cli.py`. Per the contract's own "do not build a
second, competing risk scorer" mandate, `plan_builder.py` computes no
priority/feasibility judgment of its own — those are copied verbatim from
the input test_strategy target. Its only original logic composes two
existing signals into candidate scenarios: one per regression-hunter flag
(citing that flag's own description), and one per function/class in
codebase-intelligence's structural listing (each rationale disclosing that
no line-range data exists to attribute a diff to one specific symbol — a
file-level fallback fires only when neither signal exists for a target).
Demonstrated by reusing the exact real, committed inputs from TEP Phase
5a's own dogfood run — committed at
`examples/scenario-planner/example-run.md`. The honest real result: **zero
plans**, because the upstream test_strategy report it consumes already had
zero targets (Phase 5a's own [[12-known-limitations|L36]] finding,
surfacing one level further downstream by design — no new limitation entry
was needed). The positive "here are this target's candidate scenarios"
path — which this real run's own honest data could not exercise — is
proven separately via 7 of the 26 unit tests in `scenario_planner/tests/`
using synthetic fixtures. All 6 engine files stay under 300 lines (largest,
`plan_builder.py`, is 150 lines; 517 engine lines total). See
[[11-decisions|ADR-028]] and [[22-scenario-plan-report-schema]] for the
full decision record and schema. TEP Phase 5c and beyond requires its own
separate, explicit user instruction before starting.

## What TEP Phase 5c built

The user asked directly what Test Generation would even produce and
whether it was needed; the honest answer (generating unexecuted test code
contradicts the contract's own non-goal on unverified reliability claims)
led to a third disambiguation round, choosing to pair Test Generation with
**Independent Validation** as one phase rather than build generation alone.
Two Explore-agent research passes confirmed codebase-intelligence has no
parameter/type data to derive negative cases from, and that
`project-memory-bank/` is the wrong place for a per-target-repo naming
convention (even the two memory-capture skills never auto-write there).

Built as two new top-level packages. `test_generation/` (`scenario_loader.
py`, `naming_convention.py`, `source_excerpt_reader.py`,
`generation_planner.py`, `models.py`, `cli.py`) never authors test code
itself — codebase-intelligence's name-only structural data can't support
deriving real negative conditions, so this engine produces a plan (real
source excerpt, inferred-or-overridden naming convention, 1 positive + 4
negative slot requests) for the calling agent to author from, writing files
under `--out/generated-tests/`, never into the target repo. The naming
convention is inferred fresh each run (majority vote over the target repo's
real test files, reusing regression-hunter's own file-recognition
heuristic) or supplied via `--naming-convention-file` pointing at a prior
run's own output — an explicit config file, not a hidden cache.
`test_validation/` (`generated_tests_loader.py`, `environment_loader.py`,
`validation_runner.py`, `report_builder.py`, `models.py`, `cli.py`) executes
those agent-authored files via subprocess with a strict timeout — this
platform's first execution capability; every prior skill and TEP package is
pure static analysis. Disclosed explicitly: no filesystem/network
sandboxing beyond the timeout is claimed.

Demonstrated twice: once reusing TEP Phase 5b's exact real (zero-candidate)
output, honestly reproducing the same inherited zero result; once against a
synthetic-but-real scenario-plan-report.json naming an actual symbol in
this repo (`test_generation/naming_convention.py`'s `_classify`), producing
a real plan with a real source excerpt, from which an agent authored a real
5-test file (1 positive + 4 negative, all genuinely distinct), which
`test_validation` then actually executed via subprocess and reported
passing. That real run found and fixed two real bugs — a relative-path
resolution error in `validation_runner.py` and an unfiltered
`.pytest_cache` artifact in `generated_tests_loader.py` — that the 51 unit
tests written before it (all using absolute `tmp_path` fixtures) did not
surface; both fixed with new regression tests, not just disclosed. All 12
engine files across both packages stay under 300 lines (largest,
`validation_runner.py`, is 109 lines; 906 engine lines total; 54 new
tests, 148 total across all TEP packages). See [[11-decisions|ADR-029]],
[[23-generation-plan-report-schema]], and
[[24-validation-report-schema]] for the full decision record and schemas.

## What TEP Phase 5d built

The user asked to continue toward a "scalable and production level stable
system"; `AskUserQuestion` narrowed TEP Phase 5d's 7-item unscoped bucket
to security/production hardening specifically, with a follow-up
confirming path-containment and resource guards around
`test_validation`'s subprocess execution. An Explore-agent audit (file:line
level) ran first, grounding every change in a real, cited gap.

No new package — five existing files hardened, each narrowing an
already-existing risk surface: (1) `test_validation/
generated_tests_loader.py` and `evidence/skill_info.py` now
resolve-and-contain candidate paths, rejecting symlink- and traversal-based
escapes that were previously accepted with no check; (2)
`validation_runner.py`'s `run_validation` redirects subprocess stdout/
stderr to disk-backed `tempfile.TemporaryFile()` instead of in-memory
`capture_output=True`, so a runaway test printing unbounded output can no
longer exhaust parent-process memory before the existing 30s timeout
fires; (3) `report_builder.py`/`cli.py` add `--max-test-files`/
`--max-test-file-bytes` caps (defaults 200 files / 1 MB), skipping +
warning rather than hard-failing; (4) five JSON loaders
(`test_strategy/profile_loader.py`, `test_validation/environment_loader.
py`, `scenario_planner/ci_module_loader.py`, `project_intelligence/
ci_report_loader.py`, `test_generation/scenario_loader.py`) now reject a
wrong-type top-level container with their own typed error instead of a
raw `TypeError`/`AttributeError`; (5) `test_validation/pyproject.toml`
declares `pytest` as a real runtime dependency, paired with an upfront
`PytestUnavailableError` precondition check.

No sandboxing claim is added — ADR-029's own disclosure stands unchanged;
this pass narrows existing risk surface, it adds no new capability.
Demonstrated by 20 new regression tests (2 of 3 new symlink tests skip
gracefully on this Windows environment's unprivileged symlink-creation
restriction, confirmed via `pytest -rs`, not silently ignored) plus a
full re-run of the real `test_validation` demo post-hardening, same clean
result as before (`exit_code: 0`, `5 passed`). Every modified file stays
under 300 lines (largest, `validation_runner.py`, 130 lines); 166 passed,
3 skipped across the combined TEP suite (up from 148 passed). See
[[11-decisions|ADR-030]] for the full decision record.

## What the public-documentation pass built

At the user's explicit request (make the project's completed work visible
to a first-time reader, and produce publishable technical content), a
research pass first confirmed the concrete gap: the TEP pipeline was
documented only inside `project-memory-bank/`, invisible from every
root-level doc. This pass closed that gap without touching any code:

- New [[25-tep-pipeline-overview]] — the first file showing all 6 TEP
  packages' data flow in one place (a Mermaid diagram + a package→schema→
  command table), since files 19–24 each only document one package's own
  schema in isolation.
- [[12-known-limitations|L37]] (CI has no job for `test_strategy`,
  `scenario_planner`, `test_generation`, `test_validation`) newly disclosed,
  and a cross-reference note consolidating the L2→L34→L35→L36 root-cause
  chain that was previously scattered across three phases.
- A clarifying note under ADR-023 resolving its "Proposed, not Adopted"
  status wording, which reads ambiguously once TEP Phases 1–5d had visibly
  shipped under it.
- Root docs (`README.md`, `QuickStarterGuide.md`, `DEPENDENCIES.md`,
  `requirements.txt`) extended to cover the TEP pipeline; five new blog
  posts (`blogs/07`–`11`) written about the TEP build specifically, so the
  existing 6-post series (15-skill portfolio) isn't duplicated.

All numbers used were re-measured directly in this session (`pytest -q`
across all 21 packages), not carried over from a prior summary. See
[[11-decisions|ADR-031]] for the full decision record.

TEP Phase 5e and beyond requires its own separate, explicit user
instruction before starting.

## Documentation check-in (2026-08-26, after Phase 11 — not a new phase)

The user pasted the full "operating charter" (north-star vision, thesis,
principles, target users, skill portfolio, canonical skill contract,
assumption-tracking methodology) that ADR-001 has adopted since Phase 0 but
that had never actually been checked into the repo. Confirmed by the user as
complete. Filed at [[operating-charter]], cross-linked from ADR-001,
`00-project-vision.md`, `01-product-thesis.md`, and every file that already
cited "the operating charter" by name. One honest gap surfaced and disclosed
rather than papered over: several existing files cite charter sections
(39–40, 43, "First Activation") that don't exist in this version, which only
runs through Section 11 — see [[12-known-limitations|L27]]. No code, tests,
or roadmap changed; Phase 12+ freeze is untouched by this.

## What Phase 15 built

Built `engineering-memory`, the fifteenth and **final skill in the
originally-scoped portfolio** ([[08-roadmap]]) — the first skill whose
primary retrieval corpus is this project's own `project-memory-bank/`
markdown, not a target repo's external artifacts: `SKILL.md` contract
reusing Pattern 2 (ADR-007) a fourteenth time, plus new **ADR-021**. A
deterministic engine (12 modules, each under 300 lines, max
`memory_bank_parser.py` at 148) parses real `## ADR-NNN:` / `## LNN:`
section headers out of `11-decisions.md`/`12-known-limitations.md`
(explicitly skipping `## L8 update:` sub-entries), resolves any
backtick-quoted module mentioned in a record's body against a required
`codebase-intelligence` report (ADR-010, reused an ELEVENTH time) via
basename-EQUALITY (not containment), scores each record against a task
description's whole-token keyword overlap (title-weighted higher than
body, plus a module-overlap boost), and always attaches a staleness flag
— derived from either the record's own `(FIXED...)`/`(SUPERSEDED...)`
title suffix or a mentioned module no longer resolving — the direct,
operational answer to A8's own named risk about stale memory being
treated as authoritative. Word-boundary/whole-token matching was applied
from day one specifically because six prior disclosed limitations
(L14/L19/L21/L23/L24/L28/L29/L30) already proved the substring-
containment alternative fails — applying an accumulated lesson, not
discovering a new one. New **Engineering Memory Retrieval Checklist**
(fourteenth checklist, [[05-evaluation-framework]]). 57 passing tests
(CLI test file and a real end-to-end integration test from the start).
8-fixture evaluation harness, both layers scored perfect — fourteenth
judgment-based skill scored this way, same self-authored caveat (L8);
deterministic fixtures cover clean multi-record fit, no-fit, whole-token
collision resistance (a genuine coincidental match ranks below, never
drowns out, the real one), both staleness paths, `--top-n` truncation,
the missing-CI-report hard failure, and memory-bank header-format drift.
Real dogfood (`examples/engineering-memory/example-run.md`) — a real,
non-fixture retrieval run against this project's own actual 50-record
memory bank (20 decisions, 30 limitations) and a freshly-generated real
`codebase-intelligence` report, using this session's own real Phase 15
task description — 8/8 top matches were substantively on-topic, and both
real staleness signals fired correctly, but found a new,
disclosed-not-fixed limitation: **L31** — `module_resolver.py`'s
basename-exact resolution, built correct from day one specifically to
defeat the L23/L24/L28-class *substring* collision, has a different,
real ambiguity once the corpus is this project's actual many-skill
memory bank: `ci_report_loader.py` (a real, distinct file in most
composing skills) caused five different records about five different
skills (ADR-016, L24, ADR-020, ADR-015, ADR-017) to all resolve their
mention to the same single `root-cause-analyzer` path — a genuinely
different failure mode than the substring class this resolver already
defeats, not a sign that defeat was incomplete. Platform test count rose
from 636 to **693**, zero regressions. `.github/workflows/tests.yml`'s
matrix updated to include the new skill.

## What Phase 14 built

Built `workflow-composer`, the fourteenth skill — the first in the
portfolio whose deliverable is composed **execution**, not analysis:
`SKILL.md` contract reusing Pattern 2 (ADR-007) a thirteenth time, plus
new **ADR-020**. A deterministic engine (12 modules, each under 300
lines, max `step_runner.py` at 152) sequences a small, hardcoded registry
of exactly 3 workflow templates — `understand-then-plan`
(`codebase-intelligence` -> `feature-planner`, reusing Phase 4's real
dogfood composition), `understand-then-test-plan`
(`codebase-intelligence` -> `acceptance-test-engineer`, reproducing Phase
3's real Pilot B composition via a `TEXT_APPEND` wiring mode since
`acceptance-test-engineer`'s CLI has no `--ci-report`-style flag,
confirmed by reading its shipped `engine/cli.py`), and
`understand-then-optimize-context` (`codebase-intelligence` ->
`context-optimizer`, reusing Phase 13's real dogfood composition, via a
`CLI_FLAG` wiring mode) — every template's step 1 is a required
`codebase-intelligence` report (ADR-010, reused a TENTH time). Real
execution subprocess-invokes each named skill's actual `engine/cli.py`;
a `compatibility_checker.py` textual drift guard confirms each step's
declared upstream marker still appears in the downstream skill's real
SKILL.md before trusting the wiring; `executor.py` fails **CLOSED** on
any step failure or a pre-execution compatibility issue — the opposite
default from ADR-019's fail-open content-inclusion inversion one phase
earlier, explicitly framed as the same underlying principle (fail toward
the cheaper-to-recover-from error) pointing the normal direction because
building on a broken step is the expensive failure here, not the cheap
one. New **Workflow Composition Checklist** (thirteenth checklist,
[[05-evaluation-framework]]). 51 passing tests (CLI test file from the
start, plus one genuinely real subprocess-based integration test — no
prior skill's test suite invokes another skill's real code). 8-fixture
evaluation harness, both layers scored perfect — thirteenth judgment-based
skill scored this way, same self-authored caveat (L8); deterministic
fixtures mix real registry-template dry-runs (against a bundled
`tests/fixtures/tiny-repo`) with fixture fake-skill runs (for
deterministic fail-closed-path coverage: a simulated step failure, and a
simulated compatibility drift). Real dogfood
(`examples/workflow-composer/example-run.md`) — a real, non-dry-run
execution of `understand-then-plan` against this repo's own current
(fourteen-skill) state, using this session's own real Phase 14 task
description — both real steps succeeded (2.31s total against 1,010
scanned files, zero compatibility issues), and found a new,
disclosed-not-fixed limitation: **L30** — `feature-planner`'s own
relevance scorer (composed, not computed by `workflow-composer` itself)
ranked a test file
(`skills/workflow-composer/tests/test_real_execution.py`) as the single
highest-scoring file in the entire repository, ahead of every real
implementation file relevant to the task — the same coincidental-
keyword-collision mechanism class `architecture-decision`'s L14/L19/L21
and `context-optimizer`'s L29 already disclosed, now confirmed present
inside `feature-planner` itself (the oldest keyword-relevance engine in
this portfolio), not just `context-optimizer`'s scorer. `workflow-
composer` composes with `feature-planner` as-is; it does not filter or
improve the composed skill's own output. Platform test count rose from
585 to **636**, zero regressions. `.github/workflows/tests.yml`'s matrix
updated to include the new skill; `.gitignore` updated to exclude the
evaluation harness's generated `_run/` working directory.

## What Phase 13 built

Built `context-optimizer`, the thirteenth skill: `SKILL.md` contract
reusing Pattern 2 (ADR-007) a twelfth time — a deterministic engine (12
modules, each under 100 lines, max `models.py` at 95) that scores every
file in a required `codebase-intelligence` report (ADR-010, reused a
ninth time) against a free-text task description's extracted keywords —
matched against path/docstring/functions/classes/imports via a tokenized
whole-token check (the FIFTH independent copy of a containment check in
the L23/L24 lineage, and the SECOND built correct from day one, but using
tokenization on `_`/`/`/`.`/`-` rather than `location_resolver.py`'s
`\b`-regex, a deliberate, disclosed different precision/recall tradeoff)
— boosts a file's score with real fan_in/hotspot structural data
(ADR-013-style reuse), and tiers every nonzero-scoring file
CORE/SUPPORTING/EXCLUDED, optionally against a `--budget-lines` cap. New
**ADR-019** documents the required-composition reuse, the tokenized
relevance scorer's tradeoff vs. Phase 12's regex approach, and — the
headline architectural decision this phase — an explicit **inversion**
of the fail-closed-toward-caution convention ADR-011/017/018 established:
this skill fails **OPEN** toward inclusion under uncertainty instead
(a low-but-nonzero score still earns at least SUPPORTING; a single file
whose own size exceeds the budget is flagged, never silently dropped),
because for a context-recommendation tool, silently excluding a needed
file is the worse failure, not silently including an unimportant one.
New **Context Optimization Checklist** (twelfth checklist,
[[05-evaluation-framework]], decision-gate shaped like the Security,
Dependency Risk, and Knowledge Capture checklists). 64 passing tests (CLI
test file from the start). 8-fixture evaluation harness, both layers
scored perfect — twelfth judgment-based skill scored this way, same
self-authored caveat (L8). Real dogfood
(`examples/context-optimizer/example-run.md`) — a fresh
`codebase-intelligence` report against this repo's current (thirteen-skill)
state, and a real task description drawn from this actual session's own
work — found a new, disclosed-not-fixed limitation: **L29** — at
full-repository scale, keyword relevance floods with false-positive CORE
recommendations when the task description is phrased in this project's
own recurring vocabulary (shared documentation/evaluation-harness
boilerplate repeated across every skill); 5 of 17 CORE recommendations in
the dogfood run were unrelated files (four other skills'
`run_evaluation.py` files plus one unrelated fixture), not
`context-optimizer` files. This is a new manifestation of the same
coincidental-keyword-collision mechanism class `architecture-decision`'s
L14/L19/L21 already disclosed — the second time this exact mechanism
class has been hit on a real dogfood run without either project having
acted on it. Platform test count rose from 521 to **585**, zero
regressions. `.github/workflows/tests.yml`'s matrix updated to include
the new skill.

## What Phase 12 built

Built `engineering-knowledge-capture`, the twelfth skill: `SKILL.md`
contract reusing Pattern 2 (ADR-007) an eleventh time — a deterministic
engine (9 modules, each under 130 lines) that scans a free-text
engineering narrative for four candidate categories (decision, lesson,
limitation, workaround; 16 patterns total, non-exhaustive), resolves any
module mentioned on the matched line against a required `codebase-
intelligence` report (ADR-010, reused an eighth time), and rolls a
resolved candidate's real fan_in/hotspot data into an advisory
`suggested_capture_priority` (HIGH/MEDIUM — LOW is defined but never
assigned this version, a deliberate fail-upward choice under uncertainty).
New **ADR-018** documents the required-composition reuse, the fourth
independent copy of the word-boundary-aware resolution fix first applied
after L23/L24 — this one built correct from day one rather than shipped
with the bug first — and this skill's status as the first in the
portfolio whose deterministic layer targets a documentation artifact (an
ADR/known-limitation/lessons-learned candidate) rather than a code-risk
judgment. New **Knowledge Capture Checklist** (eleventh checklist,
[[05-evaluation-framework]], decision-gate shaped like the Security and
Dependency Risk checklists). 47 passing tests (CLI test file from the
start). 8-fixture evaluation harness, both layers scored perfect —
eleventh judgment-based skill scored this way, same self-authored caveat
(L8). Real dogfood (`examples/engineering-knowledge-capture/example-run.md`)
against a narrative built from genuine excerpts of this project's own
engineering history (the L23/L24 fix, Phase 11's dropped license-detection
decision) found a new, disclosed-not-fixed limitation: **L28** —
`location_resolver.py` only checks the exact matched line for a module
mention, not the surrounding paragraph, so every candidate in that real
run resolved to no location at all despite `target_resolver.py` being
named four times in the sentence immediately above the flagged markers.
This is the first dogfood run in this project's history whose finding is
about a gap between synthetic-fixture behavior and real-prose behavior
specifically (every evaluation fixture deliberately puts the module
mention in the same sentence as the marker; real retrospective writing
often doesn't). Platform test count rose from 474 to **521**, zero
regressions. `.github/workflows/tests.yml`'s matrix updated to include the
new skill.

## What Phase 11 built

Built `dependency-supply-chain`, the eleventh skill: `SKILL.md` contract
reusing Pattern 2 (ADR-007) a tenth time — a deterministic engine (11
modules, each under 100 lines) that reuses a required `codebase-
intelligence` report's `external_dependencies` field (ADR-010, reused a
seventh time) and produces four explicit signals — pin status (missing/
wildcard/range/pinned, covering both pip- and npm-style specifiers), a
5-entry curated known-risk-name table (each citing a real public incident,
exact-name matched, not substring), duplicate/conflicting version
declarations across manifests, and surface-area stats — rolled into one
advisory, fail-closed `suggested_risk_level` (CLEAR/NEEDS_REVIEW/
REQUIRES_REVIEW), reusing `security-context-guard`'s ADR-011 discipline.
**Corrected mid-implementation**: the original plan included a
`license_patterns.py` module for per-dependency license-risk detection;
this was dropped once it became clear a manifest's `license` field
describes the *project's* license, not each dependency's, and no such data
is actually available from what `codebase-intelligence` parses — shipping
a fabricated-looking license flag was rejected in favor of naming the gap
explicitly (L26). 46 passing tests (CLI test file from the start). New
**ADR-017** documents both the required-composition reuse and the two
explicit scope decisions (no live CVE lookup, no license-risk detection).
New **Dependency Risk Checklist** (tenth checklist,
[[05-evaluation-framework]], decision-gate shaped like the Security
checklist). 8-fixture evaluation harness, both layers scored perfect —
tenth judgment-based skill scored this way, same self-authored caveat (L8).
Real dogfood (`examples/dependency-supply-chain/example-run.md`) against
this repo's own root manifest found only 1 real dependency (`pytest`),
concretely confirming the inherited L2 root-level-only scope gap (the
platform's real per-skill dependencies live in `skills/*/pyproject.toml`,
one level below repo root). New known limitations L25 (no live CVE
database, permanent scope decision) and L26 (no per-dependency license
data, corrected-during-build scope decision). Platform test count rose
from 428 to **474**, zero regressions. `.github/workflows/tests.yml`'s
matrix updated to include the new skill.

## Mentor-review follow-up (2026-08-26, before Phase 11)

1. **Fixed L23 fully, L24 partially** — replaced the bare substring check
   (`target_stem in imports_text`) with a word-boundary-aware match
   (`\b<stem>\b`) in `refactoring-safety/engine/target_resolver.py`,
   `regression-hunter/engine/target_resolver.py`,
   `release-readiness/engine/target_resolver.py`, and
   `release-readiness/engine/test_coverage_scanner.py`. This closes the
   embedded-substring collision class (e.g. "scanner" inside
   "testability_scanner") that L23 fully described. It does **not** close
   L24's headline example — two different skills each legitimately
   importing their own identically-stemmed `models.py` still produces a
   real, boundary-respecting match, since the resolver has no notion of
   "same skill" path scoping. See `12-known-limitations.md`'s updated L23
   (FIXED) and L24 (PARTIALLY fixed, narrowed scope) entries for the exact
   distinction — do not read this as L24 being closed. 8 new regression
   tests added (2 refactoring-safety, 2 regression-hunter, 4
   release-readiness); platform test count rose from 420 to **428**, all
   passing, zero regressions.
2. **Scaffolded `evaluations/usage-comparison/`** — a before/after
   token/turns/time measurement harness, the first artifact in this project
   that can log a real task run both with a skill and with plain prompting.
   Ships empty (no fabricated numbers); see its README for the same
   self-run-pilot honesty caveat every other harness here carries.

Both items were the "purely technical" half of a broader checklist the
mentor critique produced (see the session's chat history / plan file for
the full checklist) — the remaining items (get one real external user, run
an independent/blind eval pass, actually log real usage-comparison runs)
require the user's own action outside this session and were explicitly
left to them.

## Prior phase summary (historical)

## What Phase 10 built

Built `release-readiness`, the tenth skill and the final skill in the
Engineering Lifecycle group: `SKILL.md` contract reusing Pattern 2
(ADR-007) a ninth time — a deterministic engine (16 modules, each under
300 lines, max 211) that parses a unified git diff (independent copy of
`regression-hunter`'s/`adversarial-diff-reviewer`'s parsing conventions)
into structured per-file hunks, scans those hunks directly for four
mechanically-detectable, release-blocking diff-hygiene shapes (debug
leftovers, merge-conflict markers, hardcoded-secret-shaped literals,
TODO-blocking markers), resolves each changed file against a real
`codebase-intelligence` report (a THIRD independent copy of
`refactoring-safety`'s/`regression-hunter`'s `target_resolver.py`
pattern), checks an independently-computed test-coverage signal, and
combines these three ALWAYS-AVAILABLE axes into one `readiness_tier` per
file via a documented rule table. Two FURTHER axes — a supplied
`regression-hunter` report's `overall_risk_tier` and a supplied
`security-context-guard` report's `suggested_verdict` — are OPTIONAL,
loaded via `--regression-report`/`--security-report`, surfaced verbatim,
and deliberately excluded from the rule table. Per-file tiers roll up into
one report-level `overall_verdict`
(`NOT_READY`/`READY_WITH_CONDITIONS`/`READY`), explicitly and repeatedly
framed everywhere as a recommendation for a human to review, never an
autonomous release gate. 78 passing tests, including a CLI test file
written from the start (same discipline Phases 5-9 established). Combined
with an agent-driven Release Readiness Checklist workflow — a new, ninth
checklist in [[05-evaluation-framework]] (10 categories: scope stated
precisely, diff-hygiene blockers reviewed as absolute, structural blast
radius grounded in real data, test coverage distinguished per file,
regression/security evidence surfaced-not-re-derived when present and
explicitly marked absent when not, overall verdict explained via the rule
table, false-positive check, evidence cited, assumption flag, and a
non-negotiable tenth category — verdict framed as advisory/human-
checkpoint, never an auto-gate — unique to this checklist because this
skill's output is this portfolio's single highest-stakes recommendation).

**Architecture**: reuses `feature-planner`'s/`root-cause-analyzer`'s/
`architecture-decision`'s/`refactoring-safety`'s/`regression-hunter`'s
mandatory-composition rule (ADR-010) a sixth time — a missing/malformed
`codebase-intelligence` report is a hard failure, not a degraded path,
stated explicitly as a *reuse*. New this phase: **ADR-016** — the Release
Readiness Scorecard combines three always-available, non-blended per-file
signals into a `readiness_tier` via a documented rule table (any hygiene
flag -> blocked; high structural tier with no coverage -> blocked; high or
medium structural tier, or no coverage -> needs-review; otherwise clear),
and is the FIRST skill in this platform to also compose OPTIONALLY with
TWO OTHER skills' own real outputs (not just `codebase-intelligence`'s) —
reusing `security-context-guard`'s ADR-011 optional-composition precedent
for those two specifically, rather than ADR-010's mandatory rule. The
optional evidence is surfaced but deliberately never blended into the rule
table, since each is already a rolled-up verdict from a DIFFERENT skill's
own rule table, and re-blending it would hide which skill produced which
judgment.

**Evaluation**: an 8-fixture harness (`evaluations/release-readiness/`),
same two-layer scoring (deterministic + judgment) as Phases 2-9. This is
the **ninth** judgment-based skill evaluated with self-authored,
single-rater fixtures. All 8 fixtures scored perfect precision/recall on
both layers — stated plainly as *not* evidence of higher judgment quality
than Phase 6's non-perfect score (`root-cause-analyzer`'s case-03,
0.67/0.67); a single self-authored evaluation cannot support that
comparison either way. Two fixtures deliberately exercise real divergence:
case-03 has ZERO diff-hygiene flags but is still `readiness_tier=blocked`
because a real hotspot with no test coverage is an absolute blocker on its
own (Axis 2/3 alone can block, hygiene is not the only path); case-07 has
a CLEAR `readiness_tier` from Axes 1-3 while a composed regression-hunter
report shows `overall_risk_tier=high` for the same file — independent
signals that can and do disagree, by design.

**Dogfood run** (`examples/release-readiness/example-run.md`):
regenerated a fresh `codebase-intelligence` report against this repo's
current (10-skill) state, then ran a real `git diff` of this phase's own
actual body of work — 78 new files, staged (never committed) with `git
add`, diffed with `git diff --cached`, then immediately unstaged with
`git reset`. The run confirmed, concretely, a limitation `SKILL.md`'s
Known Limitations had already predicted before the run: the
`debug-print-leftover` hygiene pattern fired 5 times on this skill's own
`engine/cli.py` and `run_evaluation.py`, every one a legitimate CLI
stdout/stderr `print()` call, not a debug leftover — left unfixed by
design (the documented boundary between the hygiene table and the agent's
Step 4 false-positive-check judgment). It also surfaced, and deliberately
did **not** fix, a new, materially more consequential finding: **L24** —
`target_resolver.py`'s substring-based resolution, a THIRD independent
copy of the exact heuristic already disclosed as L23, was shown for the
first time to produce **false-positive test coverage** (not just an
inflated caller list) when a module's stem (e.g. `models`, `stats`,
`report`) collides with an identically-named module in an unrelated
skill — `skills/release-readiness/engine/models.py` resolved as "covered"
by `architecture-decision`'s test files despite having no
`tests/test_models.py` of its own. This is a more consequential category
of finding than L23: L23 inflated a displayed field without changing that
run's outcome; L24 corrupts the exact signal (`test_coverage.has_coverage`)
the readiness rule table uses to decide whether a structurally
consequential file needs closer review.

**Memory-bank updates this phase**: `05-evaluation-framework.md`
(Release Readiness Checklist), `11-decisions.md` (ADR-016),
`12-known-limitations.md` (L24, L8 update), `16-assumptions-
validation.md` (A5, A10 updated), `08-roadmap.md` (Phase 10 marked
complete, Phase 11 proposed next), `implementation-status.md`,
`07-current-state.md`, `03-architecture.md`, `sprint-history/SPRINT-10.md`,
root `README.md`/`ROADMAP.md`/`QuickStarterGuide.md`/`DEPENDENCIES.md`/
`CHANGELOG.md`.

## Open threads / not yet decided

- **2026-08-26 update: Phase 11 through Phase 15 all shipped at the
  user's explicit direction; the originally-scoped 15-skill portfolio is
  now complete, and no further phase exists in [[08-roadmap]]'s list.**
  The mentor-review critique concluded velocity of building had
  outpaced velocity of validating (A2/A5 both UNKNOWN after ten phases,
  zero real external users), and the user then explicitly directed
  starting Phase 11, later the same day Phase 12, later the same day
  Phase 13, later the same day Phase 14, and later the same day Phase 15,
  anyway. Phase 14 additionally overrode a named, phase-specific decision
  (A10) rather than only the general freeze — the only phase to do so;
  Phase 15's own gating decision (A8's "design only when reached") was
  satisfied simply by reaching it in order, so it did not need that same
  kind of override. Each is a one-time, explicit exception, not new
  evidence and not a general unfreezing — re-justifying ANY further skill
  work now still requires real external validation evidence first (a real
  user, an independent/blind eval pass, or a real usage-comparison run via
  `evaluations/usage-comparison/`), not just a pre-written roadmap
  proposal. This tension is now deferred across five consecutive phase
  boundaries.
- **L8 remains the most important open thread, now applying fourteen
  times**: thirteen of fourteen judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard,
  architecture-decision, refactoring-safety, regression-hunter,
  release-readiness, dependency-supply-chain, engineering-knowledge-capture,
  context-optimizer, workflow-composer, engineering-memory) scored 100%
  precision/recall against self-authored ground truth; the fourteenth
  (root-cause-analyzer) scored 7/8 perfect and 1/8 at 0.67/0.67 (L19). All
  outcomes are equally inconclusive about real-world quality —
  self-authored, single-rater evidence either way. The inter-rater-
  agreement experiment (A5) still has not been run for any of the
  fourteen.
- **L25/L26 (Phase 11)**: `dependency-supply-chain` has no live
  CVE/vulnerability-database lookup (L25, permanent scope decision — this
  project makes no network calls, ADR-006) and no per-dependency
  license-risk detection (L26, corrected mid-implementation — the data
  needed doesn't exist in what `codebase-intelligence` parses; dropped from
  scope rather than fabricated). Both named explicitly in `SKILL.md`, not
  silently omitted.
- **L28 (new, Phase 12)**: `engineering-knowledge-capture`'s
  `location_resolver.py` only checks the exact matched line for a module
  mention, not the surrounding paragraph — found via a real dogfood run
  where every candidate resolved to no location despite the relevant
  module being named four times nearby. Disclosed, not fixed — widening
  the window risks a new false-positive class this project has no evidence
  is rarer than the false negative just found.
- **L29 (new, Phase 13)**: `context-optimizer`'s `relevance_scorer.py`
  floods with false-positive CORE recommendations at full-repository
  scale when the task description is phrased in this project's own
  recurring vocabulary — a real dogfood run found 5 of 17 CORE
  recommendations were unrelated files (other skills' `run_evaluation.py`
  boilerplate), not `context-optimizer` files. Same mechanism class as
  `architecture-decision`'s L14/L19/L21, a new manifestation of it, and
  the second time this exact mechanism class has been hit on a real
  dogfood run without either project having acted on it. Disclosed, not
  fixed — a real fix (TF-IDF-style down-weighting, or a
  keyword-specificity threshold) has not been evaluated against real
  evidence of need beyond this one dogfood run.
- **L30 (new, Phase 14)**: `workflow-composer`'s real dogfood run found
  the SAME mechanism class inside `feature-planner`'s own scorer this
  time — composing with `feature-planner` (via `understand-then-plan`)
  ranked a test file above every real implementation file relevant to the
  task. `workflow-composer` itself has no keyword-scoring logic to blame;
  it composes with `feature-planner` as-is and does not filter its
  output. This is the THIRD real-dogfood-run instance of the same
  mechanism class (after `architecture-decision`'s L21 and
  `context-optimizer`'s L29), now confirmed present in the oldest
  keyword-relevance engine in this portfolio (Phase 4), not just the
  newest one. Disclosed, not fixed — same standing rationale as L29.
- **L31 (new, Phase 15)**: `engineering-memory`'s real dogfood run found a
  DIFFERENT failure mode from the L14/L19/L21/L23/L24/L28/L29/L30
  substring-collision class: `module_resolver.py`'s basename-EQUALITY
  resolution (built correct from day one specifically to defeat that
  substring class) still collapses multiple real, distinct files sharing
  a common basename (`ci_report_loader.py`, real in most composing
  skills) into whichever one the CI report lists last — five different
  records about five different skills all resolved to the same
  `root-cause-analyzer` path. Does not affect relevance scoring, only
  which file a match's `matched_modules` list names. Disclosed, not
  fixed — same "one real data point, don't guess a fix" discipline.
- **The L14/L19/L21/L23/L24 substring-collision limitation class — status
  as of 2026-08-26: L23 FIXED, L24 PARTIALLY fixed, L14/L19/L21 still
  open.** `target_resolver.py`'s caller-identification bug (L23, shared
  across `refactoring-safety`/`regression-hunter`) and its embedded-
  substring subclass in `release-readiness`'s `test_coverage_scanner.py`
  (part of L24) are fixed via a word-boundary-aware match — see
  `12-known-limitations.md`. L24's headline example (two skills'
  identically-stemmed modules producing a real, boundary-respecting
  false-positive coverage match) remains open — closing it needs
  repo-layout-aware path scoping, deliberately not implemented this pass.
  L14 (`feature-planner/relevance_scorer.py`), L19
  (`root-cause-analyzer/candidate_scorer.py`), and L21
  (`architecture-decision/impact_scorer.py`) are a related but distinct
  keyword-relevance-scoring limitation class in different files — NOT
  touched by this fix, still open.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, C) found
  plausible-but-narrow signal on N=1 each; Phase 10's dogfood run is
  additional real-usage evidence for A10, sharpening Phase 9's finding —
  composition executed correctly and was genuinely used (including, for the
  first time, the two OPTIONAL cross-skill compositions), and this time
  surfaced a more consequential gap in a shared resolution pattern (L24),
  not just a gap in the composed data itself (L22) or a displayed-field-only
  gap (L23). None upgrades its assumption's status beyond UNKNOWN — the
  missing ingredient in every case is the same: a real second party this
  session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5), L18 (Phase 6, scope boundary), L21 (Phase 7,
  keyword-collision-at-scale), L22 (Phase 8, fan_in undercounting), L23
  (Phase 9, substring-collision caller identification) remain deliberately
  deferred — revisit only if real usage shows they matter. L24 (Phase 10)
  is deferred for the same reason but flagged, above, as the strongest
  candidate yet to revisit soon.
- No real (non-agent) engineer has used any of the fifteen skills yet —
  Trust Status stays EXPERIMENTAL on all fifteen, and assumptions
  A2/A3/A5/A7/A8/A10 in [[16-assumptions-and-validation]] remain only
  partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[operating-charter]] — the source document everything else in this
   memory bank distills (only needed for deep context; skip on a quick
   resume)
3. [[implementation-status.md]]
4. [[07-current-state]]
5. `README.md` (root) — primary public-facing entry point
6. `skills/engineering-memory/SKILL.md`,
   `skills/workflow-composer/SKILL.md`,
   `skills/context-optimizer/SKILL.md`,
   `skills/engineering-knowledge-capture/SKILL.md`,
   `skills/dependency-supply-chain/SKILL.md`,
   `skills/release-readiness/SKILL.md`,
   `skills/regression-hunter/SKILL.md`,
   `skills/refactoring-safety/SKILL.md`,
   `skills/architecture-decision/SKILL.md`,
   `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
7. `examples/engineering-memory/example-run.md` (real, non-fixture
   retrieval run against this project's own actual memory bank, surfaced
   the new L31 basename-collision-of-distinct-files finding),
   `examples/workflow-composer/example-run.md` (real, non-dry-run
   composed execution, surfaced the new L30 cross-skill keyword-flooding
   finding), `examples/context-optimizer/example-run.md` (real dogfood,
   surfaced the new L29 full-repository-scale keyword-flooding gap),
   `examples/engineering-knowledge-capture/example-run.md` (real dogfood,
   surfaced the new L28 line-vs-paragraph resolution gap),
   `examples/dependency-supply-chain/example-run.md` (real dogfood, confirms
   the inherited L2 scope gap concretely) and `examples/release-readiness/
   example-run.md` (the real diff run that disclosed L24)
8. [[17-experiment-viability-check.md]]
9. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with Phase 6-11 posts)

## Last updated

2026-09-06 — CI gap fix ([[11-decisions|ADR-032]]): at the user's explicit
follow-up request, [[12-known-limitations|L37]] (no CI job for
`test_strategy`, `scenario_planner`, `test_generation`, `test_validation`)
is now fixed, not just disclosed — four new jobs added to
`.github/workflows/tests.yml`, mirroring the existing `evidence`/
`project-intelligence` job shape (`test_validation`'s job installs with
`pip install -e .`, no `[dev]` extra, since ADR-030 moved `pytest` to its
real runtime dependencies). Verified locally before committing.

2026-09-06 — Public-documentation completion pass ([[11-decisions|ADR-031]]):
the TEP pipeline (built across TEP Phases 1–5d) is now visible in the root
`README.md`, `QuickStarterGuide.md`, and `DEPENDENCIES.md`, which previously
did not mention it at all. Added [[25-tep-pipeline-overview]] (the first
whole-pipeline diagram), [[12-known-limitations|L37]] (CI gap for 4 of 6 TEP
packages), an L2/L34/L35/L36 cross-reference note, and an ADR-023 status
clarification. Five new blog posts (`blogs/07`–`11`) extend the existing
series with TEP-specific content. No code changed; all cited numbers
re-measured directly this session. See "What the public-documentation pass
built" above.

2026-09-06 — TEP Phase 5d's Security/Production Hardening sub-initiative
for the "Project-Aware Test Engineering Platform" pivot
([[11-decisions|ADR-030]]), at the user's explicit direction toward a
"scalable and production level stable system," narrowed via
`AskUserQuestion` to security/production hardening specifically (not
DX/orchestration, distribution, or eval/ablation). An Explore-agent audit
(file:line level) grounded five changes to existing files — no new
package: path containment against symlink/traversal escapes in
`test_validation/generated_tests_loader.py` and `evidence/skill_info.py`;
bounded (disk-backed, not in-memory) subprocess stdout/stderr capture in
`validation_runner.py`; file-count/file-size resource caps in
`report_builder.py`/`cli.py`; wrong-type-container rejection in five JSON
loaders across `test_strategy`, `test_validation`, `scenario_planner`,
`project_intelligence`, and `test_generation`; and `pytest` declared as a
real runtime dependency of `test_validation`. No sandboxing claim added —
ADR-029's disclosure stands unchanged. 20 new regression tests (166
passed, 3 skipped — Windows symlink-creation permission, not a failure);
the real `test_validation` demo was re-run post-hardening with the same
clean result. See "What TEP Phase 5d built" above.

2026-09-06 — TEP Phase 5c's Test Generation & Independent Validation
sub-initiative for the "Project-Aware Test Engineering Platform" pivot
([[11-decisions|ADR-029]]), at the user's explicit direction following TEP
Phase 5b, and the user's explicit choice to pair Test Generation with
Independent Validation as one phase (asked directly, after the user
questioned what Test Generation alone would even produce). Built two new
packages: `test_generation/`, which never authors test code itself — it
produces a plan (real source excerpt, naming convention, 1 positive + 4
negative slot requests) for an agent to author from — and `test_validation/`,
which executes those agent-authored files via subprocess with a strict
timeout, this platform's first execution capability, with no filesystem/
network sandboxing beyond that timeout explicitly disclosed. Demonstrated
twice: an honest zero-result run inheriting TEP Phase 5b's own
[[12-known-limitations|L36]] chain, and a real positive run against an
actual symbol in this repo that produced a real agent-authored test file,
actually executed, that actually passed — which itself found and fixed two
real bugs (a relative-path resolution error, an unfiltered `.pytest_cache`
artifact) that the unit tests written before it did not catch. See
[[23-generation-plan-report-schema]], [[24-validation-report-schema]], and
"What TEP Phase 5c built" above. No existing skill's code changed;
separate from, and does not reopen, the closed 15-skill portfolio below.
TEP Phase 5d and beyond not started — requires its own explicit approval.

2026-09-06 — TEP Phase 5b's Scenario Planner sub-initiative for the
"Project-Aware Test Engineering Platform" pivot ([[11-decisions|ADR-028]]),
at the user's explicit direction following TEP Phase 5a, and the user's
explicit choice of Scenario Planner among ten remaining unscoped TEP Phase
5b sub-initiatives. Built a new `scenario_planner/` package that composes
a real `test_strategy` report's flagged targets with the real
`regression-hunter` flags and `codebase-intelligence` structural listing
they came from, proposing candidate test scenarios — computing no new risk
score and no line-level diff attribution, per the contract's mandate.
Demonstrated by reusing TEP Phase 5a's own real, committed dogfood inputs.
The honest real result — zero plans — is an inherited instance of TEP Phase
5a's own [[12-known-limitations|L36]] finding, surfacing one level further
downstream by design; no new limitation entry was needed. See
[[22-scenario-plan-report-schema]] and "What TEP Phase 5b built" above. No
existing skill's code changed; separate from, and does not reopen, the
closed 15-skill portfolio below. TEP Phase 5c and beyond not started —
requires its own explicit approval.

2026-09-06 — TEP Phase 5a (Test Strategy Engine) for the "Project-Aware
Test Engineering Platform" pivot ([[11-decisions|ADR-027]]), at the user's
explicit direction following TEP Phase 4, and the user's explicit choice of
Test Strategy Engine among eleven unscoped TEP Phase 5 sub-initiatives.
Built a new `test_strategy/` package that combines a real
`regression-hunter` report (per-file risk tier + test coverage) with a real
`project_intelligence` TestEnvironmentProfile (test-framework availability)
to decide which changed files need a test — computing no new risk score of
its own, per the contract's mandate. Demonstrated on a real diff (the
historical addition of `evidence/cli.py`, still genuinely untested today)
against a freshly-generated, full-repository `codebase-intelligence`
report. The honest real result — zero targets flagged — surfaced a new,
real, documented finding: reusing regression-hunter's test-coverage signal
also means inheriting its already-disclosed cross-skill identical-stem
false-positive gap (L24), now logged as its own instance,
[[12-known-limitations|L36]]. See [[21-test-strategy-report-schema]] and
"What TEP Phase 5a built" above. No existing skill's code changed;
separate from, and does not reopen, the closed 15-skill portfolio below.
TEP Phase 5b and beyond not started — requires its own explicit approval.

2026-09-06 — TEP Phase 4 (Test Environment Discovery, Android/JVM
specifically) for the "Project-Aware Test Engineering Platform" pivot
([[11-decisions|ADR-026]]), at the user's explicit direction following TEP
Phase 3. Extended `project_intelligence/` with Android JUnit/Robolectric/
Espresso detection (`android_test_frameworks`, `android_frameworks_absent`
fields), demonstrated on a real run against a real Android repo
(`android/architecture-samples`, `views` branch). The honest real result —
"unavailable" for all three despite genuine source declarations — surfaced
a new, real, documented finding: Android/Gradle repos almost universally
version dependencies via variable interpolation, which the existing Gradle
parser (L33) can't resolve, now logged as [[12-known-limitations|L35]]. See
[[20-test-environment-profile-schema]] and "What TEP Phase 4 built" above.
No existing skill's code changed; separate from, and does not reopen, the
closed 15-skill portfolio below. TEP Phase 5 and beyond not started —
requires its own explicit approval.

2026-09-06 — TEP Phase 3 (Project Intelligence extensions) for the
"Project-Aware Test Engineering Platform" pivot ([[11-decisions|ADR-025]]),
at the user's explicit direction following TEP Phase 2. New
`project_intelligence/` package deriving a `TestEnvironmentProfile` from an
existing `codebase-intelligence` report, demonstrated on a real run
against `skills/codebase-intelligence` itself. Also fixed a packaging
defect shared with `evidence/` (flat module layout broke a clean
`pip install -e`). See [[20-test-environment-profile-schema]] and "What TEP
Phase 3 built" above. No existing skill's code changed; separate from, and
does not reopen, the closed 15-skill portfolio below. TEP Phase 4 not
started — requires its own explicit approval.

2026-09-06 — TEP Phase 2 (Evidence Foundation) for the "Project-Aware Test
Engineering Platform" pivot ([[11-decisions|ADR-024]]), at the user's
explicit direction following TEP Phase 1. New `evidence/` package
implementing the run-provenance schema, demonstrated on a real run of
`codebase-intelligence` against this repo. See
[[19-evidence-provenance-schema]] and "What TEP Phase 2 built" above. No
existing skill's code changed; separate from, and does not reopen, the
closed 15-skill portfolio below. TEP Phase 3 not started — requires its
own explicit approval.

2026-09-06 — TEP Phase 1 (Product Contract) for the newly-proposed
"Project-Aware Test Engineering Platform" pivot ([[11-decisions|ADR-023]]),
at the user's explicit direction following TEP Phase 0. See
[[18-test-engineering-platform-contract]] and "What TEP Phase 1 built"
above. No code, tests, or existing skill changed; separate from, and does
not reopen, the closed 15-skill portfolio below.

2026-08-29 — ADR-022: Java/Kotlin multi-language support, added at the
user's explicit direction after they asked whether the 15-skill portfolio
works on Java/Kotlin repos. A read-only audit confirmed it largely did
not (Kotlin had zero support anywhere in the codebase; Java got import
extraction but zero graph edges, zero entry points, zero manifest
parsing). This is **user-directed, cross-cutting scope — NOT a new
roadmap phase**: the originally-scoped 15-skill portfolio was already
completed by Phase 15 below, and there is still no Phase 16 in
[[08-roadmap]]'s list. Touched `codebase-intelligence` (new
`jvm_parser.py`; `graph.py` gains a package-declaration FQN index
resolver for Java/Kotlin, deliberately not directory-convention guessing;
`external_deps.py` parses Maven `pom.xml`/Gradle `build.gradle[.kts]`)
and 5 downstream skills (`dependency-supply-chain`'s `pin_checker.py`
gains ecosystem-aware classification; `adversarial-diff-reviewer`'s/
`release-readiness`'s pattern tables gain additive JVM entries;
`refactoring-safety`'s/`regression-hunter`'s/`release-readiness`'s
`test_coverage_scanner.py` copies and `regression-hunter`'s own
`is_test_shaped_path` recognize the JVM `*Test`/`*Tests`/`*Spec` suffix
convention). 40 new tests (693 → 733); the other 9 skills' counts are
unchanged, confirmed via a full platform re-run. A real dogfood run
against a synthetic Java+Kotlin+Gradle project (not just unit fixtures)
confirmed the full scan→parse→graph→entry-point→manifest pipeline end to
end. Two new disclosed limitations: L32 (the regex type-extraction
doesn't track brace depth, so a nested/inner type can collide with a
top-level one in the new FQN index) and L33 (Maven/Gradle parsing scope
boundary — no version catalogs, map-notation, property interpolation, or
multi-module coordination). See [[11-decisions]] ADR-022 and
[[12-known-limitations]] L32/L33.

2026-08-26 — Phase 15 (`engineering-memory`) shipped at the user's
explicit direction, a FIFTH one-time reopening of the same-day
mentor-review freeze (after Phase 11 `dependency-supply-chain`, Phase 12
`engineering-knowledge-capture`, Phase 13 `context-optimizer`, and Phase
14 `workflow-composer`) — unlike Phase 14, this one did not override a
named phase-specific decision (A8's own "design only when reached" gate
was satisfied by reaching Phase 15 in order). This completes the
originally-scoped 15-skill portfolio; no Phase 16 exists in
[[08-roadmap]]'s list, and any further skill work is a newly-proposed
scope requiring real external validation evidence first. Test count: 693
(up from 636). Earlier the same day, between Phase 11 and Phase 12: the
operating charter checked in at [[operating-charter]] (documentation
only, no code/roadmap change; see [[12-known-limitations|L27]] for the
disclosed section-numbering gap).
