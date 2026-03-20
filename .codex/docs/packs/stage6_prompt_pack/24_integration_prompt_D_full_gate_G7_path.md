# Integration Prompt D — Gate G7 path

Implement only the integration tests for:
- `workflows/agent_roles.py`
- `workflows/agent_contracts.py`
- `workflows/handoff_manager.py`
- `workflows/delegation_engine.py`
- `workflows/review_orchestrator.py`
- `validation/agent_governance.py`
- `validation/handoff_validator.py`
- `substrate/agent_trace.py`

## Required assertions
- planner/executor/reviewer chain exchanges typed handoff artifacts
- bounded role contracts are enforced
- no hidden state is required between agents
- no free-form unbounded loop is allowed
- review/validation/governance cannot be bypassed
- full agent chain is traceable
