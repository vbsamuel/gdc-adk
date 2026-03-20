# Tests only: `src/gdc_adk/workflows/review_orchestrator.py`

## Required assertions
- reviewer can be assigned explicitly
- reviewer role must differ from author/executor for non-trivial reviewable outputs
- review trigger can produce a traceable review path
- review findings can be recorded durably
- review path can support issue escalation from findings
- review does not collapse into plain comments/chat
