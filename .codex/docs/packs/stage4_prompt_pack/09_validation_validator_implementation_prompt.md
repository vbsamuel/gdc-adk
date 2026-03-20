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

# Implement only: `src/gdc_adk/validation/validator.py`

## Owning subsystem
- `validation`

## Responsibility
Central validation entry point that produces independent structured `ReviewFinding` objects for reviewable artifacts and workflow outputs.

## Required public functions
- `validate_artifact(artifact, workflow_context) -> dict`
- `validate_workflow_output(output_artifact, workflow_context) -> dict`
- `create_validation_finding(finding_type, severity, description, related_artifact_ids, evidence, reviewer_identity) -> dict`
- `transition_finding_status(finding, next_status, reason) -> dict`
- `resolve_validation_finding(finding, resolution_reason) -> dict`
- `reopen_validation_finding(finding, reopen_reason) -> dict`

## Required ReviewFinding lifecycle
You must support an explicit finding lifecycle with at minimum:
- `open`
- `accepted`
- `rejected`
- `resolved`
- `reopened`

## Lifecycle rules
- all findings must preserve evidence and artifact linkage
- reopening a finding must preserve prior lifecycle history
- finding-to-issue escalation must be representable
- non-trivial validation must not be the same exact generation path as authoring
- validation output must be separate from the authored artifact and must produce independent finding objects

## Must not contain
- authoring of the primary artifact under review
- provider routing
- workflow policy mutation
- plain comments as substitute for findings

## Definition of done
- reviewable artifacts can produce independent structured findings
- finding lifecycle transitions are explicit and serializable
