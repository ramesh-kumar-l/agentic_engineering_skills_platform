# 03 — Architecture

First real architectural content, established in Phase 1
([[08-roadmap]], ADR-005/ADR-006 in [[11-decisions]]), extended in Phase 2
with a second pattern for judgment-based skills (ADR-007/ADR-008), reused
as-is (no new base pattern) in Phase 3 (`acceptance-test-engineer`), reused
a third time in Phase 4 (`feature-planner`) alongside a new architectural
decision making composition mandatory rather than optional, reused a
fourth time in Phase 5 (`security-context-guard`) — see "Pattern 2, reused
for Phase 5" and ADR-011 — reused a fifth time in Phase 6
(`root-cause-analyzer`), which also reuses Phase 4's mandatory-composition
rule a second time and adds a new tiered-evidence-scoring decision (ADR-012)
— see "Pattern 2, reused for Phase 6" — reused a **sixth** time in
Phase 7 (`architecture-decision`), which reuses the mandatory-composition
rule a third time and adds a new per-option blast-radius-tiering decision
(ADR-013) — see "Pattern 2, reused for Phase 7" — reused a **seventh**
time in Phase 8 (`refactoring-safety`), which reuses the mandatory-
composition rule a fourth time and adds a new per-target risk-tier +
independent test-coverage-signal decision (ADR-014) — see "Pattern 2,
reused for Phase 8" — reused an **eighth** time in Phase 9
(`regression-hunter`), which reuses the mandatory-composition rule a fifth
time and adds a new three-axis, non-blended regression-risk-scoring
decision (ADR-015), and reused a **ninth** time in Phase 10
(`release-readiness`), which reuses the mandatory-composition rule a sixth
time and adds a new Release Readiness Scorecard decision (ADR-016), reused
a **tenth** time in Phase 11 (`dependency-supply-chain`), which reuses the
mandatory-composition rule a seventh time and adds two explicit no-live-
CVE/no-license-detection scope decisions plus an advisory/fail-closed
reuse (ADR-017), and reused an **eleventh** time in Phase 12
(`engineering-knowledge-capture`), which reuses the mandatory-composition
rule an eighth time and adds a new decision (ADR-018): its deterministic
layer is the first in this portfolio to target a *documentation artifact*
(an ADR/known-limitation/lessons-learned candidate) rather than a
code-risk or process-quality judgment — see ADR-018 in [[11-decisions]]
for the full rationale. At eleven consecutive reuses without a new base-pattern ADR,
Pattern 2 is this project's settled default architecture for judgment-based
skills, not a fresh per-skill choice each time — worth stating plainly
rather than re-justifying from scratch every phase.

## Pattern: SKILL.md + optional deterministic engine

A skill is not required to be pure LLM reasoning. [[04-skill-contract]]
requires every skill to declare `Tool Permissions` and a `Workflow` — those
fields exist precisely so a skill can wrap a small, deterministic backing tool
instead of asking an agent to re-derive the same analysis via ad hoc
Read/Grep on every invocation.

Use this pattern when:
- The task is deterministic and repeatable (structure extraction, parsing,
  graph-building) — not a task that genuinely requires judgment.
- Doing it via the agent's own tools each time would be slow, expensive, or
  produce inconsistent results across runs (violates NFR2/NFR5 in
  [[02-requirements]]).

Do NOT use this pattern when the task is inherently a judgment call (e.g. "is
this diff safe to merge") — that belongs in the SKILL.md workflow/agent
reasoning, not baked into deterministic code.

## codebase-intelligence: reference implementation of the pattern

```
skills/codebase-intelligence/
  SKILL.md            <- contract: when/how an agent invokes the engine
  engine/              <- deterministic, stdlib-only Python package
    models.py           shared schema (CodebaseIntelligenceReport and friends)
    scanner.py           repo walk, exclusions, secret-file avoidance
    python_parser.py     AST-based import/def/class/docstring/entry-point extraction
    generic_parser.py    heuristic (regex) import extraction for JS/TS/Java
    graph.py              internal dependency graph + hotspot ranking
    external_deps.py     requirements.txt / pyproject.toml / package.json parsing
    report.py             orchestrates the above into one report
    render_json.py       full-detail machine-readable output
    render_markdown.py   condensed human/agent-readable output
    cli.py                thin entry point only — no logic of its own
  tests/                unit + integration tests, one file per engine module
```

Each engine module is single-responsibility and under 300 lines (checked
manually at Phase 1 completion — see [[07-current-state]]) so an agent working
on one concern only needs to read the ~100-line file for it, not a monolith.

## Data flow

```
scanner.scan() -> FileInfo[]
    -> python_parser / generic_parser -> ModuleInfo[]
        -> graph.build_graph() -> DependencyGraph
        -> external_deps.parse_external_dependencies() -> ExternalDependency[]
    -> report.build_report() assembles CodebaseIntelligenceReport
        -> render_json.render_json() | render_markdown.render_markdown()
```

`report.py` is the only module that knows this ordering; every other module
is independently unit-testable without it.

## Security-relevant design choices

- `scanner.py` never reads the contents of secret-shaped files (`.env`,
  `*.pem`, `*.key`, `credentials.json`, `secrets.yaml`, SSH keys) — only the
  filename is recorded, as a warning. See [[06-security-model]].
  Verified by `tests/test_scanner.py::test_scan_skips_secret_shaped_files_without_reading_content`
  and `tests/test_integration.py::test_full_pipeline_produces_valid_json_and_markdown`.
- Only structural metadata (imports, names, sizes) is extracted — full file
  contents are never included in engine output, by construction (no module
  ever stores raw source text on a returned object).

## Evaluation harness architecture (first real instance)

```
evaluations/codebase-intelligence/
  fixtures/       synthetic mini-repos, one per test scenario
  expected/       hand-authored ground truth (structural summary, not full dump)
  eval_cases/     Input/Context/Expected Behavior/Acceptance Criteria docs
  run_evaluation.py   runs the engine against every fixture, diffs vs expected,
                       scores Correctness/Completeness/Efficiency automatically;
                       leaves Safety/Relevance/Explainability for human review
  RESULTS.md      actual, honestly-reported scores (regenerated by the script)
```

This is the first concrete instance of the "Skill → Evaluation Dataset →
Agent Runtime → Execution → Scoring → Report" architecture described in
[[05-evaluation-framework]], intentionally scoped to one skill rather than
built as a generic multi-skill harness before there's evidence one is needed.

## Known limitation this architecture doesn't yet address

`external_deps.py` only checks the scan root for manifest files — it does not
walk into subdirectories for nested manifests (a monorepo/multi-package layout
like this platform's own `skills/codebase-intelligence/pyproject.toml`). See
[[12-known-limitations]].

---

## Pattern 2 (Phase 2): deterministic pre-processor + agent-driven adversarial workflow

Established via `adversarial-diff-reviewer` (ADR-007/ADR-008). This is the
counterpart to Pattern 1 above, for skills whose core task is a **judgment
call** rather than structure extraction — Pattern 1 explicitly says not to
bake judgment tasks into deterministic code, so this pattern gives them a
different, still-disciplined shape:

- A small stdlib-only engine parses the input and flags a fixed table of
  **mechanically-detectable patterns** — but only ever as *leads*, never as a
  verdict. It is unit-tested exactly like Pattern 1's engines.
- The actual judgment happens in the `SKILL.md` workflow, performed by the
  invoking agent, reasoning against a fixed checklist (the 10 failure-first
  categories in [[05-evaluation-framework]]) — using the engine's flags as a
  starting point, not a ceiling.

## adversarial-diff-reviewer: reference implementation of Pattern 2

```
skills/adversarial-diff-reviewer/
  SKILL.md            <- contract: Step 1 engine, Steps 2-4 agent reasoning
  engine/              <- deterministic, stdlib-only Python package
    models.py            shared schema (DiffContext, RiskFlag, DiffIntelligenceReport)
    diff_parser.py        unified diff text -> structured hunks/files/line changes
    risk_patterns.py     fixed regex table (secrets, dangerous calls, broad
                          except, SQL injection shapes, debug leftovers)
    risk_scanner.py       applies risk_patterns to added lines; redacts secrets
                          in place (both flag and raw line content)
    stats.py              objective diff stats (files/lines/hunks touched)
    report.py             orchestrates the above into one pre-review packet
    render_json.py / render_markdown.py
    cli.py                thin entry point only
  tests/                unit + integration tests, one file per engine module
```

Same modularity discipline as Pattern 1: every engine module under 300 lines,
single-responsibility, independently testable.

## Security-relevant design choice specific to Pattern 2

A diff reviewer cannot skip secret-shaped content the way `codebase-
intelligence` skips secret-shaped *files* — the diff itself is exactly what
must be reviewed, and a newly-added hardcoded secret is one of the defects
this skill exists to catch. Instead, `risk_scanner.py` redacts the matched
secret span in place (`pattern.regex.sub()`, covering every occurrence per
line, not just the first) in **both** the `RiskFlag` and the underlying
`LineChange.content`, before either reaches JSON/Markdown output. Two real
redaction gaps were found and fixed during this phase's own dogfooding — see
L5/L6 in [[12-known-limitations]] and
`examples/adversarial-diff-reviewer/example-run.md`.

## Evaluation harness architecture — filling in "Agent Runtime" for real

Phase 1's harness never needed to run an agent — it diffed deterministic
engine output against ground truth directly. A judgment-based skill's harness
must score two layers separately:

```
evaluations/adversarial-diff-reviewer/
  fixtures/        8 seeded-defect diffs (+ 1 clean/negative case)
  expected/        hand-authored ground truth: risk_flag_pattern_ids + defects
  actual/          this session's agent's REAL findings from actually
                   performing the SKILL.md workflow against each fixture
                   (not fabricated to match expected — see [[12-known-limitations]] L8)
  eval_cases/      Input/Context/Expected Behavior/Acceptance Criteria docs
  run_evaluation.py   scores the deterministic layer automatically (like Phase 1)
                      AND scores actual/ vs expected/ for Precision/Recall/FP/FN
  RESULTS.md       both layers' scores, explicitly labeled single-rater/self-authored
```

This is the first time the "Skill → Evaluation Dataset → **Agent Runtime** →
Execution → Scoring → Report" pipeline in [[05-evaluation-framework]] actually
runs an agent, rather than only diffing deterministic output. The scoring
script itself remains deterministic and automated (category+file+keyword
match) — what's new is that one of its two inputs (`actual/*.json`) required a
real agent turn to produce, not just code.

---

## Pattern 2, reused for Phase 3: `acceptance-test-engineer`

Phase 3 did not introduce a new base pattern — it reused Pattern 2 exactly
(deterministic anti-pattern flagging + agent-driven derivation against a
fixed checklist), swapping the domain from diff review to requirement
testability. This is itself a small piece of evidence the pattern
generalizes beyond its original use case:

```
skills/acceptance-test-engineer/
  SKILL.md            <- contract: Step 1 engine, Steps 2-4 agent reasoning
  engine/              <- deterministic, stdlib-only Python package
    models.py            shared schema (RequirementContext, TestabilityFlag,
                          AcceptanceTestabilityReport)
    requirement_parser.py   free text -> structured sentences
    patterns.py            fixed regex table: vague terms, weak modal verbs,
                            per-sentence + whole-document absence checks
    testability_scanner.py   applies patterns.py to a RequirementContext
    stats.py                objective requirement stats (sentences, words,
                             vague-term/modal counts, existing-criteria markers)
    report.py               orchestrates the above into one pre-review packet
    render_json.py / render_markdown.py
    cli.py                thin entry point only
  tests/                unit + integration tests, one file per engine module
```

The 10-category coverage checklist this skill's Step 3 uses lives in
[[05-evaluation-framework]] (acceptance-coverage checklist), alongside the
pre-existing failure-first checklist, since both are reusable methodology
artifacts rather than code specific to one skill.

Evaluation harness architecture is identical in shape to Phase 2's (fixtures
+ expected + actual + eval_cases + run_evaluation.py + RESULTS.md), with the
same up-front self-authored/single-rater disclosure — see
`evaluations/acceptance-test-engineer/RESULTS.md` and L8/A5.

New this phase: [[17-experiment-viability-check]] — the first attempt at
using more than one existing skill together (composing `codebase-
intelligence`'s real Phase 1 output into `acceptance-test-engineer`'s input),
run as an explicitly-labeled pilot, not the real Experiment B (ADR-009).

---

## Pattern 2, reused for Phase 4: `feature-planner` — plus mandatory composition (ADR-010)

Phase 4 reused Pattern 2 a third time (deterministic pre-processing +
agent-driven derivation against a fixed checklist), swapping the domain to
turning a task description into a structured plan. The new architectural
element this phase is **not** the judgment-workflow split — that part is
now well-established — it's that `codebase-intelligence`'s report becomes a
**required precondition**, not optional composed context (ADR-010 in
[[11-decisions]]). Every prior skill's composition with `codebase-
intelligence` was optional; this is the first time a missing upstream
report is a hard failure condition.

```
skills/feature-planner/
  SKILL.md            <- contract: Step 1 precondition, Step 2 engine, Steps 3-4 agent reasoning
  engine/              <- deterministic, stdlib-only Python package
    models.py            shared schema (CiReportContext, RelevanceReport,
                          PlanningFlag, FeaturePlanningReport)
    ci_report_loader.py  loads a codebase-intelligence report.json into a
                          LOCAL, independent schema (no cross-package import)
                          — missing/malformed report -> CiReportError, a
                          hard failure per ADR-010
    relevance_scorer.py  keyword-overlap scoring of ci_report modules against
                          the task text, annotated with fan_in/fan_out/hotspot
                          blast-radius signal from the dependency graph
    planning_patterns.py / planning_scanner.py   fixed regex table: vague
                          scope terms, weak goal modals, scope-boundary/
                          verification absence checks (mirrors Phase 3's
                          testability_scanner.py exactly)
    stats.py, report.py, render_json.py / render_markdown.py, cli.py
  tests/                unit + integration tests, one file per engine module
```

`ci_report_loader.py` deliberately does not import `codebase-intelligence`'s
own `engine.models` — it defines its own lightweight dataclasses for the
subset of fields it needs (module path/docstring/functions/classes/imports,
dependency-graph fan_in/fan_out/hotspots) and loads them from the JSON
directly. This keeps `feature-planner` portable on its own (same rationale
as every other engine being stdlib-only) while still consuming a real,
already-computed structural map instead of re-deriving one.

The 10-category Plan Quality checklist this skill's Step 3 uses lives in
[[05-evaluation-framework]], a third checklist alongside the failure-first
and acceptance-coverage ones — all three now share the same category-10
honesty-valve convention.

**Real evidence composition matters, found via dogfooding, not claimed in
the abstract**: `examples/feature-planner/example-run.md` regenerates a
fresh `codebase-intelligence` report against this repo's current (4-skill)
state and runs a real task against it. Two genuine findings came out of
that one real run: (1) the relevance scorer's path-weighting floods when a
task's keywords collide with a shared directory name — the true target file
ranked 13th, not 1st (L13 in [[12-known-limitations]], not fixed, a
documented boundary the agent's Step 3 judgment is specifically designed to
absorb — and did, correctly, in that same run); (2) grounding "affected
files" in the real module list surfaced that `acceptance-test-engineer`'s
own CLI had zero test coverage — the second cross-skill dogfood finding in
this project (after L10), fixed same-session.

Evaluation harness architecture is identical in shape to Phases 2-3
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `task.txt` with a synthetic
`ci_report.json`, so the required-composition precondition is exercised on
every fixture, not just the real dogfood run — see
`evaluations/feature-planner/RESULTS.md` and L8/A5 (now applying a third
time).

---

## Pattern 2, reused for Phase 5: `security-context-guard` — plus ADR-011

Phase 5 reused Pattern 2 a **fourth** time (deterministic pre-processing +
agent-driven derivation against a fixed checklist), swapping the domain to
classifying content/actions for security purposes. The new architectural
element this phase is that the deterministic engine's output
(`suggested_verdict`) must never be treated as a final decision — Pattern 2
has always kept judgment in the agent's workflow, but this is the first
skill where the *thing being judged* is itself an authorization decision,
so the "leads, not verdicts" discipline gets an explicit, stronger
statement: the engine classifies and recommends, it never authorizes
(ADR-011 in [[11-decisions]]), per [[06-security-model]]'s Human Approval
principle.

```
skills/security-context-guard/
  SKILL.md            <- contract: Step 1 gather inputs, Step 2 engine, Steps 3-4 agent reasoning
  engine/              <- deterministic, stdlib-only Python package
    models.py            shared schema (SecretMatch, PiiMatch, SensitivePathMatch,
                          ActionFlag, Classification, SecurityGuardReport) — no
                          field anywhere on this schema ever holds a raw
                          secret/PII value
    secret_patterns.py / pii_patterns.py   fixed regex tables (leads, not
                          verdicts), every match redacted before output
    sensitive_paths.py   filename/path convention table (.env, *.pem, id_rsa*, ...)
    action_patterns.py   keyword table for the six high-risk action categories
                          named in project-memory-bank/06-security-model.md;
                          verb+object categories matched by SAME-SENTENCE
                          co-occurrence, not a fixed character-distance window
                          (see L16 in [[12-known-limitations]] for why)
    scanner.py            orchestrates matching + redaction
    classification.py     deterministic sensitivity/suggested_verdict rollup —
                          fails closed (REQUIRES_HUMAN_APPROVAL) on inconclusive input
    stats.py, report.py, render_json.py / render_markdown.py, cli.py
  tests/                unit + integration tests, one file per engine module,
                        including a CLI test file written from the start
                        (not discovered missing via a later dogfood run, unlike
                        L10/L13)
```

Unlike `feature-planner`'s ADR-010, composition with `codebase-intelligence`
stays **optional** here — `--ci-report` only adds a hotspot-touch note, and
a missing/unreadable report is a warning, never a failure. This skill is a
general-purpose classify/sanitize/authorize gate, useful standalone; ADR-010's
own Future Evolution clause says mandatory composition is adopted only when
ungrounded output is actively harmful, which doesn't apply to a
classify/redact/flag skill the way it did to affected-files grounding.

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/security-context-guard/example-run.md` runs the engine against
this phase's own real source file and a real pending decision this session
actually faced ("commit and push these Phase 5 files to the shared origin
repository"). The first run missed the action entirely — the `publishing`
pattern's fixed-width proximity window (`push ... .{0,N} ... origin`)
couldn't span the 150+ character parenthetical file list real phrasing put
between the verb and its target, no matter how far the window was widened.
The real fix replaced the fixed window with same-sentence co-occurrence
matching (`ActionPattern.matches()` in `action_patterns.py`) — a
better-justified design, not a bigger magic number. Logged as **L16** in
[[12-known-limitations]], fixed same-session (the third "real dogfood run on
real phrasing found a gap" finding, after L1 and L13, but the first one
found in the very skill being dogfooded rather than a different one).

This dogfood run doubles as **Pilot C**, the first internal pilot toward
[[16-assumptions-and-validation]] A7 — see [[17-experiment-viability-check]].

The 7-category Security Decision Checklist this skill's Step 3 uses lives in
[[05-evaluation-framework]], a **fourth** checklist alongside the
failure-first, acceptance-coverage, and Plan Quality ones — but shaped
differently: a decision-gate/verdict workflow, not a coverage-enumeration
list, since this skill's job is deciding whether to proceed, not
enumerating coverage. Its honesty-valve category (7) is adapted accordingly:
fail closed under uncertainty, rather than "state the assumption."

Evaluation harness architecture is identical in shape to Phases 2-4
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md) — see `evaluations/security-context-guard/RESULTS.md` and
L8/A5 (now applying a fourth time).

---

## Pattern 2, reused for Phase 6: `root-cause-analyzer` — plus ADR-012 (tiered evidence) and ADR-010 reused

Phase 6 reused Pattern 2 a **fifth** time (deterministic pre-processing +
agent-driven derivation against a fixed checklist), swapping the domain to
diagnosing why a failure happened. Two architectural elements carry over
from prior phases rather than being invented fresh: `feature-planner`'s
mandatory-composition rule (ADR-010) applies here too — a missing/malformed
`codebase-intelligence` report is a hard failure, not a degraded path — and
this is stated explicitly as a **reuse**, not a new decision on that point
(see ADR-012 in [[11-decisions]]). What is new this phase: candidate
locations are scored in two explicit, non-blended **evidence tiers**, not a
single blended score.

```
skills/root-cause-analyzer/
  SKILL.md            <- contract: Step 1 precondition, Step 2 engine, Steps 3-4 agent reasoning
  engine/              <- deterministic, stdlib-only Python package
    models.py            shared schema (CiReportContext, StackFrame,
                          SymptomFlag, CandidateLocation, CandidateReport,
                          RootCauseReport)
    ci_report_loader.py  same required-precondition pattern as
                          feature-planner's loader (ADR-010, reused, own
                          independent copy — no cross-package import)
    stack_trace_parser.py   extracts stack-trace-shaped frames from the
                          symptom text: Python tracebacks
                          (`File "path", line N, in symbol`) and a generic
                          `path:line` shape
    candidate_scorer.py   scores ci_report modules against the symptom in
                          two tiers — a dominant flat bonus for a
                          stack-trace path match (evidence_tier=
                          "stack-trace"), reusing relevance_scorer.py's
                          keyword-overlap weighting as the fallback tier
                          (evidence_tier="keyword") — see ADR-012
    symptom_patterns.py / symptom_scanner.py   fixed regex table: vague
                          symptom language, missing expected/actual,
                          missing repro, missing error signal (mirrors
                          Phase 4's planning_patterns.py/planning_scanner.py)
    stats.py, report.py, render_json.py / render_markdown.py, cli.py
  tests/                unit + integration + CLI tests, one file per engine
                        module, CLI test file written from the start (same
                        discipline Phase 5 established, not discovered
                        missing via a later dogfood run — see L10/L13)
```

`candidate_scorer.py` deliberately keeps `evidence_tier` as its own field on
`CandidateLocation`, separate from the numeric `score` — so the agent's
Step 3 investigation can always tell "the traceback literally names this
file" apart from "this file happens to share vocabulary with the bug
report," even after both are sorted into one ranked list.

The 10-category Root Cause Investigation checklist this skill's Step 3 uses
lives in [[05-evaluation-framework]], a **fifth** checklist alongside the
failure-first, acceptance-coverage, Plan Quality, and Security Decision
ones — shaped like the coverage-enumeration checklists (not the
decision-gate shape), since this skill's job is enumerating what a complete
investigation covers, not issuing a binary verdict. Its honesty-valve
category (10) follows the same "state the assumption" convention as the
other three coverage-shaped checklists.

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/root-cause-analyzer/example-run.md` regenerates a fresh
`codebase-intelligence` report against this repo's current (6-skill) state
and runs a real, retrospective symptom against it — a natural-language bug
report describing Phase 5's own L16 defect, written without naming the file
or the fix. The candidate scorer — using keyword-tier evidence only, since
this was a silent misclassification with no stack trace to parse — ranked
`action_patterns.py` (the file that actually contained L16's bug) first out
of 122 scored modules. This is explicitly disclosed as a *retrospective
validation*, not a new bug find (L16 was already fixed in Phase 5) — the
real, still-open test is whether this ranks a **genuinely new, not-yet-
diagnosed** symptom's true root cause well, which this project has not yet
observed.

Evaluation harness architecture is identical in shape to Phases 2-5
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `symptom.txt` with a
synthetic `ci_report.json` — see `evaluations/root-cause-analyzer/
RESULTS.md` and L8/A5 (now applying a fifth time, and the first of the
five where the judgment layer did not score perfectly on every fixture —
see L19 in [[12-known-limitations]]).

## Pattern 2, reused for Phase 7: `architecture-decision` — plus ADR-013 (per-option blast-radius tiering) and ADR-010 reused a third time

`architecture-decision` (Phase 7) is the **sixth** consecutive skill to
reuse Pattern 2 without a new base-pattern ADR: `engine/` is a stdlib-only
deterministic pre-processor (option parsing, decision-quality anti-pattern
flags, per-option blast-radius scoring), and `SKILL.md`'s Step 3 is the
agent-driven judgment layer that actually weighs the decision against a
fixed checklist. It also reuses `feature-planner`'s (ADR-010) and
`root-cause-analyzer`'s (ADR-012) required-composition rule a **third**
time — a missing/malformed `codebase-intelligence` `report.json` is a hard
failure for this skill too, via its own independent `ci_report_loader.py`
copy (no cross-package import, same portability discipline as every prior
composing skill).

**What's genuinely new (ADR-013)**: `option_parser.py` splits the decision
text into distinct `DecisionOption`s using three fixed shapes — explicit
`Option A:` markers, a numbered/lettered list, or a `vs`/`versus` fallback
split on a single line — falling back to one unlabeled "proposed" option
if none match, rather than inventing alternatives that were never stated.
`impact_scorer.py` then scores each option against `codebase-intelligence`'s
modules using the same keyword-weighting scheme every prior judgment skill
reuses (path > name > docstring/imports), but rolls the result up into a
**blast-radius tier** using real dependency-graph data:
`hotspot_count > 0 or blast_radius_score >= _HIGH_BLAST_RADIUS` forces
`high`, regardless of the keyword relevance number — a decision option that
touches a real hotspot is never presented with the same confidence as one
that merely shares vocabulary with a module. `blast_radius_tier` is carried
as its own field on `OptionImpact`, the same "don't collapse the
distinction into one blended number" discipline ADR-012 established for
evidence tiering.

```
skills/architecture-decision/
  engine/
    models.py               (CiModule/CiReportContext copy, DecisionOption,
                              DecisionFlag, DecisionStats, ImpactedModule,
                              OptionImpact, ArchitectureDecisionReport)
    ci_report_loader.py     (own copy, required precondition — ADR-010/013)
    option_parser.py        (3 shapes: markers, list items, vs-split)
    decision_patterns.py / decision_scanner.py
                             (vague-decision-language + 4 absence checks:
                              alternatives, reversibility, tradeoff, security)
    impact_scorer.py        (keyword relevance -> blast-radius tier, ADR-013)
    stats.py, report.py, render_json.py, render_markdown.py, cli.py
  tests/  (34 tests, CLI test file written from the start, same
            discipline Phase 5 established, not discovered missing via a
            later dogfood run — see L10/L13)
```

The 10-category Architecture Decision Record checklist this skill's Step 3
uses lives in [[05-evaluation-framework]], a **sixth** checklist alongside
the failure-first, acceptance-coverage, Plan Quality, Security Decision,
and Root Cause Investigation ones — coverage-shaped like the other four
enumeration checklists. Its category 6 (blast radius grounded in real
data) is specific to this skill: distinguishing "the engine found nothing
because the option is genuinely low-impact" from "the engine found nothing
because the decision text never named a real target" is what stops an
ungrounded option from being read as a safe one (see evaluation case-04's
Option B, a real high-risk option that scored zero matched modules because
its target went unnamed).

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/architecture-decision/example-run.md` regenerates a fresh
`codebase-intelligence` report against this repo's current (7-skill, 143-
module) state and runs a real, in-flight decision through it — whether
`architecture-decision` itself should require or merely accept
`codebase-intelligence` composition (the exact ADR-013 choice this phase
made). The run found and fixed a real gap same-session: the tradeoff
absence-pattern regex matched only the noun form ("tradeoff"/"trade-off"),
not the verb phrasing ("trades X for Y") the decision text used twice — see
L20 in [[12-known-limitations]]. It also surfaced, and deliberately did
**not** fix, a sharper version of `feature-planner`'s (L14) and
`root-cause-analyzer`'s (L19) coincidental-substring limitation: at full-
repository scale, a decision *about the platform's own architecture*
necessarily reuses this project's own recurring vocabulary, so both options'
blast-radius scores inflated to 240+ and touched all 10 of the report's
hotspots — a real but not useful signal (see L21).

Evaluation harness architecture is identical in shape to Phases 2-6
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `decision.txt` with a
synthetic `ci_report.json` — see `evaluations/architecture-decision/
RESULTS.md` and L8/A5 (now applying a sixth time; unlike Phase 6, all 8
fixtures scored perfect precision/recall on the judgment layer, stated
plainly as not evidence of higher judgment quality than Phase 6's score,
since a single self-authored evaluation cannot support that comparison).

## Pattern 2, reused for Phase 8: `refactoring-safety` — plus ADR-014 (per-target risk tier + independent test-coverage signal) and ADR-010 reused a fourth time

`refactoring-safety` (Phase 8) is the **seventh** consecutive skill to
reuse Pattern 2 without a new base-pattern ADR: `engine/` is a stdlib-only
deterministic pre-processor (operation/target parsing, target resolution,
test-coverage scanning, safety-quality anti-pattern flags, per-target risk
scoring), and `SKILL.md`'s Step 3 is the agent-driven judgment layer that
actually decides whether the refactor is safe to proceed against a fixed
checklist. It also reuses `feature-planner`'s (ADR-010), `root-cause-
analyzer`'s (ADR-012), and `architecture-decision`'s (ADR-013) required-
composition rule a **fourth** time — a missing/malformed `codebase-
intelligence` `report.json` is a hard failure for this skill too, via its
own independent `ci_report_loader.py` copy (no cross-package import, same
portability discipline as every prior composing skill).

**What's genuinely new (ADR-014)**: `operation_parser.py` detects one of 8
fixed operation types (rename/delete/move/change-signature/split/merge/
extract/inline, falling back to generic "refactor") and extracts target
identifiers — quoted/backticked names first, a bare-identifier fallback
second (requiring an underscore, dotted extension, or internal capital, so
it doesn't misfire on ordinary sentence-initial capitalized words).
`target_resolver.py` resolves each target against `codebase-intelligence`'s
modules (stem, function-name, or class-name match) and finds its real
callers via an independent substring scan of every module's raw `imports`
list — deliberately not trusting `codebase-intelligence`'s own `fan_in`
field for caller *identity*, only for the risk-tier calculation (see L22
below for why that distinction turned out to matter).
`test_coverage_scanner.py` independently checks whether any test-shaped
module (`tests/` dir, or `test_*`/`*_test` filename) imports the target.
`safety_scorer.py` then rolls operation type (boundary-changing vs.
internal-only) and fan-in/hotspot data into a `risk_tier`
(`low`/`medium`/`high`), and — the actually new architectural move —
raises a **distinct** `untested-blast-radius` flag when the tier is
medium/high and no covering test module was found, rather than blending
structural risk and verification status into one number. `risk_tier` and
`test_coverage_modules` stay separate fields on `TargetAssessment`, the
same "don't collapse the distinction into one blended number" discipline
ADR-012 and ADR-013 already established for their own tiering decisions.

```
skills/refactoring-safety/
  engine/
    models.py                (CiModule/CiReportContext copy, RefactorTarget,
                               SafetyFlag, RefactorStats, CallerModule,
                               TargetAssessment, RefactoringSafetyReport)
    ci_report_loader.py      (own copy, required precondition — ADR-010/014)
    operation_parser.py      (8 fixed op types, quoted/backtick + bare
                               identifier fallback target extraction)
    target_resolver.py       (module-stem/function/class resolution, real
                               caller lookup via independent import scan)
    test_coverage_scanner.py (independent static test-coverage heuristic)
    safety_scorer.py         (risk tier from op type + fan-in/hotspot,
                               distinct untested-blast-radius flag — ADR-014)
    safety_patterns.py / safety_scanner.py
                              (vague-refactor-language + 4 absence checks:
                               test plan, rollback, caller update, verification)
    stats.py, report.py, render_json.py, render_markdown.py, cli.py
  tests/  (62 tests, CLI test file written from the start, same discipline
            Phases 5-7 established, not discovered missing via a later
            dogfood run — see L10/L13)
```

The 10-category Refactoring Safety checklist this skill's Step 3 uses lives
in [[05-evaluation-framework]], a **seventh** checklist alongside the
failure-first, acceptance-coverage, Plan Quality, Security Decision, Root
Cause Investigation, and Architecture Decision Record ones —
coverage-shaped like the five other enumeration checklists. Its category 4
(test coverage distinguished from text-level silence) is specific to this
skill: a refactor description that never mentions tests is not the same
claim as a target that has no real test coverage — these are independent
signals, and evaluation case-03 deliberately makes them diverge (the text
never says "test," but the target genuinely has a real covering test
module) to test that the checklist walk keeps them distinct.

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/refactoring-safety/example-run.md` regenerates a fresh
`codebase-intelligence` report against this repo's current (8-skill) state
and runs a real refactor through it — extracting a path-stem helper
duplicated across this skill's own `target_resolver.py` and
`test_coverage_scanner.py`, a genuine artifact of this phase's own build,
not an invented example. The run surfaced, and deliberately did **not**
fix, a new category of limitation: `codebase-intelligence`'s own `fan_in`
count for `target_resolver.py` reported 1, but this skill's own
`caller_modules` scan correctly found 2 real callers (`engine/report.py`
via a relative import, and `tests/test_target_resolver.py` via an
absolute-style cross-package import that `codebase-intelligence`'s
dependency-graph builder did not recognize as an edge) — see L22 in
[[12-known-limitations]]. Unlike Phase 7's L20 (a bug in this skill's own
regex) or L21 (a scaling limitation in this skill's own scorer), L22
originates in the *composed upstream data itself*, a distinct and useful
category of dogfood finding this project had not produced before.

Evaluation harness architecture is identical in shape to Phases 2-7
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `refactor.txt` with a
synthetic `ci_report.json` — see `evaluations/refactoring-safety/
RESULTS.md` and L8/A5 (now applying a seventh time; all 8 fixtures scored
perfect precision/recall on the judgment layer, stated plainly as not
evidence of higher judgment quality than Phase 6's score, since a single
self-authored evaluation cannot support that comparison).

## Pattern 2, reused for Phase 9: `regression-hunter` — plus ADR-015 (three-axis, non-blended regression-risk scoring) and ADR-010 reused a fifth time

`regression-hunter` (Phase 9) is the **eighth** consecutive skill to reuse
Pattern 2 without a new base-pattern ADR: `engine/` is a stdlib-only
deterministic pre-processor (diff parsing, target resolution, test-coverage
scanning, diff-pattern regression flagging, three-axis risk scoring), and
`SKILL.md`'s Step 3 is the agent-driven judgment layer that actually
decides what existing behavior is genuinely at risk against a fixed
checklist. It also reuses `feature-planner`'s (ADR-010), `root-cause-
analyzer`'s (ADR-012), `architecture-decision`'s (ADR-013), and
`refactoring-safety`'s (ADR-014) required-composition rule a **fifth**
time — a missing/malformed `codebase-intelligence` `report.json` is a hard
failure for this skill too, via its own independent `ci_report_loader.py`
copy (no cross-package import, same portability discipline as every prior
composing skill).

**What's genuinely new (ADR-015)**: unlike every prior composing
judgment-based skill, this skill's primary input is a **git diff**, not a
free-text description — `diff_parser.py` is an independent copy of
`adversarial-diff-reviewer`'s unified-diff parsing conventions, adapted to
this skill's own `ChangedFile`/`Hunk`/`LineChange` models.
`regression_patterns.py`/`regression_scanner.py` scan the diff's own hunks
directly for five mechanically-detectable shapes (removed exception
handling, a removed conditional guard with no replacement, a large
unreplaced deletion, decreased test assertions in a changed test file, a
modified function signature with no corresponding test-file change in the
same diff) — this is the genuinely new deterministic-layer contribution
this phase, since no prior skill scans a diff's hunks for regression shapes
(`adversarial-diff-reviewer`'s `risk_scanner.py` scans *added* lines for
new defects; this skill scans *removed and modified* lines for existing
behavior at risk). `target_resolver.py` and `test_coverage_scanner.py`
reuse `refactoring-safety`'s resolution and coverage patterns as
independent copies, adapted to resolve a diff's changed-file paths instead
of free-text-parsed identifiers. `risk_scorer.py` then combines all three
axes — diff-pattern flags, structural tier, test coverage — into one
`overall_risk_tier` per file via a documented, explicit rule table, while
keeping all three fields visible and separately inspectable on
`FileRiskAssessment`, the same "don't collapse the distinction into one
blended number" discipline ADR-012/013/014 already established for their
own tiering decisions — extended here to three axes instead of two.

```
skills/regression-hunter/
  engine/
    models.py                (CiModule/CiReportContext copy, ChangedFile/
                               Hunk/LineChange, RegressionFlag,
                               StructuralAssessment, TestCoverageStatus,
                               FileRiskAssessment, RegressionHunterReport)
    ci_report_loader.py      (own copy, required precondition — ADR-010/015)
    diff_parser.py           (independent copy of adversarial-diff-
                               reviewer's unified-diff parsing conventions)
    target_resolver.py       (exact-path + module-stem resolution against
                               the composed report, real caller lookup via
                               import scan — same pattern as refactoring-
                               safety's, same L23 substring-collision gap)
    test_coverage_scanner.py (independent static test-coverage heuristic,
                               same pattern as refactoring-safety's)
    regression_patterns.py / regression_scanner.py
                              (5 diff-pattern checks scanned against the
                               diff's own hunks — the new Axis 1)
    risk_scorer.py           (combines Axis 1/2/3 into overall_risk_tier
                               via a documented rule table — ADR-015)
    stats.py, report.py, render_json.py, render_markdown.py, cli.py
  tests/  (64 tests, CLI test file written from the start, same discipline
            Phases 5-8 established, not discovered missing via a later
            dogfood run — see L10/L13)
```

The 10-category Regression Risk checklist this skill's Step 3 uses lives in
[[05-evaluation-framework]], an **eighth** checklist alongside the
failure-first, acceptance-coverage, Plan Quality, Security Decision, Root
Cause Investigation, Architecture Decision Record, and Refactoring Safety
ones — coverage-shaped like six of the seven other enumeration checklists.
Its category 5 (overall risk tier explained via the documented rule table,
not asserted) is specific to this skill's three-axis design: the checklist
walk should be able to explain *why* a file landed at a given tier from the
three underlying fields, not just repeat the tier as an assertion, the same
way category 4 in `refactoring-safety`'s checklist distinguishes text-level
silence from structural fact.

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/regression-hunter/example-run.md` regenerates a fresh
`codebase-intelligence` report against this repo's current (9-skill) state
and runs a real `git diff` through it — a genuine, already-tested
`codebase-intelligence` scanner fix this phase's own build produced
(excluding `*.egg-info` directories from repo scans, with a new test,
24/24 `codebase-intelligence` tests passing). The run correctly scored both
changed files LOW overall risk (zero diff-pattern flags, no structural
escalation) — the correct, honest outcome for a small, purely additive,
already-tested change. It also surfaced, and deliberately did **not** fix,
a new category of limitation: `target_resolver.py`'s substring-based
caller-identification heuristic — shared, as an independent copy, with
`refactoring-safety`'s identical pattern — inflated `scanner.py`'s caller
list to 22 modules, most of them false positives from other skills' own
`*_scanner.py` modules sharing the substring `"scanner"` (see L23 in
[[12-known-limitations]]). Unlike L22 (a gap in the *composed upstream
data*), L23 is a gap in a *resolution pattern shared across two skills'
independent copies* — a new, more precise category of cross-skill finding
this project had not produced before.

Evaluation harness architecture is identical in shape to Phases 2-8
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `diff.txt` with a synthetic
`ci_report.json` — see `evaluations/regression-hunter/RESULTS.md` and
L8/A5 (now applying an eighth time; all 8 fixtures scored perfect
precision/recall on the judgment layer, stated plainly as not evidence of
higher judgment quality than Phase 6's score, since a single self-authored
evaluation cannot support that comparison).

## Pattern 2, reused for Phase 10: `release-readiness` — plus ADR-016 (the Release Readiness Scorecard) and ADR-010 reused a sixth time

`release-readiness` (Phase 10) is the **ninth** consecutive skill to reuse
Pattern 2 without a new base-pattern ADR, and the final skill in the
Engineering Lifecycle group: `engine/` is a stdlib-only deterministic
pre-processor (diff parsing, diff-hygiene flagging, structural resolution,
test-coverage scanning, optional regression/security evidence loading,
per-file/overall readiness scoring), and `SKILL.md`'s Step 4 is the
agent-driven judgment layer that actually decides what a given release
readiness scorecard means for THIS release, against a fixed checklist. It
also reuses `feature-planner`'s (ADR-010), `root-cause-analyzer`'s
(ADR-012), `architecture-decision`'s (ADR-013), `refactoring-safety`'s
(ADR-014), and `regression-hunter`'s (ADR-015) required-composition rule a
**sixth** time — a missing/malformed `codebase-intelligence` `report.json`
is a hard failure for this skill too, via its own independent
`ci_report_loader.py` copy (no cross-package import, same portability
discipline as every prior composing skill).

**What's genuinely new (ADR-016)**: unlike every prior composing skill,
`release-readiness` is the FIRST to also compose OPTIONALLY with two other
skills' own outputs (`regression-hunter`'s and `security-context-guard`'s
`report.json`), not just `codebase-intelligence`'s. `hygiene_scanner.py`
scans the diff's own hunks for release-blocking anti-patterns (debug
leftovers, TODO-blocking markers, hardcoded-secret-shaped literals, merge-
conflict markers) — Axis 1, a mechanically-detectable-shape table in the
same spirit as `regression-hunter`'s `regression_patterns.py` but scoped to
release-blocking concerns rather than regression-correlated ones.
`target_resolver.py`/`blast_radius_scorer.py` (Axis 2) and
`test_coverage_scanner.py` (Axis 3) reuse `refactoring-safety`'s/
`regression-hunter`'s patterns as a THIRD independent copy.
`regression_report_loader.py`/`security_report_loader.py` load the two
optional reports (Axis 4/5) — missing or malformed input is a warning, not
a failure, reusing `security-context-guard`'s ADR-011 precedent for
optional composition rather than ADR-010's mandatory one. `readiness_
scorer.py` combines ONLY the three always-available axes into a per-file
`readiness_tier` via a documented rule table (any hygiene flag -> blocked;
high structural tier with no coverage -> blocked; medium/high structural
tier or no coverage -> needs-review; otherwise clear), then rolls per-file
tiers into one `overall_verdict`. Axis 4/5 evidence is surfaced as distinct
fields but deliberately NOT blended into the rule table — a design choice,
not an oversight, since each is already a rolled-up verdict from a
DIFFERENT skill's own rule table, and re-blending it here would hide which
skill actually produced which judgment (the same "don't collapse the
distinction away" discipline ADR-012/013/014/015 already established for
their own axes, extended here across skill boundaries rather than within
one skill's own axes).

```
skills/release-readiness/
  engine/
    models.py                (CiModule/CiReportContext copy, ChangedFile/
                               Hunk/LineChange, HygieneFlag, StructuralAssessment,
                               TestCoverageStatus, RegressionEvidence,
                               SecurityEvidence, FileReadinessAssessment,
                               ReleaseReadinessReport)
    ci_report_loader.py      (own copy, required precondition — ADR-010/016)
    diff_parser.py           (independent copy of regression-hunter's/
                               adversarial-diff-reviewer's parsing conventions)
    target_resolver.py       (exact-path + module-stem resolution, real
                               caller lookup via import scan — THIRD
                               independent copy of the L23 substring-
                               matching limitation, now shown to also
                               affect test-coverage matching — see L24)
    test_coverage_scanner.py (independent static test-coverage heuristic,
                               third independent copy of the same pattern)
    blast_radius_scorer.py   (structural tier from fan-in/hotspot data)
    hygiene_patterns.py / hygiene_scanner.py
                              (release-blocking anti-pattern table — debug
                               leftovers, TODO-blocking markers, hardcoded-
                               secret-shaped literals, merge-conflict markers)
    regression_report_loader.py / security_report_loader.py
                              (OPTIONAL composition, ADR-011 precedent —
                               absent evidence, not a failure, on missing/
                               malformed input)
    readiness_scorer.py      (per-file readiness_tier from Axes 1-3 only,
                               overall_verdict rollup — ADR-016)
    stats.py, report.py, render_json.py, render_markdown.py, cli.py
  tests/  (78 tests, CLI test file written from the start, same discipline
            Phases 5-9 established, not discovered missing via a later
            dogfood run — see L10/L13)
```

The 10-category Release Readiness Checklist this skill's Step 4 uses lives
in [[05-evaluation-framework]], a **ninth** checklist alongside the
failure-first, acceptance-coverage, Plan Quality, Security Decision, Root
Cause Investigation, Architecture Decision Record, Refactoring Safety, and
Regression Risk ones — coverage-shaped like seven of the eight other
enumeration checklists, but with an explicit non-negotiable framing
category (verdict is advisory, never an auto-gate) this skill's
higher-stakes recommendation specifically requires.

**Real evidence found via dogfooding, not claimed in the abstract**:
`examples/release-readiness/example-run.md` regenerates a fresh
`codebase-intelligence` report against this repo's current (10-skill)
state and runs a real, staged-then-unstaged (never committed) `git diff` of
this phase's own 78 new files through it. The run confirmed, concretely on
this skill's own real `engine/cli.py` and `run_evaluation.py`, an
already-documented limitation (legitimate CLI `print()` output flagged as a
debug leftover) — left unfixed by design, the same "leads not verdicts"
boundary every prior anti-pattern table has. It also surfaced, and
deliberately did **not** fix, a new, more consequential manifestation of
the L14/L19/L21/L23 substring-collision limitation class: `target_
resolver.py`'s stem-based matching — reused unmodified inside `test_
coverage_scanner.py` — produced **false-positive test coverage**, not just
an inflated caller list, for modules whose stem (`models`, `stats`,
`report`, etc.) collides with an identically-named module in an unrelated
skill (L24 in [[12-known-limitations]]).

Evaluation harness architecture is identical in shape to Phases 2-9
(fixtures + expected + actual + eval_cases + run_evaluation.py +
RESULTS.md), except every fixture now pairs a `diff.txt` with a synthetic
`ci_report.json`, and two fixtures (case-07, case-08) also supply a
synthetic `regression_report.json`/`security_report.json` to exercise the
optional composition path — see `evaluations/release-readiness/
RESULTS.md` and L8/A5 (now applying a ninth time; all 8 fixtures scored
perfect precision/recall on the judgment layer, stated plainly as not
evidence of higher judgment quality than Phase 6's score, since a single
self-authored evaluation cannot support that comparison).
