# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Phase 2: Adversarial Diff Reviewer — second skill
  (`skills/adversarial-diff-reviewer/`): `SKILL.md` contract combining a
  deterministic risk-flagging engine (9 modules, each under 300 lines, 19
  passing tests) with an agent-driven adversarial review workflow, an
  8-fixture evaluation harness scoring both the deterministic layer
  (automated) and a judgment layer (this session's agent actually performing
  each review — `evaluations/adversarial-diff-reviewer/`), and a dogfood run
  against a real in-session diff (`examples/adversarial-diff-reviewer/`) that
  found and fixed two real secret-redaction bugs in sequence.
- ADR-007 (deterministic pre-processor + agent-driven adversarial workflow
  pattern) and ADR-008 (redact-not-exclude for secrets in diff content) in
  `project-memory-bank/11-decisions.md`.
- Phase 1: Codebase Intelligence — first real skill
  (`skills/codebase-intelligence/`): `SKILL.md` contract, stdlib-only Python
  engine (11 modules, each under 300 lines, 23 passing tests), a 4-fixture
  evaluation harness (`evaluations/codebase-intelligence/`, all passing), and
  a dogfood run against this repo (`examples/codebase-intelligence/`) that
  found and fixed a real false-positive entry-point detection bug.
- New memory-bank files: `03-architecture.md`, `12-known-limitations.md`,
  `implementation-status.md`, `active-context.md`.
- ADR-005 (SKILL.md + deterministic engine pattern) and ADR-006 (stdlib-only
  Python engine choice) in `project-memory-bank/11-decisions.md`.
- Phase 0: Foundation — established `project-memory-bank/` (project vision,
  product thesis, requirements, skill contract, evaluation framework, security
  model, current-state tracking, roadmap, architectural decisions, assumptions
  ledger, and Sprint 00 record).
- Repository scaffolding: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `ROADMAP.md`.

No skill has been used on real (non-synthetic, non-agent) engineering work yet.
