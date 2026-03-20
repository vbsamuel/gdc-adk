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

# Implement only: `src/gdc_adk/substrate/artifact_store.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- artifact creation, retrieval, revision, and lineage support

Use the `Artifact` contract from `core/contracts.py`.

## Required public functions
- `create_artifact(artifact: Artifact) -> Artifact`
- `get_artifact(artifact_id: str) -> Artifact`
- `list_artifacts() -> list[Artifact]`
- `list_artifacts_by_workflow_run_id(workflow_run_id: str) -> list[Artifact]`
- `list_artifacts_by_issue_id(issue_id: str) -> list[Artifact]`
- `create_artifact_revision(artifact: Artifact) -> Artifact`
- `link_parent_artifacts(artifact_id: str, parent_artifact_ids: list[str]) -> Artifact`

## Supported artifact classes
- input artifact
- normalized artifact
- generated artifact
- evidence artifact
- emitted artifact

## Requirements
- initial storage may be in-memory
- duplicate `artifact_id` must reject
- `create_artifact_revision` must create a new artifact identity, not overwrite an existing artifact
- parent linkage must preserve lineage
- artifacts must be retrievable by stable ID
- artifacts must be queryable by `workflow_run_id` and `issue_id`

## Must not contain
- provider logic
- review logic
- workflow sequencing
- versioning ownership beyond artifact linkage

## Definition of done
- meaningful input can be stored as artifact
- derived artifact can link to parents
- revisions preserve prior artifacts
