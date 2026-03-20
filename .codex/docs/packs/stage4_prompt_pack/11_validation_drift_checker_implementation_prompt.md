# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 4 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 4 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 4
- Do not pull Stage 5 or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not reduce workflows to prose-only state
- Do not treat review as plain comments or chat notes
- Do not allow non-trivial validation to be performed by the same exact generation path without independent finding objects
- Do not omit reopen, verification, or closure semantics
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, workflow/validation boundaries, controlled vocabularies, serializability, replayability, explicit state transitions, independent findings, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/validation/drift_checker.py`

## Owning subsystem
- `validation`

## Responsibility
Detect constitution violations, hidden-state patterns, provider-policy drift, and lineage drift, and surface them as structured findings.

## Required public functions
- `check_constitution_drift(subject) -> list[dict]`
- `check_provider_policy_drift(subject) -> list[dict]`
- `check_hidden_state_drift(subject) -> list[dict]`
- `check_lineage_drift(subject) -> list[dict]`

## Requirements
- constitution violations must become findings
- provider-policy violations must become findings
- hidden-state prompt chaining must become findings
- revised artifact lineage loss must become findings
- outputs must be structured and serializable

## Must not contain
- direct repo rewrites
- policy mutation
- provider transport
- plain warning comments instead of findings

## Definition of done
- constitution/provider-policy/hidden-state/lineage failures become structured findings
