"""Test Strategy Engine (TEP Phase 5a).

Given a regression-hunter report (per-file risk signals for a staged diff)
and a project_intelligence TestEnvironmentProfile for the same repo, decides
which changed files need a regression test — reusing both engines' existing
signals rather than re-deriving risk or environment detection. See
project-memory-bank/18-test-engineering-platform-contract.md and
project-memory-bank/21-test-strategy-report-schema.md.
"""
