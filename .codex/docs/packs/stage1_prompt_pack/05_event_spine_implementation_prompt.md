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

# Implement only: `src/gdc_adk/substrate/event_spine.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- append-only event recording and retrieval for Stage 1

Use the `Event` contract from `core/contracts.py`.

## Required public functions
- `record_event(event: Event) -> Event`
- `get_event(event_id: str) -> Event`
- `list_events() -> list[Event]`
- `list_events_by_correlation_id(correlation_id: str) -> list[Event]`
- `list_events_by_workflow_run_id(workflow_run_id: str) -> list[Event]`
- `list_events_by_event_type(event_type: str) -> list[Event]`

## Stage 1 event types that must be fully supported in behavior
- `request_received`
- `artifact_created`
- `issue_created`
- `workflow_started`
- `workflow_transitioned`

## Constraints
- initial storage may be in-memory
- behavior must still be append-only
- must preserve record order
- must reject duplicate `event_id`
- must validate event type
- must reject non-serializable payloads

## Must not contain
- provider selection
- workflow branching
- issue creation
- artifact creation
- hidden mutation of historical events

## Definition of done
- valid events append and are retrievable
- lookup by `correlation_id` works
- lookup by `workflow_run_id` works
- invalid or duplicate events fail explicitly
