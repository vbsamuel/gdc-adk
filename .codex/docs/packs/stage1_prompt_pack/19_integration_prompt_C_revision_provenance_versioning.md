# Integration Prompt C — revision + provenance + versioning

Implement only the integration tests for:
- `substrate/artifact_store.py`
- `substrate/provenance.py`
- `substrate/versioning.py`

## Required assertions
- revised artifact creates a new artifact ID
- revised artifact preserves parent linkage
- provenance derivation is retrievable
- version history is retrievable
- prior artifact remains addressable
- supersession linkage is explicit if recorded
