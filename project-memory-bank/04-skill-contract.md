# 04 — Skill Contract

Canonical specification. Breaking changes to the contract itself require an
architectural decision entry in [[11-decisions]] — do not change it casually.

## A skill is not a prompt

A Skill is:

```
Intent + Inputs + Context Requirements + Preconditions + Workflow +
Agent Responsibilities + Tool Permissions + Human Checkpoints +
Security Constraints + Outputs + Verification + Failure Conditions +
Evaluation + Version + Provenance
```

## Canonical `SKILL.md` template

```markdown
# <Skill Name>

## Metadata
- Version:
- Status:
- Author:
- Maturity:
- Compatible Runtimes:

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
### Step 1
### Step 2
### Step 3

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

## Maturity model

| Level | Name | Definition |
|---|---|---|
| 0 | Prompt | One-off instruction, not a skill |
| 1 | Reusable Skill | Standardized `SKILL.md` |
| 2 | Evaluated Skill | Skill + evaluation cases |
| 3 | Trusted Skill | Skill + evaluation + security + provenance + known limitations |
| 4 | Composable Skill | Can participate in larger workflows |
| 5 | Adaptive Skill | Uses validated memory/feedback to improve future runs |

Never claim a maturity level beyond what the skill's evidence actually supports.

## Trust model

Every skill must eventually expose:

```
Trust Status | Evidence | Evaluation Results | Known Failure Modes |
Security Classification | Provenance | Version | Last Validation |
Human Review Requirement
```

Trust statuses (exactly these four — no others):

```
EXPERIMENTAL | PARTIALLY VERIFIED | VERIFIED | BLOCKED
```

Banned language: "100% reliable" or any equivalent unsupported reliability claim,
anywhere a skill's status is described (docs, UI, README, marketing).

See [[05-evaluation-framework]] for how a skill earns Level 2+/VERIFIED, and
[[06-security-model]] for the security classification a skill must carry.
