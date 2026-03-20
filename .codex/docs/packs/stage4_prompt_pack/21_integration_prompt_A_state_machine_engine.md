# Integration Prompt A — state machine + engine

Implement only the integration tests for:
- `workflows/state_machine.py`
- `workflows/engine.py`

## Required assertions
- engine relies on state-machine validation for transitions
- invalid transitions are blocked
- valid transitions advance structured state
- blocked/failed/reopened states preserve reasons
- state history remains serializable and replay-friendly
