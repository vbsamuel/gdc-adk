# Integration Prompt C — context migration

Implement only the integration tests for:
- `memory/context_store.py`
- `memory/replay.py`

## Required assertions
- context blocks retain source linkage through export
- exported context can be rehydrated into stable structures
- superseded context blocks remain traceable
- migration-friendly context does not depend on one in-memory-only implementation
