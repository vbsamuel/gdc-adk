# Tests only: `src/gdc_adk/substrate/artifact_store.py`

## Required assertions
- `create_artifact` stores a valid artifact
- `get_artifact` returns the stored artifact
- `list_artifacts` returns created artifacts
- `list_artifacts_by_workflow_run_id` filters correctly
- `list_artifacts_by_issue_id` filters correctly
- duplicate `artifact_id` rejects
- invalid artifact rejects before storage
- `link_parent_artifacts` preserves `parent_artifact_ids`
- `create_artifact_revision` creates a new artifact identity
- prior artifact remains retrievable after revision
