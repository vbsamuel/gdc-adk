# Tests only: `src/gdc_adk/substrate/event_spine.py`

## Required assertions
- `record_event` appends a valid event
- `get_event` returns the stored event
- `list_events` preserves append order
- `list_events_by_correlation_id` filters correctly
- `list_events_by_workflow_run_id` filters correctly
- `list_events_by_event_type` filters correctly
- duplicate `event_id` rejects
- invalid event type rejects
- non-serializable payload rejects
- silent failure is not allowed
