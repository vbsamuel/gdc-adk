# Integration Prompt A — contracts to stores

Implement only the integration tests for:
- `memory/contracts.py`
- `memory/cache.py`
- `memory/context_store.py`
- `memory/continuity.py`

## Required assertions
- store implementations can satisfy the declared interfaces
- serializable payloads flow through interface boundaries
- context and continuity objects remain exportable
- no interface requires opaque implementation-specific objects
