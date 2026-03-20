# Integration Prompt B — fix-flow dispatch + issue lifecycle

Implement only the integration tests for:
- `substrate/dispatch_system.py`
- `substrate/issue_tracker.py`
- `substrate/event_spine.py`
- `substrate/artifact_store.py`

## Required assertions
- fix-like request selects `fix_flow`
- fix-like request creates an artifact
- fix-like request creates an issue
- issue is linked to the request artifact
- `issue_created` event is recorded
- `workflow_run.issue_ids` includes the created issue ID
