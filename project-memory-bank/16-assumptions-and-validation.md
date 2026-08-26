# 16 — Assumptions and Validation

Every major product assumption, tracked honestly. Statuses:
`UNKNOWN | VALIDATED | PARTIALLY_VALIDATED | INVALIDATED | REQUIRES_MORE_EVIDENCE`.

All entries below start at `UNKNOWN` — zero real-world usage exists yet
(see [[07-current-state]]). If evidence later contradicts an assumption,
update [[08-roadmap]] rather than forcing reality to fit the plan.

---

### A1: Engineers want reusable agentic skills

- **Why we believe it**: engineers already write ad-hoc prompt templates and
  reuse them informally; a standardized, evaluated version seems like a natural
  next step.
- **Risk**: engineers may prefer ad-hoc prompting because it's lower-friction
  than adopting a contract/workflow.
- **Validation experiment**: Experiment C ([[01-product-thesis]]) — hand a skill
  to an external engineer with no explanation, observe adoption/comprehension.
- **Expected evidence**: engineer completes the task faster/more correctly using
  the skill than without, and would reach for it again unprompted.
- **Actual evidence**: none yet.
- **Status**: UNKNOWN.
- **Decision**: run Experiment C once a Phase 1 skill exists.

### A2: Skills provide measurable benefit over normal prompting

- **Why we believe it**: structure (preconditions, checkpoints, evaluation)
  should reduce rework versus unstructured prompting.
- **Risk**: the overhead of the skill contract could outweigh the benefit for
  simple tasks.
- **Validation experiment**: Experiment A — engineer + normal AI workflow vs.
  engineer + skill on matched real tasks, measuring Time-to-Correct-Result.
- **Expected evidence**: skill-assisted workflow shows lower
  Time-to-Correct-Result and fewer review findings.
- **Actual evidence**: none yet — Experiment A (skill vs. normal prompting on
  matched real tasks) has not been run. Phase 1–3 only prove each skill can
  be built and passes its own synthetic evaluation; neither compares against
  unstructured prompting on real work. Phase 3 attempted a first viability
  check: Experiment A is not runnable rigorously without an independent
  party, so a single-session, N=1, un-blinded internal pilot was run instead
  (Pilot A, [[17-experiment-viability-check]]) — it surfaced one real,
  checkable signal (the skill's category-10 discipline surfaced an
  assumption about `argparse` interaction that direct reasoning likely would
  have skipped) but is explicitly not evidence for or against this
  assumption at the required rigor. 2026-08-26 (mentor-review follow-up): a
  minimal before/after measurement harness now exists —
  `evaluations/usage-comparison/` — the first artifact in this project that
  can actually log real turns/tokens/wall-clock-time for a task run both
  with a skill and with plain prompting. It ships empty, same discipline as
  every other harness here: no numbers are claimed until real runs are
  logged, and the README states plainly this remains a self-run pilot
  (ADR-009), not a rigorous blinded Experiment A.
- **Status**: UNKNOWN — unchanged; a harness existing is not evidence, only
  the capability to eventually produce some. 2026-08-26: Phase 11
  (`dependency-supply-chain`) was started at the user's explicit direction,
  reopening the freeze the mentor-review pass (same date) had put on new
  skill work pending real validation evidence. Building an eleventh skill
  is not evidence toward this assumption either way — it is stated here so
  the record doesn't imply otherwise by omission. Same date, Phase 12
  (`engineering-knowledge-capture`) was started the same way — a second,
  one-time user-directed exception to the same freeze, not new evidence
  A2 moved off UNKNOWN. Building a twelfth skill does not change this
  status either. Same date, Phase 13 (`context-optimizer`) was started
  the same way — a THIRD one-time user-directed exception to the same
  freeze, now deferred across three consecutive phase boundaries.
  Building a thirteenth skill does not change this status either. Same
  date, Phase 14 (`workflow-composer`) was started the same way — a
  FOURTH one-time user-directed exception, now deferred across four
  consecutive phase boundaries, and the first to also directly override a
  named, phase-specific decision (A10's "do not build Workflow Composer
  until Experiment B can be run"), not just the general freeze. Building a
  fourteenth skill does not change this status either.
- **Decision**: still required before claiming any skill is "Level 2 —
  Evaluated" *in the outcome sense* — codebase-intelligence,
  adversarial-diff-reviewer, and acceptance-test-engineer have each met the
  narrower "ships with evaluation cases" bar in [[04-skill-contract]], not
  this assumption. Do not run Experiment A "for real" using only one agent
  session — see ADR-009.

### A3: `SKILL.md` is a useful distribution format

- **Why we believe it**: Markdown is human-readable, diffable, and portable
  across current AI coding tools.
- **Risk**: lack of structure/typing could limit tooling (evaluation harness,
  registry search) as the ecosystem grows.
- **Validation experiment**: attempt to build the evaluation harness
  ([[05-evaluation-framework]]) against real `SKILL.md` files; note friction.
- **Expected evidence**: harness can parse/execute skills without excessive
  custom parsing logic.
- **Actual evidence**: `evaluations/codebase-intelligence/run_evaluation.py`
  was built against the real `skills/codebase-intelligence/SKILL.md` contract
  with no custom SKILL.md-parsing logic needed — the harness invokes the
  engine directly and scores its output, treating SKILL.md as human/agent-
  readable documentation rather than something the harness itself parses.
  That's a real gap worth naming: this doesn't yet prove SKILL.md's structure
  is machine-actionable, only that it's a workable *human-facing* contract.
- **Status**: PARTIALLY_VALIDATED — as documentation format, not yet as a
  machine-parseable one.
- **Decision**: see ADR-002 in [[11-decisions]] — format is deliberately not
  locked in. Revisit machine-parseability only if/when a registry or
  multi-skill harness needs to introspect SKILL.md programmatically.

### A4: Skills behave consistently enough across runtimes

- **Why we believe it**: the contract's Tool Permissions/Workflow sections are
  meant to be runtime-agnostic instructions.
- **Risk**: different agent runtimes may interpret instructions differently
  enough to break the "Compatible Runtimes" claim in a skill's metadata.
- **Validation experiment**: run the same skill + eval case set on ≥2 runtimes
  once one is built; compare scores.
- **Expected evidence**: comparable evaluation scores across runtimes for the
  same skill/case.
- **Actual evidence**: none yet — single-runtime only so far.
- **Status**: UNKNOWN.
- **Decision**: do not claim multi-runtime compatibility on any skill until
  tested on that runtime.

### A5: Skill quality can be objectively evaluated

- **Why we believe it**: the 0–5 dimension scoring plus precision/recall-style
  metrics ([[05-evaluation-framework]]) give a structured, repeatable rubric.
- **Risk**: scoring may still be too subjective/model-dependent to be trusted
  without heavy human review.
- **Validation experiment**: have two independent reviewers score the same
  skill run; measure agreement.
- **Expected evidence**: reasonable inter-rater agreement on scored dimensions.
- **Actual evidence**: for a deterministic, structural skill
  (codebase-intelligence), Correctness/Completeness/Efficiency scored fully
  automatically against hand-authored ground truth with no ambiguity (4/4
  fixtures, see `evaluations/codebase-intelligence/RESULTS.md`). Safety/
  Relevance/Explainability were, as designed, left unscored and flagged for
  human review — no inter-rater agreement experiment has been run on those.
  So the "objective" half of the rubric worked; the harder, judgment-based
  half remains untested.
- **Status**: PARTIALLY_VALIDATED — unchanged status, but now with a sharper
  picture of what's still missing. Phase 2 built the first judgment-based
  skill (`adversarial-diff-reviewer`) and attempted to evaluate it: 8 seeded-
  defect fixtures, this session's agent actually performed the adversarial
  review (not fabricated), and scored 100% precision/recall against hand-
  authored ground truth (`evaluations/adversarial-diff-reviewer/RESULTS.md`).
  However, this same agent authored the fixtures, the ground truth, AND the
  review — a stronger bias than plain single-rater variance (see L8 in
  [[12-known-limitations]]). The inter-rater-agreement experiment itself —
  a second, independent reviewer scoring the same fixtures blind — still has
  not been run.
- **Decision**: never let the model be sole evaluator of itself for critical
  claims, regardless of this experiment's outcome. The Phase 2 evidence
  should be read as "the workflow is executable and internally consistent,"
  not as "this skill reviews code well" — that claim requires either an
  independent rater or real external usage. Run the actual inter-rater
  experiment before upgrading this status further. Phase 3 repeated the same
  pattern for `acceptance-test-engineer` (100% precision/recall,
  `evaluations/acceptance-test-engineer/RESULTS.md`, same self-authored
  caveat, disclosed up front this time rather than discovered after the
  fact) — two-for-two on judgment-based skills scoring perfectly against
  their own authors' ground truth is itself a signal that this evaluation
  design cannot discriminate a genuinely good derivation from a mediocre
  one; that gap, not the scores, is the real finding. Phase 4 repeated the
  pattern a third time for `feature-planner` (100% precision/recall,
  `evaluations/feature-planner/RESULTS.md`, same caveat) — three-for-three
  then, and Phase 5 repeated it a fourth time for `security-context-guard`
  (100% precision/recall, `evaluations/security-context-guard/RESULTS.md`,
  same caveat) — four-for-four then. Phase 6 (`root-cause-analyzer`) is the
  fifth judgment-based skill evaluated this way, and the first that did
  **not** score perfectly on every fixture: 7/8 fixtures perfect, one
  (case-03) at 0.67/0.67 precision and recall
  (`evaluations/root-cause-analyzer/RESULTS.md`, L19 in
  [[12-known-limitations]]). This is disclosed as-is, not adjusted — and it
  does not resolve the underlying question either way: a single
  self-authored, single-rater case scoring below 100% is exactly as
  inconclusive about real-world quality as four cases scoring 100% were.
  The inter-rater-agreement experiment still has not been run for any of
  the five skills. Phase 7 (`architecture-decision`) is the sixth
  judgment-based skill evaluated this way, and returned to perfect
  precision/recall on all 8 fixtures
  (`evaluations/architecture-decision/RESULTS.md`) — this should not be
  read as evidence this skill's judgment quality is higher than
  `root-cause-analyzer`'s Phase 6 score; a single self-authored evaluation
  cannot support that comparison in either direction. The more interesting
  Phase 7 evidence on this question came from the real dogfood run, not the
  synthetic fixtures: it found and fixed one real gap in the deterministic
  layer (L20 in [[12-known-limitations]]) and surfaced, undisclosed by any
  fixture, a real limitation that only shows up at full-repository scale
  (L21) — a reminder that a clean self-authored fixture score and a
  skill's real-world behavior are answering different questions, exactly
  the point this assumption's status has tracked since Phase 2.
  The inter-rater-agreement experiment still has not been run for any of
  the six skills. Phase 8 (`refactoring-safety`) is the seventh
  judgment-based skill evaluated this way, and also scored perfect
  precision/recall on all 8 fixtures
  (`evaluations/refactoring-safety/RESULTS.md`) — same caveat as Phase 7:
  this is not evidence this skill's judgment quality exceeds
  `root-cause-analyzer`'s Phase 6 score, since a single self-authored
  evaluation cannot support that comparison either way. Once again, the
  real dogfood run was the more informative evidence: it surfaced a genuine
  cross-skill limitation (L22 in [[12-known-limitations]] —
  `codebase-intelligence`'s own `fan_in` count undercounting a real caller)
  that no synthetic fixture, authored by the same session that would have
  to notice the gap to test for it, could have found. The inter-rater-
  agreement experiment still has not been run for any of the seven skills.
  Phase 9 (`regression-hunter`) is the eighth judgment-based skill evaluated
  this way, and also scored perfect precision/recall on all 8 fixtures
  (`evaluations/regression-hunter/RESULTS.md`) — same caveat as Phases 7-8:
  this is not evidence this skill's judgment quality exceeds
  `root-cause-analyzer`'s Phase 6 score, since a single self-authored
  evaluation cannot support that comparison either way. The real dogfood
  run was again the more informative evidence: it correctly scored a real,
  already-tested `codebase-intelligence` fix as low-risk on both axes that
  mattered, and surfaced a new cross-skill limitation (L23 in
  [[12-known-limitations]] — `target_resolver.py`'s substring-based caller
  identification, shared as an independent copy between `refactoring-
  safety` and `regression-hunter`, inflates the caller list for any module
  with a short, common stem name) that, like L22 before it, no
  self-authored synthetic fixture could plausibly have surfaced. The
  inter-rater-agreement experiment still has not been run for any of the
  eight skills. Phase 10 (`release-readiness`) is the ninth judgment-based
  skill evaluated this way, and also scored perfect precision/recall on
  all 8 fixtures (`evaluations/release-readiness/RESULTS.md`) — same
  caveat as Phases 7-9: this is not evidence this skill's judgment quality
  exceeds `root-cause-analyzer`'s Phase 6 score, since a single
  self-authored evaluation cannot support that comparison either way. The
  real dogfood run was again the more informative evidence: it confirmed a
  predicted false-positive shape concretely (a legitimate CLI `print()`
  flagged as a debug leftover), and surfaced a materially new, more
  consequential manifestation of the L14/L19/L21/L23 limitation class (L24
  in [[12-known-limitations]] — `target_resolver.py`'s substring matching,
  reused a third time, now shown to produce false-positive test coverage,
  not just an inflated caller list) that, like L22/L23 before it, no
  self-authored synthetic fixture could plausibly have surfaced. The
  inter-rater-agreement experiment still has not been run for any of the
  nine skills. Phase 11 (`dependency-supply-chain`, 2026-08-26) is the
  tenth judgment-based skill evaluated this way and also scored perfect
  precision/recall on all 8 fixtures
  (`evaluations/dependency-supply-chain/RESULTS.md`) — same caveat, ten for
  ten now. This phase's real dogfood run (`examples/dependency-supply-chain/
  example-run.md`) again surfaced a genuine, pre-known limitation in
  practice rather than proving new judgment quality: run against this
  repo's own root, only 1 of the platform's real dependencies was visible,
  concretely confirming the inherited L2 root-level-only scope gap. Phase 12
  (`engineering-knowledge-capture`, 2026-08-26) is the eleventh judgment-based
  skill evaluated this way and also scored perfect precision/recall on all 8
  fixtures (`evaluations/engineering-knowledge-capture/RESULTS.md`) — same
  caveat, eleven for eleven now. This phase's real dogfood run
  (`examples/engineering-knowledge-capture/example-run.md`) again surfaced a
  genuine, newly-found limitation rather than proving new judgment quality:
  every candidate in the real run resolved to no location at all, because
  `location_resolver.py` only checks the exact matched line, not the
  surrounding paragraph a real narrative's module mention typically sits in
  (L28). Phase 13 (`context-optimizer`, 2026-08-26) is the twelfth
  judgment-based skill evaluated this way and also scored perfect
  precision/recall on all 8 fixtures
  (`evaluations/context-optimizer/RESULTS.md`) — same caveat, twelve for
  twelve now. This phase's real dogfood run
  (`examples/context-optimizer/example-run.md`) again surfaced a genuine,
  newly-found limitation rather than proving new judgment quality: at
  full-repository scale, 5 of 17 CORE-tier recommendations were unrelated
  files whose scores were inflated purely by this project's own recurring
  documentation/evaluation-harness vocabulary, a new manifestation of the
  same coincidental-keyword-collision mechanism class `architecture-
  decision`'s L14/L19/L21 first disclosed (L29). Phase 14
  (`workflow-composer`, 2026-08-26) is the thirteenth judgment-based skill
  evaluated this way and also scored perfect precision/recall on all 8
  fixtures (`evaluations/workflow-composer/RESULTS.md`) — same caveat,
  thirteen for thirteen now. This phase's real dogfood run
  (`examples/workflow-composer/example-run.md`) again surfaced a genuine,
  newly-found limitation rather than proving new judgment quality: the
  composed `feature-planner` step's own relevance scorer ranked a test
  file above every real implementation file relevant to the task — the
  same coincidental-keyword-collision mechanism class, now confirmed
  present inside `feature-planner` itself, not just `context-optimizer`
  (L30). The inter-rater-agreement experiment still has not been run for
  any of the thirteen skills.

### A6: Engineers will tolerate the additional workflow

- **Why we believe it**: human checkpoints and structured review are common in
  senior engineering practice already (PR review, design review).
- **Risk**: added ceremony could feel like friction versus a raw chat prompt.
- **Validation experiment**: Experiment A / C, tracking drop-off or workaround
  behavior (e.g., skipping the skill after first use).
- **Expected evidence**: repeat voluntary usage without being told to use it.
- **Actual evidence**: none yet.
- **Status**: UNKNOWN.
- **Decision**: pending.

### A7: Security-aware context handling materially increases trust

- **Why we believe it**: explicit classification/minimization should reduce
  accidental data exposure and make engineers more willing to grant tool access.
- **Risk**: may add perceived overhead without a visible trust payoff to the
  end user.
- **Validation experiment**: qualitative feedback from Security Context Guard
  (Phase 5) users on whether it changed their willingness to grant permissions.
- **Expected evidence**: users cite the security model as a reason for trusting
  a skill.
- **Actual evidence**: `security-context-guard` is now built
  ([[03-architecture]], ADR-011). Phase 5 ran a first internal pilot toward
  this assumption — Pilot C in [[17-experiment-viability-check]] — a real
  dogfood run against this session's own real pending git-push decision. The
  structured report's bottom-line recommendation (`REQUIRES_HUMAN_APPROVAL`
  for a `Publishing`-category action) matched what this session's existing
  bounded-autonomy behavior would already do without the skill, so on this
  one case the report didn't change the actual decision a human would see.
  What it did add: an explicit, auditable evidence trail (exact match
  counts, named category) an unstructured pass wouldn't spontaneously
  produce, and the dogfood process itself caught a real false-negative bug
  (L16 in [[12-known-limitations]]) before it could ever mislead a real
  decision. This is a real observation, but it is one N=1, self-rated data
  point about this session's own agent, not qualitative feedback from an
  actual human user deciding whether to grant more permissions — which is
  what this assumption's validation experiment actually requires.
- **Status**: UNKNOWN.
- **Decision**: still requires a real user (not this session's agent)
  reporting whether the structured classification changed their own
  willingness to grant permissions. Pilot C is a floor, not a substitute —
  same discipline ADR-009 applies to Pilot A/B.

### A8: Engineering memory improves future agent performance

- **Why we believe it**: validated historical context should reduce repeated
  mistakes and re-derivation of already-known facts.
- **Risk**: stale/unvalidated memory could actively degrade performance if
  treated as authoritative (Section 43 of the charter explicitly warns about
  this). Note (2026-08-26): the checked-in [[operating-charter]] contains no
  Section 43 — see [[12-known-limitations|L27]].
- **Validation experiment**: deferred — Engineering Memory is Phase 15, last in
  the roadmap by design.
- **Expected evidence**: TBD.
- **Actual evidence**: none — not yet in scope.
- **Status**: UNKNOWN.
- **Decision**: do not implement early; design only when reached.

### A9: Developers will contribute skills

- **Why we believe it**: open-source contribution model with a clear quality
  gate ([[06-security-model]]) should lower the bar to contribute safely.
- **Risk**: contract overhead (evaluation cases, security docs) may be too high
  for casual contributors.
- **Validation experiment**: track external PRs/issues once the repo is public
  and has ≥1 real skill.
- **Expected evidence**: at least one external contribution or substantive
  issue within a defined window post-publication.
- **Actual evidence**: none yet — nothing published.
- **Status**: UNKNOWN.
- **Decision**: pending publication of first skill.

### A10: Composed workflows outperform isolated skills

- **Why we believe it**: chaining understand → verify → plan should catch
  issues no single skill catches alone.
- **Risk**: composition overhead (context handoff, checkpoint friction) may
  erode the benefit — Experiment B exists specifically to test this.
- **Validation experiment**: Experiment B — normal AI vs. individual skill vs.
  composed workflow.
- **Expected evidence**: composed workflow shows measurably better outcomes
  than the best individual skill alone, net of added time/friction.
- **Actual evidence**: none yet at the required rigor — no formal workflow
  composition exists (Phase 14). Phase 3 ran a first viability check: with 3
  skills now covering UNDERSTAND → VERIFY → DEFINE CORRECTNESS, composition
  is technically possible for the first time, so a single-session, N=1,
  un-blinded internal pilot was run (Pilot B,
  [[17-experiment-viability-check]]) — feeding `codebase-intelligence`'s real
  Phase 1 output into `acceptance-test-engineer` resolved a specific
  assumption (which directories need READMEs) that the individual skill
  alone could only flag as unresolved. One data point, one requirement
  shape — not evidence composition wins in general.
- **Status**: UNKNOWN.
- **Decision**: do not build Workflow Composer (Phase 14) until Experiment B
  can be run on at least the first few individual skills, with a genuinely
  independent baseline — see ADR-009. The Phase 3 pilot shows a plausible
  signal worth re-testing at proper rigor, not proof composition works.
  Phase 4 changed the *architecture*, not the evidence: `feature-planner`
  makes composition with `codebase-intelligence` a hard precondition
  (ADR-010) rather than an optional pilot, and the real dogfood run
  (`examples/feature-planner/example-run.md`) shows composition being
  genuinely load-bearing — grounding "affected files" in the real report
  correctly identified the right target file and surfaced a real gap in a
  different skill (L13/L14 in [[12-known-limitations]]). That is stronger
  evidence composition *executes correctly and is used for real* than
  Phase 3's pilot was, but it is still not the rigorous, independently-
  baselined comparison Experiment B requires — one architecture existing
  and working is not the same as composition being *shown to outperform*
  the individual-skill alternative. Phase 6 (`root-cause-analyzer`, ADR-012)
  reuses `feature-planner`'s required-composition rule (ADR-010) a second
  time — required composition is now a pattern applied twice, by two
  different skills, not a one-off. The Phase 6 dogfood run
  (`examples/root-cause-analyzer/example-run.md`) is additional real-usage
  evidence in the same shape as Phase 4's: a fresh `codebase-intelligence`
  report was genuinely required and genuinely used, and correctly ranked a
  real historical root-cause file first out of 122 scored modules from a
  natural-language description alone. That is still retrospective-
  validation evidence on N=1, not the independently-baselined comparison
  Experiment B requires. Phase 7 (`architecture-decision`, ADR-013) reuses
  the same required-composition rule a third time — required composition
  is now a pattern applied by three different skills, strengthening the
  case that this is a real, repeatable architectural choice rather than a
  one-off. The Phase 7 dogfood run
  (`examples/architecture-decision/example-run.md`) is a different shape of
  evidence than Phase 4's or Phase 6's, though: composition was genuinely
  required and used, but the blast-radius signal it produced was too noisy
  at full-repo scale to be decisive either way for the real decision this
  session faced (L21 in [[12-known-limitations]]) — a case where required
  composition executed correctly but did not clearly demonstrate its value
  on this particular real use. That is an honest, disclosed data point
  against overclaiming composition's benefit, not for it. Phase 8
  (`refactoring-safety`, ADR-014) reuses the same required-composition rule
  a fourth time — required composition is now a pattern applied by four
  different skills. The Phase 8 dogfood run
  (`examples/refactoring-safety/example-run.md`) is closer in shape to
  Phase 4's and Phase 6's than Phase 7's: composition was genuinely
  required and used, every risk-tier and caller claim in the output traced
  to real structural data, and the run correctly grounded a real refactor
  target's blast radius — but it also surfaced a real limitation in the
  *composed* data itself (L22): `codebase-intelligence`'s own `fan_in`
  metric can silently undercount a real caller that this skill's own
  independent caller scan still finds. This is a new, more precise
  category of evidence than any prior phase produced: composition can
  execute correctly and be genuinely used, while still depending on an
  upstream report whose own internal consistency has not been fully
  verified — a reason for measured caution about composition's reliability
  guarantees, not its execution. Phase 9 (`regression-hunter`, ADR-015)
  reuses the same required-composition rule a fifth time — required
  composition is now a pattern applied by five different skills. The
  Phase 9 dogfood run (`examples/regression-hunter/example-run.md`) is
  closest in shape to Phase 8's: composition was genuinely required and
  used, every structural-tier and caller claim traced to real data from the
  composed report, and the run correctly scored a real, already-tested
  change as low-risk — but it also surfaced a limitation shared across TWO
  skills' independent copies of the same composition-consuming logic (L23):
  `target_resolver.py`'s substring-based caller-identification heuristic,
  present in both `refactoring-safety` and `regression-hunter` as
  independent copies (not a shared import, per this project's portability
  discipline), inflates the caller list for any composed-report module
  whose stem is a short, common word. This sharpens Phase 8's finding: it
  is not just that composition depends on an upstream report whose internal
  consistency has gaps (L22), but that two skills consuming that same
  report through the same resolution pattern can inherit the identical gap
  independently — a reason for even more measured caution about treating
  every consumer of a composed report as independently verified just
  because each one is independently tested. Phase 10 (`release-readiness`,
  ADR-016) reuses the same required-composition rule a sixth time —
  required composition is now a pattern applied by six different skills —
  and is also the FIRST skill in this platform to compose OPTIONALLY with
  two other skills' own outputs (`regression-hunter`'s and
  `security-context-guard`'s reports), not just `codebase-intelligence`'s.
  The Phase 10 dogfood run (`examples/release-readiness/example-run.md`)
  sharpens Phase 9's finding a third time: `target_resolver.py`'s
  substring-based resolution pattern, now reused a THIRD time, was shown
  for the first time to corrupt not just a displayed caller list (L23) but
  the actual `test_coverage.has_coverage` field a downstream rule table
  consumes to decide whether a file needs closer review (L24) — a
  genuinely untested new module can be made to look tested by the same
  underlying mechanism. This is the strongest evidence yet in this project
  that a shared resolution *pattern* (not a shared module — no cross-skill
  imports exist) can carry a real, increasingly consequential defect
  across independently-tested copies, without any single skill's own test
  suite being able to catch it, since each copy's tests are written
  against synthetic fixtures the same session authored. Status stays
  UNKNOWN.

  **Phase 14 update (2026-08-26)**: `workflow-composer` was built anyway,
  at the user's explicit direction, directly overriding this section's
  own "do not build Workflow Composer (Phase 14) until Experiment B can
  be run" decision — not because Experiment B became runnable or because
  A2/A5 moved off `UNKNOWN`. This is the first phase in this project to
  override a decision that named the overridden phase by number, not just
  the general roadmap freeze; see `08-roadmap.md` and `11-decisions.md`
  ADR-020 for the full process note. Once built, `workflow-composer`
  produced a real, timed pilot run
  (`examples/workflow-composer/example-run.md`): `understand-then-plan`
  executed for real against this repo's own current state (2 real
  subprocess steps, 2.31s total, zero compatibility issues) — genuine
  evidence composition *executes correctly end-to-end when actually run*,
  in the same shape as every prior phase's dogfood evidence above, and
  per ADR-009 explicitly disclosed as a pilot, not Experiment B. The same
  run also surfaced L30 in [[12-known-limitations]]: composing with
  `feature-planner` inherits that skill's own keyword-flooding
  susceptibility unfiltered (a test file outscored every relevant
  implementation file) — a reason for the same measured caution about
  composition's *content* reliability this section has named since
  Phase 8 (L22), not just its execution reliability. Status stays
  UNKNOWN — this phase is not new evidence for or against A10, only new
  evidence that the freeze around it has now been overridden four
  consecutive times, the last one specifically.
