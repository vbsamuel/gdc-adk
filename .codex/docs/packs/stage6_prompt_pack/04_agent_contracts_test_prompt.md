# Tests only: `src/gdc_adk/workflows/agent_contracts.py`

## Required assertions
- valid handoff artifact can be created
- handoff artifact includes all required fields
- handoff artifact is serializable
- missing workflow_run_id rejects explicitly
- missing from_role or to_role rejects explicitly
- missing durable reference fields rejects explicitly where required
- raw free-form hidden state is not accepted as a handoff substitute
