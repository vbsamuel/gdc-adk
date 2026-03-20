# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 1 only.

Treat the uploaded markdown grounding files as binding architecture, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the owned contracts
3. identify the workflow modes structurally affected
4. identify the Stage 1 traceability rows advanced
5. identify the acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand beyond Stage 1
- Do not reference future stages as implemented behavior
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not modify unrelated files
- Do not put logic in adapters or labs
- Do not add provider routing, provider execution, ingestion, workflow engine sequencing, validation subsystem behavior, or memory backend behavior

Output implementation-grade Python code only for the requested file.
Respect repo constitution, naming rules, controlled enums, serializability, replayability, and exact public API requirements.
```

# Implement only: `src/gdc_adk/core/contracts.py`

## Owning subsystem
- `core`

## Owned responsibility
- canonical typed Stage 1 object contracts shared by substrate

## This file must define
- `Artifact`
- `Issue`
- `WorkflowRun`
- `ReviewFinding`
- `Emission`
- `ContinuitySnapshot`
- `Event`

## Required public functions
- `validate_artifact_record(artifact: Artifact) -> None`
- `validate_issue_record(issue: Issue) -> None`
- `validate_workflow_run_record(workflow_run: WorkflowRun) -> None`
- `validate_event_record(event: Event) -> None`
- `serialize_artifact(artifact: Artifact) -> dict`
- `serialize_issue(issue: Issue) -> dict`
- `serialize_workflow_run(workflow_run: WorkflowRun) -> dict`
- `serialize_event(event: Event) -> dict`

## Required Artifact fields
- `artifact_id: str`
- `artifact_kind: str`
- `content: str | None`
- `content_ref: str | None`
- `source: dict`
- `metadata: dict`
- `created_at: str`
- `parent_artifact_ids: list[str]`
- `workflow_run_id: str | None`
- `issue_ids: list[str]`

## Required Issue fields
- `issue_id: str`
- `issue_type: str`
- `title: str`
- `description: str`
- `severity: str`
- `status: str`
- `related_artifact_ids: list[str]`
- `related_finding_ids: list[str]`
- `created_at: str`
- `updated_at: str`
- `reopen_count: int`

## Required WorkflowRun fields
- `workflow_run_id: str`
- `workflow_mode: str`
- `current_state: str`
- `input_artifact_ids: list[str]`
- `output_artifact_ids: list[str]`
- `issue_ids: list[str]`
- `finding_ids: list[str]`
- `created_at: str`
- `updated_at: str`
- `state_history: list[dict]`

## Required Event fields
- `event_id: str`
- `event_type: str`
- `created_at: str`
- `correlation_id: str`
- `workflow_run_id: str | None`
- `payload: dict`

## ReviewFinding minimum support
- `finding_id`
- `severity`
- `description`
- `related_artifact_ids`
- `status`
- `created_at`

## Emission minimum support
- `emission_id`
- `emission_type`
- `payload`
- `target`
- `created_at`

## ContinuitySnapshot minimum support
- `snapshot_id`
- `workflow_run_id`
- `artifact_ids`
- `issue_ids`
- `created_at`

Use canonical validators from `core/state.py` where applicable.

## Must enforce
- typed, serializable, stable contracts
- explicit validation failures
- no hidden defaults that erase required field failures

## Must not contain
- storage logic
- provider references
- workflow sequencing
- config loading

## Negative-path requirements
- reject invalid enum/state values
- reject malformed structures
- reject non-serializable payloads
- reject invalid artifact payload absence when both `content` and `content_ref` are missing where material content is required
