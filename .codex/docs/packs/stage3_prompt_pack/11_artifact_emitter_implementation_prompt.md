# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 3 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 3 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 3
- Do not pull Stage 4, Stage 5, or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not bypass canonicalization by sending raw user text directly into providers
- Do not treat indexing as optional
- Do not collapse emitted outputs into plain chat text only
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, import-direction rules, substrate contracts, information-plane ownership, controlled vocabularies, serializability, replayability, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/information_plane/egress/artifact_emitter.py`

## Owning subsystem
- `information_plane`

## Responsibility
Emit structured output artifacts and response envelopes. Egress must preserve provenance and artifact identity and must not collapse emitted outputs into plain chat text only.

## Required public functions
- `emit_direct_answer(emission_input) -> dict`
- `emit_generated_artifact(emission_input) -> dict`
- `emit_issue_update(emission_input) -> dict`
- `emit_workflow_status(emission_input) -> dict`
- `emit_review_packet(emission_input) -> dict`
- `emit_handoff_package(emission_input) -> dict`

## Required emission fields
- `emission_id`
- `emission_type`
- `artifact_ids`
- `workflow_run_id` if applicable
- `provenance_notes`
- `created_at`
- structured `payload`

## Required emission classes
- direct answer
- generated artifact
- review packet
- issue update
- workflow status
- package or handoff artifact

## Requirements
- egress must preserve provenance
- egress must preserve artifact identity
- egress must preserve workflow linkage where applicable
- emission must be replay-friendly and serializable
- emitted outputs must not degrade into plain text only

## Must not contain
- provider routing
- workflow execution
- review logic ownership
- adapter/lab output shortcuts that bypass structured emission

## Definition of done
- every emitted result is structured, artifact-linked, provenance-preserving, and replay-friendly
