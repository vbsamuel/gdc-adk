# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 5 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 5 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 5
- Do not pull Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not store critical continuity only in prompt text or runtime-local hidden variables
- Do not make memory implementation non-exportable or non-replayable
- Do not bind the design so tightly to current operational memory that future Coherence-Base replacement becomes impossible
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, memory ownership boundaries, stable contracts, replayability, exportability, rehydration semantics, and future Coherence-Base replaceability.
```

# Implement only: `src/gdc_adk/memory/context_store.py`

## Owning subsystem
- `memory`

## Responsibility
Store, retrieve, supersede, and export structured context blocks and grounding fragments with preserved source linkage.

## Required public functions
- `put_context_block(context_block) -> dict`
- `get_context_block(context_block_id) -> dict | None`
- `list_context_blocks_by_artifact(artifact_id) -> list[dict]`
- `mark_context_block_superseded(context_block_id, superseded_by_id) -> dict`
- `export_context_blocks(filter_spec=None) -> dict`

## Required ContextBlock-compatible fields
- `context_block_id`
- `block_type`
- `content`
- `source_artifact_ids`
- `created_at`
- optional `tags`
- optional `validity_window`
- optional `superseded_by`

## Requirements
- source linkage must be preserved
- context blocks must be exportable
- supersession must preserve prior traceability rather than erase it
- context must not collapse into hidden prompt snippets with no object identity
- retrieval must not depend on one in-memory-only implementation

## Inputs
- typed context block payloads
- artifact IDs
- filter spec for export

## Outputs
- stored context block
- retrieved context block
- context block lists
- supersession result
- export bundle

## Must not contain
- prompt-assembly policy
- workflow sequencing
- provider execution
- non-exportable implicit in-memory context only

## Definition of done
- source-linked context blocks can be stored, retrieved, superseded, and exported
- context remains migration-friendly and traceable
