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

# Implement only: `src/gdc_adk/memory/cache.py`

## Owning subsystem
- `memory`

## Responsibility
Provide a bounded operational cache for reusable computed results without trapping critical continuity in cache-only state.

## Required public functions
- `put_result(key, payload, metadata) -> dict`
- `get_result(key) -> dict | None`
- `invalidate_result(key) -> dict`
- `export_results(filter_spec=None) -> dict`

## Required cache record fields
- `cache_key`
- `payload`
- `metadata`
- `created_at`
- optional `expires_at`
- optional `invalidated_at`

## Requirements
- cache must be bounded and explicit
- cache hit and miss semantics must be attributable
- cache entries must be exportable in replay-friendly form
- invalidation or expiration behavior must be explicit
- cache must not become the sole residence of critical resumable state

## Inputs
- stable cache key
- bounded reusable payload
- metadata including task or workflow scope if available

## Outputs
- stored cache record
- retrieved cache record or explicit miss
- invalidation result
- export bundle of cache records

## Must not contain
- long-horizon continuity ownership
- workflow execution
- provider selection
- hidden reliance on one in-memory-only structure
- Stage 6 handoff logic

## Definition of done
- results can be stored, retrieved, invalidated, and exported
- cache-only state is non-critical
- cache records are replayable and migration-friendly
