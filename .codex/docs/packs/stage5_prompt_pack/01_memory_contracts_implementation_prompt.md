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

# Implement only: `src/gdc_adk/memory/contracts.py`

## Owning subsystem
- `memory`

## Responsibility
Define the explicit public memory interfaces and memory-facing typed shapes that keep the current operational memory layer replaceable.

## Required public interface objects
- `MemoryStore`
- `ContextStore`
- `ContinuityStore`

## Required public interface behavior

### `MemoryStore`
Must support at minimum:
- `put_result(key, payload, metadata) -> dict`
- `get_result(key) -> dict | None`
- `invalidate_result(key) -> dict`
- `export_results(filter_spec=None) -> dict`

### `ContextStore`
Must support at minimum:
- `put_context_block(context_block) -> dict`
- `get_context_block(context_block_id) -> dict | None`
- `list_context_blocks_by_artifact(artifact_id) -> list[dict]`
- `export_context_blocks(filter_spec=None) -> dict`

### `ContinuityStore`
Must support at minimum:
- `create_snapshot(snapshot_payload) -> dict`
- `get_snapshot(snapshot_id) -> dict | None`
- `list_snapshots_for_workflow(workflow_run_id) -> list[dict]`
- `export_snapshots(filter_spec=None) -> dict`
- `rehydrate_snapshot(snapshot_or_id) -> dict`

## Required boundary guarantees
- no interface may return opaque implementation-specific objects as the only usable form
- all interfaces must operate on serializable contract shapes
- all interfaces must remain storage-backend-agnostic
- memory contracts must not force downstream layers to know current implementation details

## Inputs
- artifact references
- issue references
- review finding references
- context block payloads
- continuity snapshot payloads
- bounded reusable result payloads

## Outputs
- serializable store/retrieval/export results
- stable contract-shaped payloads only

## Must not contain
- workflow sequencing
- provider routing
- artifact authoring
- hard-coupling to one future permanent memory backend
- hidden runtime-only object handles as the primary output form

## Definition of done
- explicit interface contracts exist
- contract behavior is serializable and replay-friendly at the boundary
- future Coherence-Base replacement is not blocked by the interface shape
