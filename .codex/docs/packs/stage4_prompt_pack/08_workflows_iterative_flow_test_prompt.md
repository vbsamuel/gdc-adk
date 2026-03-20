# Tests only: `src/gdc_adk/workflows/iterative_flow.py`

## Required assertions
- iterative flow can start with explicit input artifacts
- revision delta records prior and revised artifact IDs
- related finding IDs are preserved in revision delta
- prior findings remain addressable across passes
- revision overwrite without lineage rejects explicitly
- reopen path exists and preserves history
- no Stage 5 continuity storage is implemented here
