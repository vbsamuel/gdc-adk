# Forge-X Stage 3 Operator Runbook

## Purpose
This runbook gives the exact execution order for the full Stage 3 information-plane scope and its matching test slices.

## Exact implementation order
1. `01_document_ingestor_implementation_prompt.md`
2. `02_document_ingestor_test_prompt.md`
3. `03_canonicalizer_implementation_prompt.md`
4. `04_canonicalizer_test_prompt.md`
5. `05_artifact_index_implementation_prompt.md`
6. `06_artifact_index_test_prompt.md`
7. `07_trigger_router_implementation_prompt.md`
8. `08_trigger_router_test_prompt.md`
9. `09_workflow_activation_implementation_prompt.md`
10. `10_workflow_activation_test_prompt.md`
11. `11_artifact_emitter_implementation_prompt.md`
12. `12_artifact_emitter_test_prompt.md`
13. `21_integration_prompt_A_ingest_normalize_artifactize_index.md`
14. `22_integration_prompt_B_trigger_and_activation_output.md`
15. `23_integration_prompt_C_structured_egress.md`
16. `24_STAGE3_acceptance_review.md`
17. `25_traceability_update_prompt.md`

## Stop conditions after each implementation prompt
Do not proceed to the test prompt until:
- only the requested file was changed
- no Stage 4, Stage 5, or Stage 6 behavior was added
- no raw input bypasses canonicalization
- no provider call was added in the information plane
- the public API matches the prompt exactly

## Stop conditions after each test prompt
Do not proceed until:
- all required assertions exist
- negative-path coverage exists
- tests are bounded to the named file or integration slice
- no tests depend on Stage 4, Stage 5, or Stage 6 behavior

## Hard rejection rules
Reject output if it:
- sends raw text directly to providers
- skips canonicalization
- treats indexing as optional
- collapses emitted output into plain chat text only
- executes workflows inside activation
- introduces validation ownership into information plane
- introduces memory backend behavior into Stage 3
- hides logic in adapters or labs

## Expected outputs by phase
### After ingestion + normalization
- raw-signal objects are explicit
- normalized-signal objects include all required canonical fields
- source attribution and provenance are preserved

### After indexing
- required searchable structures exist
- indexing cannot be skipped

### After activation
- activation category, candidate workflow mode, issue trigger, and next actions are structured
- no workflow execution occurs

### After egress
- emissions are structured and provenance-preserving
- artifact identity is preserved
- plain-text-only collapse is prevented
