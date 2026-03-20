# Forge-X Stage 4 Operator Runbook

## Purpose
This runbook gives the exact execution order for the full Stage 4 workflow/review scope and its matching test slices.

## Exact implementation order
1. `01_workflows_engine_implementation_prompt.md`
2. `02_workflows_engine_test_prompt.md`
3. `03_workflows_state_machine_implementation_prompt.md`
4. `04_workflows_state_machine_test_prompt.md`
5. `05_workflows_fix_flow_implementation_prompt.md`
6. `06_workflows_fix_flow_test_prompt.md`
7. `07_workflows_iterative_flow_implementation_prompt.md`
8. `08_workflows_iterative_flow_test_prompt.md`
9. `09_validation_validator_implementation_prompt.md`
10. `10_validation_validator_test_prompt.md`
11. `11_validation_drift_checker_implementation_prompt.md`
12. `12_validation_drift_checker_test_prompt.md`
13. `13_validation_traceability_auditor_implementation_prompt.md`
14. `14_validation_traceability_auditor_test_prompt.md`
15. `15_validation_grounding_checker_implementation_prompt.md`
16. `16_validation_grounding_checker_test_prompt.md`
17. `21_integration_prompt_A_state_machine_engine.md`
18. `22_integration_prompt_B_fix_flow_issue_verification.md`
19. `23_integration_prompt_C_iterative_lineage_findings.md`
20. `24_integration_prompt_D_validation_spine.md`
21. `25_STAGE4_acceptance_review.md`
22. `26_traceability_update_prompt.md`

## Stop conditions after each implementation prompt
Do not proceed to the test prompt until:
- only the requested file was changed
- no Stage 5 or Stage 6 behavior was added
- workflows are not reduced to prose-only state
- review is not plain comments
- independent findings are preserved for non-trivial validation
- reopen, verification, and closure semantics are explicit where required
- the public API matches the prompt exactly

## Stop conditions after each test prompt
Do not proceed until:
- all required assertions exist
- negative-path coverage exists
- tests are bounded to the named file or integration slice
- no tests depend on Stage 5 or Stage 6 implementation

## Hard rejection rules
Reject output if it:
- hides workflow state in prompt text or comments
- omits issue linkage in fix-flow
- omits revision lineage in iterative flow
- omits finding lifecycle
- performs non-trivial validation as the same exact generation path without independent findings
- omits reopen, verification, or closure semantics
- pulls in Stage 5 continuity backend implementation
- pulls in Stage 6 orchestration behavior
- hides logic in adapters or labs

## Expected outputs by phase
### After engine + state machine
- explicit allowed transitions exist
- engine uses structured state progression

### After fix-flow + iterative-flow
- issue/workflow/evidence linkage is explicit
- revision delta and prior findings are preserved

### After validation files
- independent structured findings exist
- drift, traceability, and grounding failures become findings
- finding lifecycle is explicit

### After integrations
- Scenario C, D, and E evidence exists in bounded Stage 4 form
- traceability rows FX-R008, FX-R009, FX-R011, FX-R012, and partial FX-R015 can be updated honestly
