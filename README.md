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

**Phase 3 — Acceptance Test Engineer complete.** Three skills exist:
[`skills/codebase-intelligence/`](skills/codebase-intelligence/) — a
structural repo-analysis skill;
[`skills/adversarial-diff-reviewer/`](skills/adversarial-diff-reviewer/) — a
diff-review skill combining a deterministic risk-flagging engine with an
agent-driven adversarial review workflow; and
[`skills/acceptance-test-engineer/`](skills/acceptance-test-engineer/) — a
requirement-to-acceptance-criteria skill using the same deterministic +
agent-driven pattern. All three are tested and evaluated, Trust Status
EXPERIMENTAL on all three (see
[`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md)
for what that status means). None has yet been used on real engineering work
by anyone outside this project's own development, and both judgment-based
skills' evaluation evidence is self-authored/single-rater (see
[`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md)
L8). Phase 3 also ran a first, explicitly-labeled viability check for the
product thesis's Experiment A/B — see
[`project-memory-bank/17-experiment-viability-check.md`](project-memory-bank/17-experiment-viability-check.md).
See
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
