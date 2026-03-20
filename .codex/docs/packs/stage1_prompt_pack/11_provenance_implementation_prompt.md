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

# Implement only: `src/gdc_adk/substrate/provenance.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- source linkage and derivation metadata

## Required public functions
- `record_artifact_source(artifact_id: str, source: dict) -> dict`
- `record_artifact_derivation(artifact_id: str, parent_artifact_ids: list[str]) -> dict`
- `get_artifact_provenance(artifact_id: str) -> dict`

## Requirements
- storage may be in-memory
- provenance records must be serializable
- source metadata must be dict-shaped
- parent linkage must preserve explicit derivation references
- derivation links to nonexistent artifacts or nonexistent parents must fail explicitly

## Must not contain
- artifact storage ownership
- workflow logic
- provider logic

## Definition of done
- artifact source can be recorded and retrieved
- derivation lineage can be recorded and retrieved
