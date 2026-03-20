# Integration Prompt C — iterative lineage + findings

Implement only the integration tests for:
- `workflows/engine.py`
- `workflows/iterative_flow.py`
- `validation/validator.py`

## Required assertions
- prior artifact lineage is preserved across revisions
- revision delta is recorded structurally
- prior findings remain addressable across passes
- iterative reopen path preserves history
- non-trivial completion can be gated on validation output
