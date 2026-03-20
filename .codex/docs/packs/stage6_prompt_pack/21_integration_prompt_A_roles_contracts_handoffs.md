# Integration Prompt A — roles + contracts + handoffs

Implement only the integration tests for:
- `workflows/agent_roles.py`
- `workflows/agent_contracts.py`
- `workflows/handoff_manager.py`

## Required assertions
- only allowed roles can participate in handoffs
- typed handoff artifact is required for handoff
- invalid role target rejects explicitly
- handoff preserves workflow/artifact linkage
- handoff updates remain traceable
