# Tests only: `src/gdc_adk/workflows/delegation_engine.py`

## Required assertions
- valid delegation succeeds only when role rules allow it
- invalid delegation target rejects explicitly
- self-escalation rejects explicitly
- max delegation depth is enforced
- max same-role repetition count is enforced
- unresolved handoff limit is enforced
- delegation remains within workflow_run scope
- delegation cannot bypass review/validation by design
