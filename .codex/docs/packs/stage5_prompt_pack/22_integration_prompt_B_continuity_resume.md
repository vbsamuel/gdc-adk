# Integration Prompt B — continuity resume

Implement only the integration tests for:
- `memory/continuity.py`
- `memory/replay.py`

## Required assertions
- continuity snapshot can be exported
- exported snapshot can be rehydrated
- rehydration can declare success, partial, or invalid explicitly
- iterative/reopen-ready continuity fields are preserved
- no critical continuity depends on prompt text or hidden runtime variables
