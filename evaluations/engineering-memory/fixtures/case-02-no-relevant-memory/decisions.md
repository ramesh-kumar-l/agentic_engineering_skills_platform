# Decisions

## ADR-008: Redact, not exclude, secrets found in diff content
A diff containing a real secret is redacted in place rather than dropped
entirely, so the surrounding review context is preserved while the
sensitive value itself never reaches the output report.
