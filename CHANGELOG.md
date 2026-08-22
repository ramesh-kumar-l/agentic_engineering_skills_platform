# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

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

No skill has been used on real (non-synthetic) engineering work yet.
