# Agentic Engineering Skills Platform

An open effort to build reusable, evaluated, secure engineering capabilities for
AI coding agents, distributed as a portable `SKILL.md` contract.

We believe engineers lack standardized, trustworthy, evaluated capabilities for
AI agents today — but that's a hypothesis we're actively testing, not a claim
we're making. See [`project-memory-bank/01-product-thesis.md`](project-memory-bank/01-product-thesis.md)
for the thesis and [`project-memory-bank/16-assumptions-and-validation.md`](project-memory-bank/16-assumptions-and-validation.md)
for what's actually been validated so far (currently: nothing — this project is
in its foundation phase).

## Status

**Phase 5 — Security Context Guard complete.** Five skills exist:
[`skills/codebase-intelligence/`](skills/codebase-intelligence/) — a
structural repo-analysis skill;
[`skills/adversarial-diff-reviewer/`](skills/adversarial-diff-reviewer/) — a
diff-review skill combining a deterministic risk-flagging engine with an
agent-driven adversarial review workflow;
[`skills/acceptance-test-engineer/`](skills/acceptance-test-engineer/) — a
requirement-to-acceptance-criteria skill using the same deterministic +
agent-driven pattern;
[`skills/feature-planner/`](skills/feature-planner/) — a task-to-structured-
plan skill that **requires** a `codebase-intelligence` report as a hard
precondition (see ADR-010 in
[`project-memory-bank/11-decisions.md`](project-memory-bank/11-decisions.md)),
the first skill in this project where composition with another skill's
output is mandatory rather than optional; and
[`skills/security-context-guard/`](skills/security-context-guard/) — a
classify/minimize/sanitize skill implementing
[`project-memory-bank/06-security-model.md`](project-memory-bank/06-security-model.md)'s
`Classify → Minimize → Sanitize → Authorize → Execute → Audit` workflow,
whose engine output is **always advisory** — it classifies and recommends,
never authorizes an action itself (see ADR-011). All five are tested and
evaluated, Trust Status EXPERIMENTAL on all five (see
[`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md)
for what that status means). None has yet been used on real engineering work
by anyone outside this project's own development, and all four judgment-
based skills' evaluation evidence is self-authored/single-rater (see
[`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md)
L8 — now applying four times). Phase 3 ran a first, explicitly-labeled
viability check for the product thesis's Experiment A/B, and Phase 5 added a
third pilot (Pilot C) toward Assumption A7 (does security handling increase
trust) — see
[`project-memory-bank/17-experiment-viability-check.md`](project-memory-bank/17-experiment-viability-check.md).
Phase 5's real dogfood run
([`examples/security-context-guard/example-run.md`](examples/security-context-guard/example-run.md))
found and fixed a real bug in its own action classifier before it could
mislead a real decision. See
[`project-memory-bank/07-current-state.md`](project-memory-bank/07-current-state.md)
for the authoritative current state.

## Where to start

- [`project-memory-bank/00-project-vision.md`](project-memory-bank/00-project-vision.md) — long-term vision
- [`project-memory-bank/01-product-thesis.md`](project-memory-bank/01-product-thesis.md) — the problem and who it's for
- [`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md) — what a "skill" is and its `SKILL.md` format
- [`ROADMAP.md`](ROADMAP.md) — current phase plan
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to propose a skill

## License

Apache 2.0 — see [`LICENSE`](LICENSE).
