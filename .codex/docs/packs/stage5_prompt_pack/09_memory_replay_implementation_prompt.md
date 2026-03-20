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

# Implement only: `src/gdc_adk/memory/replay.py`

## Owning subsystem
- `memory`

## Responsibility
Export replay packages, validate replay packages, and rehydrate them into stable contract-shaped structures suitable for future replacement and migration.

## Required public functions
- `build_replay_package(scope_spec) -> dict`
- `validate_replay_package(replay_package) -> dict`
- `rehydrate_replay_package(replay_package) -> dict`
- `export_replay_package(scope_spec) -> dict`

## Required replay package fields
- `replay_package_id`
- `schema_version`
- `exported_at`
- `workflow_run_ids`
- `snapshot_ids`
- `context_block_ids`
- `artifact_summary_refs`
- `issue_evidence_refs`
- `export_source`
- optional `integrity_metadata`

## Rehydration semantics
- successful full rehydration must reconstruct stable serializable structures
- partial rehydration must declare all gaps explicitly
- invalid replay package must fail explicitly

## Requirements
- export must cover continuity snapshots, context blocks, issue-linked evidence references, and artifact summaries or chunk references
- replay packages must be migration-friendly
- replay must not depend on hidden runtime-only object references
- schema/version metadata must be explicit
- design must remain interface-first and implementation-second

## Inputs
- scope specification such as workflow, time window, or artifact scope
- replay package object

## Outputs
- replay package
- replay package validation result
- rehydrated result with explicit status

## Must not contain
- Stage 6 handoff orchestration
- provider execution
- workflow policy ownership
- opaque export formats with no stable contract boundary

## Definition of done
- replay packages can be exported, validated, and rehydrated into stable serializable structures
- current operational memory remains replaceable later by Coherence-Base-compatible infrastructure
