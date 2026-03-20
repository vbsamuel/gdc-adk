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

# Implement only: `src/gdc_adk/validation/traceability_auditor.py`

## Owning subsystem
- `validation`

## Responsibility
Audit requirement coverage and evidence completeness against the traceability matrix and emit structured traceability-gap findings.

## Required public functions
- `audit_traceability(subject, requirement_ids) -> dict`
- `check_requirement_coverage(requirement_id, evidence_bundle) -> dict`
- `build_traceability_gap_finding(requirement_id, gap_description, related_artifact_ids) -> dict`

## Requirements
- must check row completeness against matrix schema
- must detect missing acceptance evidence
- must detect missing observability evidence
- must link findings to requirement IDs
- must emit structured findings, not prose notes

## Must not contain
- generation of the primary artifact
- provider execution
- memory implementation
- plain checklist comments without findings

## Definition of done
- requirement coverage gaps become structured findings linked to requirement IDs
