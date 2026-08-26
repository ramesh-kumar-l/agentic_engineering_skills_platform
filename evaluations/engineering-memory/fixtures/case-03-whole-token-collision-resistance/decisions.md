# Decisions

## ADR-014: `refactoring-safety` reuses ADR-010's required-composition pattern a fourth time, plus a new per-target risk-tier + independent test-coverage signal
Combines a per-target risk tier with an independently computed
test-coverage signal, so a risky change to a poorly-covered target is
never treated the same as a risky change to a well-covered one.
