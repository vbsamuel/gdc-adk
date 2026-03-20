# Tests only: `src/gdc_adk/substrate/agent_trace.py`

## Required assertions
- agent action can be recorded
- agent trace can be retrieved by workflow_run_id
- trace includes required fields
- trace preserves ordering by timestamp or durable append semantics
- trace can reconstruct multi-role chain
- trace output is serializable
- hidden prompt-only trace is not required
