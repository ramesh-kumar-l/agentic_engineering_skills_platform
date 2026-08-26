# Dependency / Supply Chain — real dogfood run

Real run against this repository's own root manifest — not a synthetic
fixture. See `project-memory-bank/03-architecture.md` for why every skill
in this portfolio is dogfooded against real, self-produced input in
addition to its synthetic evaluation fixtures.

## Command

```bash
cd skills/codebase-intelligence
python -m engine.cli ../.. --format json --out /tmp/ci-out

cd ../dependency-supply-chain
python -m engine.cli --ci-report /tmp/ci-out/report.json --format markdown
```

## Real output

```
# Dependency / Supply Chain Report

**Suggested risk level: NEEDS_REVIEW** — advisory only; a human/agent makes the real call (see SKILL.md).

## Surface area
- Total direct dependencies: 1
- Unpinned: 1 (100.0%)
  - requirements.txt: 1

## Flags (1)
- **[LOW] unpinned-version** — pytest: 'pytest' has a range version specifier ('>=7.0') — the exact resolved version is not reproducible between installs. (requirements.txt: '>=7.0')

## Dependencies (1)
- `pytest` >=7.0 [range] — requirements.txt
```

## What this actually found

Run against the whole platform repo's root, `codebase-intelligence` sees
exactly **one** declared dependency: `pytest>=7.0` from the root
`requirements.txt`. That's real, correct output — and it's also a live,
concrete demonstration of the exact scope limitation this skill's SKILL.md
and `12-known-limitations.md` disclose upfront: the ten skills'
**actual** runtime/dev dependencies live in `skills/*/pyproject.toml`, one
level down from repo root, which `codebase-intelligence`'s
`external_deps.py` does not recursively scan (L2). Running this skill
against `skills/release-readiness/` directly (rather than the repo root)
would surface that skill's own `pytest>=7.0` dev dependency the same way.

This is exactly the "zero (or near-zero) dependencies found" case
`SKILL.md`'s Known Limitations section warns about — a low count here is
not proof of a clean supply chain, it's a proof of where
`codebase-intelligence` looked. The one real flag found (`pytest`'s range
specifier) is genuine and actionable on its own: pinning it to an exact
version would make this repo's own CI runs fully reproducible.

## Honest assessment

This is a self-run, single-target pilot (same ADR-009 discipline as every
other dogfood run in this project) — not proof the skill generalizes to
other repos' manifest layouts, ecosystems, or dependency counts. It is,
however, real: the command above was actually run, against this actual
repository, and the output above is copied verbatim from that run, not
constructed to look plausible.
