# 05 — Evaluation Framework

Methodology for how a skill earns evaluated/trusted status
(see [[04-skill-contract]]). Framework only — no evaluation harness code exists
yet (see [[07-current-state]]).

## Principle

A convincing AI response is not engineering evidence. The model must never be the
sole evaluator of itself for critical claims. Use layered evaluation:

```
Automated Checks + Tests + Static Analysis + Structured Evaluation +
Human Review + Real-World Outcomes
```

## Per-case structure

Every evaluation case must define:

```
Input | Context | Expected Behavior | Acceptance Criteria | Actual Result |
Failure Modes | Score | Human Assessment
```

## Scored dimensions (0–5 each)

```
Correctness | Completeness | Safety | Relevance | Efficiency | Explainability
```

Where applicable, also measure: Precision, Recall, False Positives, False
Negatives, Time, Token Usage, Human Intervention.

## Evaluation harness architecture (target, not yet built)

```
Skill → Evaluation Dataset → Agent Runtime → Execution → Scoring → Report
```

Multi-runtime support (Claude, GPT, Gemini, Cline, others) is a later target —
do not over-engineer this before there's evidence it's needed.

## Failure-first engineering

Deliberately construct failure cases for every skill. Baseline categories to test
against (adapt per skill, e.g. for a review-type skill):

```
1. Obvious bug
2. Subtle bug
3. Concurrency bug
4. Security issue
5. Performance regression
6. Correct but unusual code
7. Large noisy diff
8. Missing context
9. Misleading implementation
10. Incorrect requirement
```

For each observed failure, record:

```
What failed | Why | Impact | Fix | Regression prevention
```

Failures are first-class product artifacts — never hide or paper over them (see
[[12-known-limitations]], holds the running failure catalog).

## Acceptance-coverage checklist

Companion to the failure-first list above, for skills whose job is *defining*
correctness rather than finding defects (e.g. `acceptance-test-engineer`,
Phase 3). Go through each category explicitly for a given requirement:

```
1. Happy path / primary success        6. Duplicate / repeat / idempotency
2. Boundary / edge values              7. Concurrent access (if applicable)
3. Invalid input / error handling      8. Authorization boundary (if applicable)
4. Explicit negative case (must-not)   9. Stated non-functional constraint
5. Empty / missing / null state       10. Explicit assumption flag (requirement
                                          silent → state the assumption, don't
                                          guess silently)
```

Category 10 is the honesty valve: when the requirement doesn't say, the agent
must say so explicitly rather than picking a plausible interpretation and
presenting it as derived fact.

## Plan Quality checklist

Third checklist, for skills whose job is *turning a vague task into a
structured plan* (`feature-planner`, Phase 4). Go through each category
explicitly for a given task:

```
1. Scope statement (goal/deliverable)     6. Rollback/reversibility per risky step
2. Explicit non-goals / out-of-scope      7. Test/acceptance-criteria hook
3. Affected files — grounded in real      8. Security/permission touchpoints
   repo structure, not guessed            9. Dependencies & blockers
4. Ordered step sequence, each step      10. Explicit assumption flag (context
   independently verifiable                 silent → state it, don't guess)
5. Risk & blast-radius assessment
   (fan-in/fan-out/hotspot signal)
```

**Convention, established across the first three checklists**: category 10 is
always the honesty valve. The failure-first checklist doesn't need one (its
job is finding defects, not resolving ambiguity), but both checklists whose
job is *defining* something ambiguous end their list the same way — state
the assumption, don't guess silently.

## Security Decision Checklist

Fourth checklist, for skills whose job is *deciding whether an action needs
human authorization* (`security-context-guard`, Phase 5). Unlike the three
checklists above, this one is not a coverage-enumeration list — it's a
decision-gate/verdict workflow, so it's shaped differently on purpose:

```
1. Data classification (none/low/medium/high, with evidence)
2. Minimization opportunity (can less be exposed and still work?)
3. Sanitization applied (secrets/PII redacted, never raw, in every output)
4. Authorization requirement (does this match a project-memory-bank/
   06-security-model.md high-risk action category?)
5. Recommendation (AUTHORIZE / REQUIRES_HUMAN_APPROVAL) + rationale —
   framed as advice to a human, never a self-executed gate
6. Audit entry (what/why/when, durable-log-shaped)
7. Explicit uncertainty flag — if evidence is inconclusive, say so and
   default toward REQUIRES_HUMAN_APPROVAL; never silently AUTHORIZE
```

Category 7 is this checklist's version of the honesty-valve convention,
adapted from "state the assumption" to **"fail closed under uncertainty"**
— appropriate for a checklist whose job is a safety decision, not defining
ambiguous scope. Keep this convention (an honesty-valve final category,
adapted to the checklist's actual job) if a future skill adds a fifth
checklist of this shape.

## Root Cause Investigation Checklist

Fifth checklist, for skills whose job is *diagnosing why a failure happened*
(`root-cause-analyzer`, Phase 6). Shaped like the acceptance-coverage and
Plan Quality checklists (a coverage-enumeration list, not a decision-gate
like the Security Decision Checklist) because the job here is enumerating
what a complete investigation covers, not issuing a binary verdict:

```
1. Symptom restated precisely (observed vs. expected behavior)
2. Reproduction context (steps/trigger/frequency, if stated)
3. Candidate locations — grounded in the candidate report, not guessed
4. Evidence tier distinguished (stack-trace-confirmed vs. keyword-inferred)
5. Blast-radius / hotspot context for each candidate (fan-in/fan-out signal)
6. Recent-change correlation (deploy/release timing, if mentioned)
7. Ruled-out candidates and why (negative evidence, not just positive leads)
8. Confirmation step to prove the root cause before proposing a fix
9. Fix-risk note (does the suspected fix touch a hotspot/high fan-in module?)
10. Explicit assumption flag (evidence silent → state it, don't guess which
    location is truly the root cause)
```

**Convention, established across all five checklists now**: category 10 is
always the honesty valve when the checklist's job is *defining* or
*diagnosing* something ambiguous (this one and the three coverage-shaped
checklists before it); the Security Decision Checklist's category 7 adapts
the same convention to "fail closed" because its job is a gate, not an
enumeration. Category 4 here is specific to this skill: distinguishing
evidence tiers is what stops a coincidental keyword match from being
presented with the same confidence as a real stack-trace hit (see ADR-012
in [[11-decisions]]).

## Architecture Decision Record Checklist

Sixth checklist, for skills whose job is *weighing a decision between
alternatives* (`architecture-decision`, Phase 7). Shaped like the
acceptance-coverage, Plan Quality, and Root Cause Investigation checklists
(a coverage-enumeration list, not a decision-gate like the Security
Decision Checklist) — the job here is enumerating what a complete decision
record covers, not issuing a binary approve/deny verdict:

```
1. Context stated precisely
2. Alternatives identified — real, grounded in what was parsed from the
   decision text, not invented by the agent
3. Decision explicitly stated
4. Consequences / tradeoffs stated, per option, not one-sided
5. Reversibility assessed per option
6. Blast radius grounded in real structural data, not assumed (a
   zero-match option means "ungrounded," not "safe" — see ADR-013)
7. Security implications considered (or explicit N/A)
8. Evidence cited, not opinion
9. Future evolution / revisit trigger stated
10. Explicit assumption flag (evidence silent → state it, don't guess)
```

**Convention, established across all six checklists now**: category 10 is
always the honesty valve when the checklist's job is *defining*,
*diagnosing*, or *deciding* something ambiguous (this one and the four
coverage-shaped checklists before it); the Security Decision Checklist's
category 7 adapts the same convention to "fail closed" because its job is a
gate, not an enumeration. Category 6 here is specific to this skill:
distinguishing "the engine found nothing because the option is genuinely
low-impact" from "the engine found nothing because the decision text never
named a real target" is what stops an ungrounded option from being read as
a safe one (see ADR-013 in [[11-decisions]] and evaluation case-04's Option
B, where a real, high-risk option scored zero matched modules because its
target went unnamed).

## Refactoring Safety Checklist

Seventh checklist, for skills whose job is *assessing whether a proposed
refactor is safe to execute* (`refactoring-safety`, Phase 8). Shaped like
the acceptance-coverage, Plan Quality, Root Cause Investigation, and
Architecture Decision Record checklists (a coverage-enumeration list, not a
decision-gate like the Security Decision Checklist) — the job here is
enumerating what a complete safety assessment covers, not issuing a binary
approve/deny verdict:

```
1. Operation type stated precisely     6. Verification step stated (how
   (not a vague "refactor")               success will be confirmed)
2. Targets identified — real,          7. Behavioral equivalence / scope
   resolved against the codebase-         explicitly asserted (does this
   intelligence report, not invented      refactor also change behavior,
3. Callers / blast radius assessed        or only structure?)
   from real fan-in data, not          8. Security implications
   guessed                                considered (or explicit N/A)
4. Test coverage verified per          9. Evidence cited, not opinion
   target — covered vs. genuinely     10. Explicit assumption flag
   untested distinguished, not            (evidence silent → state it,
   conflated with text-level             don't guess)
   silence
5. Rollback / reversibility plan
   stated
```

**Convention, established across all seven checklists now**: category 10
is always the honesty valve when the checklist's job is *defining*,
*diagnosing*, or *deciding* something ambiguous (this one and the five
coverage-shaped checklists before it); the Security Decision Checklist's
category 7 adapts the same convention to "fail closed" because its job is a
gate, not an enumeration. Category 4 here is specific to this skill:
distinguishing "the refactor text never mentions tests" (a text-level
absence) from "this target has no real test coverage" (a structural fact,
independently computed) is what stops a well-written description from
being read as evidence of actual verification — the two signals can and do
diverge, and conflating them is exactly the failure mode evaluation
case-03 exists to catch (see ADR-014 in [[11-decisions]]).

## Regression Risk Checklist

Eighth checklist, for skills whose job is *identifying which existing
behavior is at risk of regressing from a diff* (`regression-hunter`, Phase
9). Shaped like the acceptance-coverage, Plan Quality, Root Cause
Investigation, Architecture Decision Record, and Refactoring Safety
checklists (a coverage-enumeration list, not a decision-gate like the
Security Decision Checklist) — the job here is enumerating what a complete
regression-risk assessment covers, not issuing a binary approve/deny
verdict:

```
1. Existing behavior at risk stated       6. False-positive check (is a
   precisely per file, not just              flagged pattern actually
   "this diff looks risky"                   safe here, e.g. exception
2. Diff-pattern flags reviewed —              re-raised elsewhere)
   distinguished from real evidence,       7. Missing-coverage files
   not treated as proof                       explicitly named, not
3. Structural blast radius grounded           silently accepted
   in real fan-in/hotspot data, not       8. Security implications
   guessed                                    considered (or explicit N/A)
4. Test coverage verified per file —      9. Evidence cited, not opinion
   covered vs. genuinely untested        10. Explicit assumption flag
   distinguished, not conflated               (evidence silent → state it,
5. Overall risk tier explained via the        don't guess)
   documented rule table, not asserted
```

**Convention, established across all eight checklists now**: category 10 is
always the honesty valve when the checklist's job is *defining*,
*diagnosing*, or *deciding* something ambiguous (this one and the six
coverage-shaped checklists before it); the Security Decision Checklist's
category 7 adapts the same convention to "fail closed" because its job is a
gate, not an enumeration. Category 2 here is specific to this skill:
distinguishing "a diff-pattern flag fired" from "a real regression exists"
is what stops a mechanically-detected shape (e.g. a removed `except` block
that was genuinely dead code) from being presented with the same confidence
as an actually-verified defect — the fixed pattern table is a lead
generator (ADR-007), never a verdict, the same discipline every prior
Pattern 2 skill's anti-pattern table already established. Category 5 is
this skill's version of the three-axis discipline ADR-015 introduces:
`overall_risk_tier` traces to a documented, inspectable rule table
combining Axis 1 (diff-pattern flags), Axis 2 (structural blast radius),
and Axis 3 (test coverage) — the checklist walk should be able to explain
*why* a file landed at a given tier from the three underlying fields, not
just repeat the tier as an assertion.

## Release Readiness Checklist

Ninth checklist, for skills whose job is *assessing whether a body of work
is ready to ship* (`release-readiness`, Phase 10 — the final skill in the
Engineering Lifecycle group). Shaped like the acceptance-coverage, Plan
Quality, Root Cause Investigation, Architecture Decision Record,
Refactoring Safety, and Regression Risk checklists (a coverage-enumeration
list, not a decision-gate like the Security Decision Checklist) for most of
its categories — but, uniquely among the coverage-shaped checklists, it
also carries a non-negotiable framing requirement (category 10) because
this skill's output is this portfolio's single highest-stakes
recommendation:

```
1. Scope stated precisely (what is       6. Overall verdict explained via
   actually being released, not just         the documented rule table,
   "this diff")                              not asserted
2. Diff-hygiene blockers reviewed as     7. False-positive check (is a
   absolute, not leads — a hygiene           flagged pattern actually
   flag means blocked, full stop            safe here, e.g. a legitimate
3. Structural blast radius grounded         print() in a CLI's own output)
   in real fan-in/hotspot data, not      8. Evidence cited, not opinion
   guessed                              9. Explicit assumption flag
4. Test coverage distinguished per          (evidence silent → state it,
   file — covered vs. genuinely             don't guess)
   untested, not conflated            10. Verdict framed as advisory/
5. Regression/security evidence             human-checkpoint, NEVER an
   surfaced-not-re-derived when              auto-gate — the single
   present, explicitly marked                non-negotiable category this
   ABSENT (not assumed clean) when           checklist adds beyond every
   not supplied                              prior coverage-shaped one
```

**Convention, established across all nine checklists now**: category 9 is
always the honesty valve when the checklist's job is *defining*,
*diagnosing*, or *deciding* something ambiguous (this one and the seven
coverage-shaped checklists before it); the Security Decision Checklist's
category 7 adapts the same convention to "fail closed" because its job is a
gate, not an enumeration. Category 10 here is genuinely new across the
whole set: no prior checklist required a non-negotiable framing statement
in every single walk, because no prior skill's output was this project's
single highest-stakes recommendation. Category 5 is specific to this
skill's optional-composition design (ADR-016): surfacing a composed
regression/security signal verbatim, distinct from this skill's own
always-available axes, is what stops a `READY` verdict (which reflects only
Axes 1-3) from being silently read as "no regression risk exists" when a
composed `regression-hunter` report actually shows otherwise — see
evaluation case-07's deliberate divergence design.

## Dependency Risk Checklist

Tenth checklist, for `dependency-supply-chain` (Phase 11). Shaped like the
Security Decision Checklist (a decision-gate, not a coverage-enumeration
list) since this skill's job is producing one advisory recommendation, not
enumerating independent findings:

```
1. Manifest completeness (via CI report - note any zero-dependency warning)
2. Pin status assessment (which unpinned/wildcard deps matter here)
3. Known-risk pattern matches (verify each against its cited incident)
4. License risk - NOT available this version; state that explicitly
   rather than guessing (see SKILL.md Known Limitations)
5. Duplicate/conflicting version declarations
6. Surface-area assessment (unpinned %, manifest breakdown)
7. Recommendation (advisory risk level + rationale) - framed as advice
   to a human, never a self-executed gate
8. Explicit uncertainty flag - if evidence is inconclusive, say so and
   default toward REQUIRES_REVIEW; never silently CLEAR
```

Category 8 is this checklist's fail-closed-under-uncertainty item, same
convention as the Security Decision Checklist's category 7. Category 4 is
new in kind, not just content: it's a checklist item whose correct answer
is always "not available" in this skill's current version, stated as such
rather than removed - an explicit, disclosed gap the checklist forces the
agent to name every single walk, rather than one it could silently skip.

## Knowledge Capture Checklist

Eleventh checklist, for `engineering-knowledge-capture` (Phase 12). Shaped
like the Security Decision Checklist and the Dependency Risk Checklist
(a decision-gate, not a coverage-enumeration list) since this skill's job
is producing one recommendation per candidate (capture it or don't), not
enumerating independent findings:

```
1. Narrative scope stated (what session/change/timeframe does this cover?)
2. Candidates reviewed per category (decision/lesson/limitation/workaround)
3. Structural relevance considered (hotspot/high-fan-in module -> higher
   priority to actually write up)
4. False-positive check (is this genuinely new knowledge, or restating
   something already captured elsewhere in the memory bank?)
5. Duplicate check against existing ADRs/L-numbers (agent responsibility -
   the engine has no memory-bank access and cannot know this itself)
6. Draft canonical entry (ADR / L-number / lesson-learned shape) for
   candidates worth keeping - this skill's actual deliverable
7. Explicit uncertainty flag - thin/ambiguous narrative or an unresolved
   location defaults toward MEDIUM priority and says so, never silently LOW
```

Category 7 is this checklist's fail-closed-under-uncertainty item, same
convention as the Security Decision Checklist's category 7 and the
Dependency Risk Checklist's category 8. Category 5 is new in kind, not
just content, the same way the Dependency Risk Checklist's category 4
was: it's a checklist item the engine can never answer on its own (it has
no `project-memory-bank/` access), so the checklist forces the agent to
do a real duplicate check every walk rather than silently skipping it.
This is also the first checklist in the portfolio whose category 6 is
itself the skill's actual deliverable (drafting the entry) rather than a
verdict about code — the checklist doesn't end at "recommend," it ends at
"produce the artifact," reflecting ADR-018's "documentation artifact, not
a code-risk judgment" framing.

## Context Optimization Checklist

Twelfth checklist, for `context-optimizer` (Phase 13). Shaped like the
Security Decision Checklist, the Dependency Risk Checklist, and the
Knowledge Capture Checklist (a decision-gate, not a coverage-enumeration
list) since this skill's job is producing one recommendation per task
(what to load), not enumerating independent findings:

```
1. Task scope stated (what is the agent about to actually do?)
2. CORE tier reviewed for completeness - any obviously-needed file that
   keyword matching wouldn't catch (a semantic-gap check the engine
   cannot do itself)
3. SUPPORTING tier reviewed for genuine value vs. noise
4. Oversized-single-file flags reviewed - consider an excerpt/summary
   instead of full inclusion (the modularity callback)
5. Budget honesty check - if a budget was applied, confirm nothing
   load-bearing was silently excluded
6. Duplicate/redundant coverage check (two files recommended that cover
   the same ground)
7. Explicit uncertainty flag - a low-but-nonzero relevance score still
   earns at least SUPPORTING, and this item says so, never silently
   narrowing further
```

Category 7 is this checklist's fail-under-uncertainty item, same
convention as every checklist before it — but, uniquely among this
portfolio's checklists so far, it names a fail-**OPEN** (toward
inclusion) default rather than a fail-closed (toward caution) one, per
ADR-019's inversion of the ADR-011/017/018 convention: here, silently
excluding a needed file is the worse failure, not silently including an
unimportant one. Category 2 is this checklist's version of the
Knowledge Capture Checklist's category 5 (a check the engine structurally
cannot perform itself — recognizing a *missing* file requires
understanding the task's real intent, not just literal keyword overlap
with what already scored above zero) — it forces the agent to actively
look for a gap, not just review what the engine already surfaced.
