# Forge-X Stage 2 Operator Runbook

## Purpose
This runbook provides the exact execution sequence for the bounded eight-file Stage 2 operator slice and its matching test slices.

## Exact implementation order
1. `01_config_settings_implementation_prompt.md`
2. `11_config_settings_test_prompt.md`

3. `02_control_plane_policy_implementation_prompt.md`
4. `12_control_plane_policy_test_prompt.md`

5. `03_control_plane_router_implementation_prompt.md`
6. `13_control_plane_router_test_prompt.md`

7. `04_runtime_local_model_manager_implementation_prompt.md`
8. `14_runtime_local_model_manager_test_prompt.md`

9. `05_providers_base_implementation_prompt.md`
10. `15_providers_base_test_prompt.md`

11. `06_providers_ollama_provider_implementation_prompt.md`
12. `16_providers_ollama_provider_test_prompt.md`

13. `07_providers_google_provider_implementation_prompt.md`
14. `17_providers_google_provider_test_prompt.md`

15. `08_providers_router_implementation_prompt.md`
16. `18_providers_router_test_prompt.md`

17. `21_integration_prompt_A_policy_router_local_path.md`
18. `22_integration_prompt_B_provider_contract_and_failover.md`
19. `23_integration_prompt_C_config_to_router_wiring.md`
20. `24_G3_acceptance_review.md`
21. `25_traceability_update_prompt.md`

## Stop conditions after each implementation prompt
Do not proceed to the test prompt until:
- only the requested file was changed
- no later-stage behavior was added
- no policy was hidden in providers
- no routing or business logic was hidden in adapters or labs
- the public API matches the prompt exactly

## Stop conditions after each test prompt
Do not proceed until:
- all required assertions exist
- negative-path coverage exists
- tests are bounded to the named file or integration slice
- no tests depend on Stage 3+ behavior

## Hard rejection rules
Reject output if it:
- modifies unrelated files
- introduces cloud-first routing
- skips deterministic-before-LLM decisioning
- lets providers choose themselves
- drops failover errors
- overclaims runtime responsibilities beyond the bounded surface
- introduces cache execution as a Stage 2 routing step
- pulls in Stage 3, 4, 5, or 6 responsibilities

## Expected outputs by phase
### After config + policy + router
- repo-root config access is stable
- deterministic, local, and cloud decisions are explicit
- provider chain is local-first and policy-controlled

### After runtime + provider contracts
- local model lifecycle surface is explicit
- provider request/response normalization exists
- local and cloud adapters are bounded and thin

### After providers router + integrations
- failover chain executes exactly in control-plane order
- failure chain is preserved
- G3 evidence is available for the operator slice

## Note on deterministic capability rows
This operator slice is bounded to the eight-file execution core. Deterministic geo/time/weather capability files are not implemented in this pack and must be handled in the separate capability slice if full FX-R004 and FX-R005 closure is required.
