# Tests only: `src/gdc_adk/workflows/engine.py`

## Required assertions
- `start_workflow` records an explicit initial transition
- `advance_workflow` uses allowed transitions only
- `block_workflow` records blocked state with reason
- `complete_workflow` records completion with reason
- `fail_workflow` records failed state with reason
- `reopen_workflow` records reopened state with reason
- `apply_validation_gate` can prevent invalid completion for non-trivial reviewable outputs
- issue IDs and finding IDs are preserved across transitions
- state history remains serializable
- this file does not implement provider routing or memory backend logic
