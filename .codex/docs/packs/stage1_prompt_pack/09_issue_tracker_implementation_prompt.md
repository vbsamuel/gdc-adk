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

# Implement only: `src/gdc_adk/substrate/issue_tracker.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- durable typed issue lifecycle support for Stage 1

Use the `Issue` contract from `core/contracts.py`.

## Required public functions
- `create_issue(issue: Issue) -> Issue`
- `get_issue(issue_id: str) -> Issue`
- `list_issues() -> list[Issue]`
- `list_issues_by_artifact_id(artifact_id: str) -> list[Issue]`
- `update_issue_status(issue_id: str, new_status: str) -> Issue`
- `reopen_issue(issue_id: str) -> Issue`
- `link_issue_to_artifact(issue_id: str, artifact_id: str) -> Issue`

## Requirements
- duplicate `issue_id` must reject
- issue status must use controlled vocabulary
- resolved is not the same as closed
- reopen preserves history
- reopen increments `reopen_count`
- issues created from fix-like requests must support artifact linkage

## Must not contain
- workflow sequencing
- provider logic
- validation subsystem logic

## Definition of done
- fix-flow issue can be created
- issue-artifact linkage persists
- issue status changes are durable and explicit
