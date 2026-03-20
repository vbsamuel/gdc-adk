# Tests only: `src/gdc_adk/substrate/dispatch_system.py`

## Required assertions
- generic request dispatches to `single_run`
- explicit valid `workflow_hint` is respected
- invalid `workflow_hint` rejects explicitly
- fix-like request dispatches to `fix_flow`
- fix-like request creates an `Issue`
- request dispatch creates an `Artifact`
- request dispatch creates a `WorkflowRun`
- `emitted_event_ids` is non-empty
- emitted events include `request_received`
- emitted events include `artifact_created`
- emitted events include `workflow_started`
- emitted events include `workflow_transitioned`
- fix-like request emits `issue_created`
- `DispatchResult` is serializable
- dispatch never requires provider calls
