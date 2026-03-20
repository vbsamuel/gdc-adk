# Tests only: `src/gdc_adk/information_plane/activation/workflow_activation.py`

## Required assertions
- valid normalized-signal input plus artifact references produces structured activation output
- activation output includes `activation_category`
- activation output includes `candidate_workflow_mode`
- activation output includes `related_artifact_ids`
- activation output includes `issue_triggered`
- activation output includes `activation_reason`
- activation output includes `next_action_types`
- activation output includes `normalized_signal_id`
- invalid input rejects explicitly
- output is serializable
- this file does not execute workflows
