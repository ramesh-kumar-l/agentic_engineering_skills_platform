# 00 — Project Vision

Stable, long-term. Update rarely, and only on deliberate strategic change.
Distilled from [[operating-charter]] §1.

## What we are building

An open ecosystem of reusable agentic engineering capabilities based on a portable
`SKILL.md` contract — a **trustworthy, evaluated, reusable capability layer for
AI-native software engineering**.

We are explicitly **not** building "a collection of Claude prompts."

## The capability progression (north star)

```
One-off Prompt
      ↓
Reusable Skill
      ↓
Evaluated Skill
      ↓
Trusted Skill
      ↓
Composable Workflow
      ↓
Skill Registry
      ↓
Community Ecosystem
      ↓
Engineering Knowledge
      ↓
Engineering Memory
      ↓
AI-Native Engineering System
      ↓
Engineering Cognition Infrastructure
```

`Skill` is the conceptual abstraction. `SKILL.md` is the *initial* portable
representation of it — chosen for portability across models/runtimes today, not
assumed to be the final form. The architecture must stay able to migrate to a
different representation if evidence says another one serves better (see
[[11-decisions]]).

## What the system continuously optimizes for

```
USEFULNESS + CORRECTNESS + SECURITY + TRUST + EVIDENCE + PORTABILITY + COMMUNITY VALUE
```

Never traded against raw automation volume, prompt count, or token throughput.

## Non-negotiable operating stance

- Build the smallest system that can teach us something important.
- Prove the skill before building the platform.
- Prove the workflow before building orchestration.
- Prove the trust model before making trust claims.
- Prove user value before scaling.
- Never trade evidence for confidence, security for convenience, or simplicity for
  premature scalability.
- Never continue past a phase boundary without explicit user instruction
  (see [[08-roadmap]]).

See [[01-product-thesis]] for the problem/user thesis this vision serves, and
[[16-assumptions-and-validation]] for what is actually proven vs. still assumed.
