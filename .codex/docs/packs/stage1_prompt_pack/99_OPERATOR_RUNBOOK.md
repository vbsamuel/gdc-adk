# Forge-X Stage 1 Operator Runbook

## Purpose
This runbook tells the operator exactly which prompt to paste, in what order, and what must be true before moving to the next prompt.

## Execution order
1. `01_core_state_implementation_prompt.md`
2. `02_core_state_test_prompt.md`
3. `03_core_contracts_implementation_prompt.md`
4. `04_core_contracts_test_prompt.md`
5. `05_event_spine_implementation_prompt.md`
6. `06_event_spine_test_prompt.md`
7. `07_artifact_store_implementation_prompt.md`
8. `08_artifact_store_test_prompt.md`
9. `09_issue_tracker_implementation_prompt.md`
10. `10_issue_tracker_test_prompt.md`
11. `11_provenance_implementation_prompt.md`
12. `12_provenance_test_prompt.md`
13. `13_versioning_implementation_prompt.md`
14. `14_versioning_test_prompt.md`
15. `15_dispatch_system_implementation_prompt.md`
16. `16_dispatch_system_test_prompt.md`
17. `17_integration_prompt_A_dispatch_artifacts_events.md`
18. `18_integration_prompt_B_fix_flow_issue_lifecycle.md`
19. `19_integration_prompt_C_revision_provenance_versioning.md`
20. `20_G1_substrate_acceptance_review.md`
21. `21_traceability_update_prompt.md`

## Stop conditions after each file implementation
Do not proceed to the matching test prompt until:
- only the requested file was changed
- no unrelated architecture was introduced
- no provider logic was added
- no Stage 2+ behavior was added
- public API matches the file prompt exactly

## Stop conditions after each test slice
Do not proceed until:
- all required assertions exist
- tests are bounded to the requested file or integration slice
- negative-path tests are present
- there are no tests relying on provider calls or future stages

## Hard rejection rules
Reject output if it:
- modifies unrelated files
- introduces provider routing or execution
- adds ingestion, workflow engine, validation subsystem, or memory backend behavior
- invents alternate enum values
- places logic in adapters or labs
- uses placeholders instead of real bounded implementation
- overwrites lineage/history

## Expected outputs by phase
### After state/contracts
- centralized enums
- stable typed contracts
- explicit validators

### After substrate primitives
- append-only events
- artifact store with lineage
- issue tracker with reopen support
- provenance and version history support

### After dispatch
- generic request -> single_run structured entry
- fix-like request -> fix_flow structured entry + issue

### After integration + G1
- Stage 1 substrate evidence exists for artifacts, events, issues, and workflow entry
