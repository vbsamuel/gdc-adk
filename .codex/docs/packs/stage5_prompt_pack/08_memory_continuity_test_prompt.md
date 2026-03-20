# Tests only: `src/gdc_adk/memory/continuity.py`

## Required assertions
- valid snapshot can be created
- snapshot can be retrieved by ID
- snapshots can be listed for workflow
- snapshot export bundle is serializable
- supersession relationship can be recorded
- rehydration can return success when references are complete
- rehydration can return partial with declared missing references
- invalid rehydration fails explicitly
- snapshot includes required resumable fields
- design does not require hidden prompt text or runtime-local hidden variables
