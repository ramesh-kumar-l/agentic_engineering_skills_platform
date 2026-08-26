# Known Limitations

## L16: Action-classifier used a fixed-distance proximity window, which real phrasing exceeded (FIXED during Phase 5)
The action classifier only looked a fixed number of tokens away from a
verb when deciding whether it governed a named action; real phrasing
often placed the verb farther away than that fixed window allowed.
