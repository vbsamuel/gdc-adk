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

# Implement only: `src/gdc_adk/workflows/engine.py`

## Owning subsystem
- `workflows`

## Responsibility
Central workflow execution coordinator for Stage 4. This file advances structured workflow state using explicit state-machine rules, mode-specific flow modules, issue/finding linkage, and validation gates.

## Required public functions
- `start_workflow(workflow_run, activation_output) -> dict`
- `advance_workflow(workflow_run, next_state, reason, context) -> dict`
- `block_workflow(workflow_run, reason) -> dict`
- `complete_workflow(workflow_run, completion_reason) -> dict`
- `fail_workflow(workflow_run, failure_reason) -> dict`
- `reopen_workflow(workflow_run, reopen_reason) -> dict`
- `apply_validation_gate(workflow_run, validation_result) -> dict`

## Requirements
- all non-trivial workflow progress must be represented as explicit structured state transitions
- the engine must use `state_machine.py` rather than hidden branching
- the engine must preserve `WorkflowRun.issue_ids`, `finding_ids`, `input_artifact_ids`, and `output_artifact_ids`
- completion of non-trivial reviewable outputs must be gateable on validation/checker outputs
- iterative and fix-flow paths must remain mode-specific, not ad hoc

## Explicit continuity boundary
- Stage 4 may preserve continuity requirements and references only
- Stage 4 must not implement Stage 5 continuity snapshot storage, load, export, or replay backends

## Must not contain
- provider routing
- provider transport
- artifact persistence implementation
- memory backend implementation
- review comments in place of `ReviewFinding` objects
- adapter/lab business logic

## Definition of done
- engine coordinates workflow progression through explicit states
- validation gates can influence progression
- no workflow state exists only in prose
