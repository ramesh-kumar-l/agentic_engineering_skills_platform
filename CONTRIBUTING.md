# Contributing

The originally-scoped 15-skill portfolio is complete, plus a Test Engineering
Platform pipeline and a native Claude Code skill built on top of it — see the
[README](README.md#status-and-roadmap) for the current state. The roadmap is
frozen pending real external validation evidence, not open by default, so a
new skill needs the same justification any phase here has needed: a real gap,
not a nice-to-have. This document describes the bar any contribution — to
`skills/` or elsewhere — needs to meet.

## Proposing a skill

A skill is not a prompt. Every contributed skill must:

1. Follow the canonical contract in
   [`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md)
   — every required section of the `SKILL.md` template, not a subset.
2. Ship with evaluation cases per
   [`project-memory-bank/05-evaluation-framework.md`](project-memory-bank/05-evaluation-framework.md),
   including deliberately constructed failure cases.
3. Document security implications and an explicit trust status per
   [`project-memory-bank/06-security-model.md`](project-memory-bank/06-security-model.md).
   No skill claims "VERIFIED" without evidence backing it.
4. Meet the publication quality gate: clear purpose, documented inputs/outputs,
   documented limitations, working examples, no secrets, explicit version and
   provenance. Experimental skills must be labeled experimental.

## What we're not looking for yet

- New abstractions, orchestration, or workflow composition — those come after
  individual skills are validated (see [`ROADMAP.md`](ROADMAP.md)).
- UI/dashboard contributions — no UI is justified until there's a validated
  workflow to visualize.
- Skills that duplicate one already in the target portfolio without improving
  on it — check [`project-memory-bank/08-roadmap.md`](project-memory-bank/08-roadmap.md)
  first.

## Reporting issues

Bugs, false positives/negatives in a skill's evaluation, or usability friction
are exactly the kind of evidence this project needs — please include enough
detail (input, expected behavior, actual behavior) to reproduce.

## Security issues

Do not open a public issue for a security vulnerability — see
[`SECURITY.md`](SECURITY.md).
