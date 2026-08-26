# Known Limitations

## L2: External dependency parsing is root-only, not recursive
Only the root-level dependency manifest is parsed; a transitive
dependency declared in a nested manifest is not discovered.
