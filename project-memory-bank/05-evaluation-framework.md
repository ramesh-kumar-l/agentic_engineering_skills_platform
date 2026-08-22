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
