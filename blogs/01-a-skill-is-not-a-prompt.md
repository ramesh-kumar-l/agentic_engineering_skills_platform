# A Skill Is Not a Prompt

*Part 1 of 5 in the Agentic Engineering Skills Platform series. Code and
data referenced here are real and current as of Phase 5 of the project.
[Repo README](../README.md).*

## The prompt that worked, until it didn't

Every engineer who's used an AI coding agent for more than a week has a
folder of prompts they reuse. "Review this diff like a senior engineer
looking for security issues." "Turn this vague ticket into acceptance
criteria." They work — until someone else on the team asks to borrow one,
and you realize you can't actually hand it over. What does it expect as
input? What should it never be used for? Does it need file access? Did it
work well last time because the prompt is good, or because the diff was
small and forgiving? There's no way to know, because a prompt carries none
of that information. It's not versioned. It has no declared inputs or
outputs. It has no record of the five times it quietly missed something
important.

That gap is the starting point for this project. Not "AI agents should
write more code" — they already do that fine — but "the *capabilities* we
hand to AI agents deserve the same rigor we'd demand of any other piece of
engineering infrastructure: a contract, tests, evaluation, security
boundaries, and an honest account of where they're known to fail."

## The capability progression

The project's [vision document](../project-memory-bank/00-project-vision.md)
frames this as a ladder, and it's worth being explicit that most AI tooling
today — including a lot of what gets marketed as "agentic" — sits on the
first rung:

```mermaid
flowchart LR
    A["One-off Prompt"] --> B["Reusable Skill"]
    B --> C["Evaluated Skill"]
    C --> D["Trusted Skill"]
    D --> E["Composable Workflow"]
    E --> F["Skill Registry"]
    F --> G["Community Ecosystem"]
    G --> H["Engineering Knowledge"]
    H --> I["Engineering Memory"]
    I --> J["AI-Native Engineering System"]

    style A fill:#eee,stroke:#999
    style B fill:#f5f5dc,stroke:#999
    style C fill:#dff0d8,stroke:#3c763d,stroke-width:2px
    style D fill:#d9edf7,stroke:#31708e
```

A **Skill** is the conceptual abstraction the whole ladder is built on:

```
Intent + Inputs + Context Requirements + Preconditions + Workflow +
Agent Responsibilities + Tool Permissions + Human Checkpoints +
Security Constraints + Outputs + Verification + Failure Conditions +
Evaluation + Version + Provenance
```

A prompt gives you the first two of those, maybe three, if you're careful.
Everything else — the part that lets a skill be trusted, reused,
composed, or handed to a stranger — is missing by construction, not by
oversight. That's the actual argument for a contract: not "prompts are bad,"
but "a prompt cannot carry the information a real capability needs to
carry."

## What `SKILL.md` actually requires

The project's [skill contract](../project-memory-bank/04-skill-contract.md)
defines a canonical template every skill in this repo follows exactly —
not a subset, not a rough approximation:

```
# <Skill Name>

## Metadata          (Version, Status, Author, Maturity, Compatible Runtimes)
## Purpose
## Problem
## When to Use
## When NOT to Use
## Preconditions
## Inputs
## Required Context
## Context Completeness
## Security Constraints

## Workflow
### Step 1 / Step 2 / Step 3 ...

## Agent Responsibilities
## Tool Permissions
## Human Checkpoints
## Outputs
## Verification
## Evaluation
## Failure Conditions
## Known Limitations
## Examples
## Provenance
## Changelog
```

Two sections are worth pausing on because they're the ones a prompt
structurally cannot have.

**"When NOT to Use."** Every skill in this repo states, in writing, the
conditions under which it should *not* be reached for. `security-context-guard`'s
`SKILL.md` says its pattern tables are "leads, not verdicts" and that the
skill's output is "never proof content contains no sensitive data." That's
not hedging — it's the difference between a tool an engineer can calibrate
trust around and a black box that either works or doesn't, with no way to
tell which case you're in until it's too late.

**"Known Limitations."** Every skill ships with an explicit, itemized list
of what it's known to get wrong, cross-referenced to
[`project-memory-bank/12-known-limitations.md`](../project-memory-bank/12-known-limitations.md).
Five of those limitations were found by actually using the skill on real
work and are documented with the exact failure, the fix, and the regression
test that now guards it — see
[part 3 of this series](03-i-dogfooded-every-skill-i-built.md) for the full
account.

## The maturity model — and refusing to round up

Not every skill in this repo is at the same trust level, and the contract
defines exactly what separates them:

| Level | Name | Definition |
|---|---|---|
| 0 | Prompt | One-off instruction, not a skill |
| 1 | Reusable Skill | Standardized `SKILL.md` |
| 2 | Evaluated Skill | Skill + evaluation cases |
| 3 | Trusted Skill | Skill + evaluation + security + provenance + known limitations |
| 4 | Composable Skill | Can participate in larger workflows |
| 5 | Adaptive Skill | Uses validated memory/feedback to improve future runs |

All five skills in this repo currently sit at **Level 2 — Evaluated**, and
every one of them is labeled `Trust Status: EXPERIMENTAL`. That's a
deliberate, load-bearing choice, not modesty. The trust model bans a
specific category of language outright — no skill's docs, UI, or README may
claim "100% reliable" or any equivalent unsupported reliability claim,
anywhere. Four of the five skills' evaluation harnesses currently *report*
100% precision/recall on their judgment layer, and every single one of
those reports opens with a paragraph explaining why that number should not
be read as proof of quality (self-authored fixtures, self-authored ground
truth, no independent rater — see
[`L8`](../project-memory-bank/12-known-limitations.md)). A skill contract
that lets you say "100%" without saying *why that 100% doesn't mean what it
looks like it means* isn't actually enforcing honesty — it's just adding
paperwork. Part 4 of this series digs into exactly why that distinction
matters.

## Five skills, one contract, no shortcuts

As of this post, the platform has five skills, each independently tested
and evaluated:

| Skill | What it does |
|---|---|
| `codebase-intelligence` | Deterministic structural map of a repo |
| `adversarial-diff-reviewer` | Risk-flags a diff, then an agent adversarially reviews it |
| `acceptance-test-engineer` | Turns a requirement into structured acceptance cases |
| `feature-planner` | Turns a task into a grounded, structured plan |
| `security-context-guard` | Classifies content/actions and recommends (never self-authorizes) approval |

Every one of them follows the exact same `SKILL.md` template above, ships
with its own test suite, its own evaluation harness, and its own real
dogfood run against actual work — not five different ad-hoc formats that
happen to share a repo. That consistency is itself a design decision: a
contract only earns its keep if it's actually enforced the same way every
time, including on the fifth skill when it would be tempting to cut a
corner because the pattern already feels proven.

## What this buys you, concretely

If you're evaluating whether to trust a skill (your own, or someone else's
built this way), the contract gives you a fixed checklist instead of a
vibe check: read the Preconditions and Inputs to know exactly what it
needs; read Security Constraints and Human Checkpoints to know what it's
allowed to do without asking; read Known Limitations to know where it's
already been shown to fail; read the Evaluation section to know exactly how
much (or how little) evidence backs the trust status it claims. None of
that exists for a prompt, no matter how well-crafted. That's the whole
argument — not that prompts are worthless, but that "a capability I can
hand to someone else, with a straight face, and have them know what they're
getting" requires more structure than a prompt can carry.

**Next in this series:** [Two Architectures for AI Agent Skills](02-two-architectures-for-ai-agent-skills.md)
— how this project decides, per skill, whether a task belongs in
deterministic code or in an agent's judgment, and what happens when that
line gets blurred.
