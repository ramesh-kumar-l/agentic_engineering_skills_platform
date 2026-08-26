# Decisions

## ADR-010: `feature-planner` requires a `codebase-intelligence` report as a hard precondition, not optional context
Guessing at structure instead of resolving against a real codebase-intelligence
report would produce ungrounded output. This required-composition pattern
has since been reused across most of the portfolio.

## ADR-018: `engineering-knowledge-capture` reuses ADR-010's required-composition pattern an eighth time, builds its word-boundary resolver correct from day one
Applies the word-boundary check to `location_resolver.py`, avoiding
substring collisions when a module name is short. This is the first
resolver in the portfolio built correct from day one rather than shipped
with the bare-substring bug and fixed later.
