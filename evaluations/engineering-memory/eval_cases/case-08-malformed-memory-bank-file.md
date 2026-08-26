# case-08-malformed-memory-bank-file

**Category**: corpus-drift

Both memory-bank files are plain prose with no `## ADR-NNN:` / `## LNN:`
headers — a stand-in for section-header format drift. The engine must
surface an explicit "no records parsed" warning rather than silently
returning an empty result indistinguishable from a genuine no-fit case.
