# Tests only: `src/gdc_adk/core/contracts.py`

## Required assertions
- each contract can be instantiated with valid data
- `serialize_artifact` returns a dict
- `serialize_issue` returns a dict
- `serialize_workflow_run` returns a dict
- `serialize_event` returns a dict
- invalid issue status rejects
- invalid workflow mode rejects
- invalid event type rejects
- invalid artifact with missing required fields rejects
- invalid non-dict source or metadata rejects
- `parent_artifact_ids` are preserved
- `related_artifact_ids` are preserved
- `state_history` is preserved
