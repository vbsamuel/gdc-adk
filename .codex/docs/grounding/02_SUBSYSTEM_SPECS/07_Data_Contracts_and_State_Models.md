# Data Contracts and State Models

## 1. Why contracts exist

Without stable contracts, Forge-X collapses into prompt-driven improvisation. Contracts are required so that workflows, memory, validation, and future Coherence-Base integration all converge on the same object shapes.

## 2. Artifact contract

Required fields:
- artifact_id
- artifact_kind
- content
- source
- metadata
- created_at

Recommended fields:
- parent_artifact_ids
- modality
- checksum or hash
- workflow_run_id
- issue_ids

## 3. Issue contract

Required fields:
- issue_id
- issue_type
- title
- description
- severity
- status
- related_artifact_ids
- created_at

Recommended fields:
- assignee_role
- finding_ids
- reopen_count
- resolution_summary
- blocked_reason

## 4. ContextBlock contract

Required fields:
- context_block_id
- block_type
- content
- source_artifact_ids
- created_at

Recommended fields:
- score
- tags
- validity_window
- superseded_by

## 5. WorkflowRun contract

Required fields:
- workflow_run_id
- workflow_mode
- current_state
- input_artifact_ids
- output_artifact_ids
- issue_ids
- created_at

Recommended fields:
- state_history
- pending_actions
- owner_role
- retry_count
- completion_reason

## 6. ReviewFinding contract

Required fields:
- finding_id
- severity
- description
- related_artifact_ids
- status
- created_at

Recommended fields:
- evidence
- issue_id
- finding_type
- reviewer_role

## 7. Emission contract

Required fields:
- emission_id
- emission_type
- payload
- target
- created_at

Recommended fields:
- artifact_ids
- issue_ids
- workflow_run_id
- provenance_notes
