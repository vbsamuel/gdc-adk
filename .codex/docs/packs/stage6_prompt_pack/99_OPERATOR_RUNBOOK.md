# Forge-X Stage 6 Operator Runbook

## Purpose
This runbook gives the exact execution order for the full Stage 6 multi-agent scope and its matching test slices.

## Exact implementation order
1. `01_agent_roles_implementation_prompt.md`
2. `02_agent_roles_test_prompt.md`
3. `03_agent_contracts_implementation_prompt.md`
4. `04_agent_contracts_test_prompt.md`
5. `05_handoff_manager_implementation_prompt.md`
6. `06_handoff_manager_test_prompt.md`
7. `07_delegation_engine_implementation_prompt.md`
8. `08_delegation_engine_test_prompt.md`
9. `09_review_orchestrator_implementation_prompt.md`
10. `10_review_orchestrator_test_prompt.md`
11. `11_agent_governance_implementation_prompt.md`
12. `12_agent_governance_test_prompt.md`
13. `13_handoff_validator_implementation_prompt.md`
14. `14_handoff_validator_test_prompt.md`
15. `15_agent_trace_implementation_prompt.md`
16. `16_agent_trace_test_prompt.md`
17. `21_integration_prompt_A_roles_contracts_handoffs.md`
18. `22_integration_prompt_B_delegation_governance.md`
19. `23_integration_prompt_C_review_validation.md`
20. `24_integration_prompt_D_full_gate_G7_path.md`
21. `25_STAGE6_acceptance_review.md`
22. `26_traceability_update_prompt.md`

## Stop conditions after each implementation prompt
Do not proceed to the test prompt until:
- only the requested file was changed
- no earlier-stage redesign was introduced except an explicitly referenced interface dependency
- no free-form swarm behavior was introduced
- no hidden agent-to-agent state exists outside durable artifacts, findings, issues, workflow state, or approved continuity structures
- no handoff occurs without typed contract and traceable lineage
- review/validation/governance cannot be bypassed
- the public API matches the prompt exactly

## Stop conditions after each test prompt
Do not proceed until:
- all required assertions exist
- negative-path coverage exists
- tests are bounded to the named file or integration slice
- no tests depend on unapproved traceability IDs

## Hard rejection rules
Reject output if it:
- allows free-form swarm behavior
- stores agent-to-agent state outside approved durable objects
- allows handoffs without typed contracts
- allows reviewer = author for non-trivial reviewable outputs
- allows bounded-delegation limits to be bypassed
- allows multi-agent flow to bypass review, validation, or governance
- invents canonical traceability IDs not present in the approved matrix
- hides logic in adapters or labs

## Expected outputs by phase
### After roles + contracts
- finite roles and bounded authority exist
- durable typed handoff artifacts exist

### After handoff + delegation
- typed handoffs and bounded delegation are enforceable
- no hidden coordination state is required

### After review + governance + validation
- independent review path is explicit
- anti-swarm controls are enforceable
- invalid handoffs are blocked

### After trace + integrations
- full agent chain is reconstructible
- Gate G7 evidence exists in bounded form
