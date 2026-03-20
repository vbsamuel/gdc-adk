# Integration Prompt B — delegation + governance

Implement only the integration tests for:
- `workflows/delegation_engine.py`
- `validation/agent_governance.py`
- `substrate/agent_trace.py`

## Required assertions
- bounded delegation is enforced
- governance detects unbounded loops and limit violations
- agent trace can support governance evaluation
- stop conditions are enforceable
- hidden coordination carriers are not accepted
