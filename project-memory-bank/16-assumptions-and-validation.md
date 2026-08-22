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
  matched real tasks) has not been run. Phase 1 and Phase 2 only prove each
  skill can be built and passes its own synthetic evaluation; neither
  compares against unstructured prompting on real work.
- **Status**: UNKNOWN.
- **Decision**: still required before claiming any skill is "Level 2 —
  Evaluated" *in the outcome sense* — codebase-intelligence and
  adversarial-diff-reviewer have each met the narrower "ships with evaluation
  cases" bar in [[04-skill-contract]], not this assumption.

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
  experiment before upgrading this status further.

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
- **Actual evidence**: none yet — Security Context Guard not built.
- **Status**: UNKNOWN.
- **Decision**: pending Phase 5.

### A8: Engineering memory improves future agent performance

- **Why we believe it**: validated historical context should reduce repeated
  mistakes and re-derivation of already-known facts.
- **Risk**: stale/unvalidated memory could actively degrade performance if
  treated as authoritative (Section 43 of the charter explicitly warns about
  this).
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
- **Actual evidence**: none yet — no workflow composition exists (Phase 14).
- **Status**: UNKNOWN.
- **Decision**: do not build Workflow Composer (Phase 14) until Experiment B
  can be run on at least the first few individual skills.
