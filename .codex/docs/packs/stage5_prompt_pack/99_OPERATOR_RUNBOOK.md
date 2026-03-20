# Forge-X Stage 5 Operator Runbook

## Purpose
This runbook gives the exact execution order for the full Stage 5 memory scope and its matching test slices.

## Exact implementation order
1. `01_memory_contracts_implementation_prompt.md`
2. `02_memory_contracts_test_prompt.md`
3. `03_memory_cache_implementation_prompt.md`
4. `04_memory_cache_test_prompt.md`
5. `05_memory_context_store_implementation_prompt.md`
6. `06_memory_context_store_test_prompt.md`
7. `07_memory_continuity_implementation_prompt.md`
8. `08_memory_continuity_test_prompt.md`
9. `09_memory_replay_implementation_prompt.md`
10. `10_memory_replay_test_prompt.md`
11. `21_integration_prompt_A_contracts_to_stores.md`
12. `22_integration_prompt_B_continuity_resume.md`
13. `23_integration_prompt_C_context_migration.md`
14. `24_integration_prompt_D_cache_bounds.md`
15. `25_STAGE5_acceptance_review.md`
16. `26_traceability_update_prompt.md`

## Stop conditions after each implementation prompt
Do not proceed to the test prompt until:
- only the requested file was changed
- no Stage 6 behavior was added
- no critical continuity is hidden in prompt text or runtime-local variables
- the public API matches the prompt exactly
- exportability and replayability boundaries are explicit

## Stop conditions after each test prompt
Do not proceed until:
- all required assertions exist
- negative-path coverage exists
- tests are bounded to the named file or integration slice
- no tests depend on Stage 6 implementation

## Hard rejection rules
Reject output if it:
- traps critical continuity only in prompt text
- traps critical continuity only in hidden runtime-local variables
- makes memory non-exportable or non-replayable
- binds design too tightly to current operational memory
- introduces Stage 6 orchestration behavior
- hides memory logic in adapters or labs

## Expected outputs by phase
### After contracts
- explicit memory interfaces exist
- boundaries are serializable and backend-agnostic

### After cache/context/continuity
- reusable results are bounded
- source-linked context is exportable
- continuity snapshots are resumable and explicit

### After replay
- replay packages can be exported, validated, and rehydrated
- replaceability guarantees are structurally supported
