# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 1 only.

Treat the uploaded markdown grounding files as binding architecture, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the owned contracts
3. identify the workflow modes structurally affected
4. identify the Stage 1 traceability rows advanced
5. identify the acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand beyond Stage 1
- Do not reference future stages as implemented behavior
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not modify unrelated files
- Do not put logic in adapters or labs
- Do not add provider routing, provider execution, ingestion, workflow engine sequencing, validation subsystem behavior, or memory backend behavior

Output implementation-grade Python code only for the requested file.
Respect repo constitution, naming rules, controlled enums, serializability, replayability, and exact public API requirements.
```

# Implement only: `src/gdc_adk/substrate/versioning.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- version chain and supersession metadata for artifacts

## Required public functions
- `create_version_record(artifact_id: str, version_number: int, parent_version: int | None) -> dict`
- `get_version_history(artifact_id: str) -> list[dict]`
- `mark_artifact_superseded(artifact_id: str, superseded_by_artifact_id: str) -> dict`

## Requirements
- storage may be in-memory
- version order must be preserved
- duplicate version number for same artifact lineage must reject
- superseding an artifact with itself must reject
- versioning must preserve prior history
- `mark_artifact_superseded` must not delete prior records

## Must not contain
- artifact content storage ownership
- workflow logic
- provider logic

## Definition of done
- version history is explicit
- supersession is explicit
- prior versions remain addressable
