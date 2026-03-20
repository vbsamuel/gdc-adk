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

# Implement only: `src/gdc_adk/memory/continuity.py`

## Owning subsystem
- `memory`

## Responsibility
Create, retrieve, list, export, and rehydrate explicit continuity snapshots for resumable workflows.

## Required public functions
- `create_snapshot(snapshot_payload) -> dict`
- `get_snapshot(snapshot_id) -> dict | None`
- `list_snapshots_for_workflow(workflow_run_id) -> list[dict]`
- `export_snapshots(filter_spec=None) -> dict`
- `rehydrate_snapshot(snapshot_or_id) -> dict`
- `mark_snapshot_superseded(snapshot_id, superseded_by_id) -> dict`

## Required resumable continuity fields
A resumable continuity snapshot must preserve at minimum:
- `snapshot_id`
- `workflow_run_id`
- `workflow_mode`
- `current_state`
- `state_history_ref` or serializable state-history slice
- `artifact_ids`
- `issue_ids`
- `finding_ids`
- `context_refs`
- `pending_actions`
- optional `completion_reason`
- optional `blocked_reason`
- `created_at`
- optional `superseded_by`

## Rehydration semantics
You must define explicit outcomes for:
- `rehydration_status = success`
- `rehydration_status = partial`
- `rehydration_status = invalid`

Partial rehydration must declare missing references explicitly.
Invalid rehydration must fail explicitly.

## Requirements
- workflows that require continuity must not depend on prompt text or hidden runtime-only state
- snapshots must be serializable, replayable, and exportable
- iterative and reopen flows must be resumable from explicit continuity objects
- supersession/newer-snapshot linkage must be explicit where applicable

## Inputs
- snapshot payload
- workflow ID
- snapshot ID
- export filter

## Outputs
- stored snapshot
- retrieved snapshot
- snapshot list
- export bundle
- rehydrated continuity result with explicit status

## Must not contain
- workflow execution
- provider routing
- opaque runtime-only continuity
- Stage 6 orchestration semantics

## Definition of done
- resumable continuity snapshots exist as explicit portable objects
- rehydration status is explicit
- hidden continuity in prompt text or local variables is not required
