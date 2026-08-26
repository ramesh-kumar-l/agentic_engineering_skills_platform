# 02 — Requirements

Current, living requirements. Expected to grow every phase — this is Phase 0's
minimal starting set, not a target spec.

## Functional requirements

- FR1: Every skill must be expressible in the portable `SKILL.md` contract
  ([[04-skill-contract]]).
- FR2: Every skill must ship with evaluation cases before being called "evaluated"
  ([[05-evaluation-framework]]).
- FR3: Every skill must expose an explicit trust status, evidence, known failure
  modes, security classification, and provenance ([[06-security-model]]).
- FR4: High-risk actions (production changes, destructive operations, credentials,
  security controls, migrations, publishing, external comms) require an explicit
  human checkpoint before execution.
- FR5: Agents operating under a skill must distinguish OBSERVED / INFERRED /
  ASSUMED / UNKNOWN and never silently promote an inference to a fact.

## Non-functional requirements

- NFR1: Portability — skills must not assume a single vendor/runtime beyond what
  is currently unavoidable; avoid unnecessary lock-in.
- NFR2: Minimum sufficient context — do not default to dumping the whole
  repository into an agent; context is an engineered object.
- NFR3: Auditability — security-relevant actions must be traceable
  (classify → minimize → sanitize → authorize → execute → audit).
- NFR4: No unsupported reliability claims anywhere in skill docs, UI, or marketing
  copy (no "100% reliable" or equivalent).
- NFR5: Token-efficiency — the memory bank, not full repo/source reads, is the
  primary context mechanism for future work sessions.

## Out of scope for now

- Multi-model runtime support beyond what's needed to prove portability in
  principle (no premature GPT/Gemini/Cline integration work).
- Any hosted/SaaS surface.
- Enterprise administration, multi-tenant permissions, billing.
- Engineering Memory implementation (design deferred — see Section 43 of the
  operating charter; will get its own memory file when actually built).
  Note (2026-08-26): the checked-in [[operating-charter]] contains no
  Section 43 — see [[12-known-limitations|L27]].
