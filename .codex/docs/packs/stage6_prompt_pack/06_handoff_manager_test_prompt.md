# Tests only: `src/gdc_adk/workflows/handoff_manager.py`

## Required assertions
- valid handoff can be initiated
- valid handoff can be completed only after validation
- rejection path preserves reason
- owner_role and pending_actions can be updated traceably
- handoff does not require inventing new workflow states
- handoff preserves artifact/issue/finding linkage
- invalid handoff rejects explicitly
