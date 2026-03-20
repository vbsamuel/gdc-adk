# Integration Prompt A — dispatch + artifacts + events

Implement only the integration tests for:
- `substrate/dispatch_system.py`
- `substrate/artifact_store.py`
- `substrate/event_spine.py`

## Required assertions
- dispatching a generic request creates exactly one request artifact
- dispatching a generic request creates exactly one workflow_run
- `request_received` event is recorded
- `artifact_created` event is recorded
- `workflow_started` event is recorded
- `workflow_transitioned` event is recorded
- artifact is retrievable by ID after dispatch
- events are retrievable by `correlation_id`
