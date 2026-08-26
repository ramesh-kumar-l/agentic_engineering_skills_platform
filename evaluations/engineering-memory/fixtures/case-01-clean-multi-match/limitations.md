# Known Limitations

## L23: `target_resolver.py`'s substring-based caller identification produces a wildly inflated caller list for short, common module stems (FIXED 2026-08-26, mentor-review follow-up)
A bare substring containment check on a module name false-positives
whenever a short stem happens to appear inside an unrelated word. This is
the exact collision class a new resolver composing on codebase-intelligence
needs to avoid from day one, not discover via a fourth real dogfood run.
