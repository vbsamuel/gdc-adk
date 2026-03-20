# Traceability Update Prompt — Stage 4

Update only the Stage 4 rows advanced by the implementation evidence.

## Rows in scope
- `FX-R008`
- `FX-R009`
- `FX-R011`
- `FX-R012`
- partial `FX-R015`

## Explicit mapping to use
- `FX-R008` -> `workflows/fix_flow.py`, `workflows/engine.py`
- `FX-R009` -> `workflows/engine.py`, `workflows/state_machine.py`, `workflows/iterative_flow.py`, `workflows/fix_flow.py`
- `FX-R011` -> `validation/validator.py`, `validation/grounding_checker.py`
- `FX-R012` -> `workflows/engine.py`, `workflows/state_machine.py`
- partial `FX-R015` -> workflow transition events, finding events, lineage-preserving revisions, explicit state history; do not claim Stage 5 memory-backed replay complete

## Observability evidence to reference where applicable
- `workflow_started`
- `workflow_transitioned`
- `workflow_blocked`
- `workflow_completed`
- `workflow_failed`
- `workflow_reopened`
- `finding_created`
- `finding_resolved`
- `issue_status_changed`

## For each row provide
- owning_files
- contracts_involved
- workflow_modes_affected
- acceptance_tests passed
- observability evidence
- remaining gaps
- completion_status

## Rules
- do not mark Stage 5 or Stage 6 rows complete
- do not mark full-system acceptance complete
- use bounded Stage 4 evidence only
