# case-04-fixed-record-flagged-stale

**Category**: staleness-fixed

A record whose title carries a real `(FIXED during Phase N)` suffix is
still returned (it is, after all, the highest-scoring match) but always
with `is_stale=True` and a reason naming the FIXED title — the direct
operational answer to A8's own named risk about stale memory being
treated as authoritative.
