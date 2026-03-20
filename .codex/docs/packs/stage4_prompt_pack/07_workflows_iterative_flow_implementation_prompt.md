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

# Implement only: `src/gdc_adk/workflows/iterative_flow.py`

## Owning subsystem
- `workflows`

## Responsibility
Implement bounded iterative refinement with revision lineage, preserved findings, and structured revision deltas.

## Required public functions
- `start_iterative_flow(workflow_run, input_artifact_ids) -> dict`
- `plan_iteration(workflow_run, plan_reason) -> dict`
- `record_revision_delta(workflow_run, prior_artifact_id, revised_artifact_id, revision_reason, related_finding_ids) -> dict`
- `attach_prior_findings(workflow_run, finding_ids) -> dict`
- `advance_iteration(workflow_run, next_state, reason) -> dict`
- `complete_iteration(workflow_run, completion_reason) -> dict`
- `reopen_iteration(workflow_run, reopen_reason) -> dict`

## Required revision-delta fields
- `prior_artifact_id`
- `revised_artifact_id`
- `revision_reason`
- `related_finding_ids`
- `delta_recorded_at`
- `carry_forward_finding_ids`
- `resolved_finding_ids`

## Requirements
- prior artifact lineage must be preserved
- prior findings must remain attached or referenceable across passes
- revision overwrite with no lineage is invalid
- Stage 4 may preserve continuity requirements only; it must not implement Stage 5 continuity storage
- completion of non-trivial reviewable outputs must be gateable on validation outputs

## Must not contain
- continuity backend implementation
- provider routing
- hidden prompt-only iteration state
- destructive overwrite of prior artifact lineage

## Definition of done
- iterative refinement preserves prior artifacts, findings, and structured deltas
- reopen and revise behavior are explicit
